#coding: utf-8
import os
import time

from termcolor import colored

from core import World
from things import Box, Wall, Zombie, ObjetiveLocation
from utils import distance, closest


class Game(object):
    def __init__(self, players, size, map_file=None, player_spawns=None,
                 zombie_spawns=None, objetives=None, initial_zombies=0,
                 minimum_zombies=0, debug=False):
        self.players = players

        self.player_spawns = player_spawns
        self.zombie_spawns = zombie_spawns
        self.objetives = objetives
        self.minimum_zombies = minimum_zombies
        self.debug = debug

        self.world = World(size, debug=debug)

        if map_file is not None:
            self.import_map(map_file)

        self.world.spawn_in_random(self.players, self.player_spawns)
        self.spawn_zombies(initial_zombies)

    def spawn_zombies(self, count):
        zombies = [Zombie() for i in range(count)]
        self.world.spawn_in_random(zombies,
                                   self.zombie_spawns,
                                   fail_if_cant=False)

    def players_alive(self):
        for player in self.players:
            if player.life > 0:
                return True
        return False

    def game_ended(self):
        return not self.players_alive()

    def position_draw(self, position):
        thing = self.world.things.get(position)
        decoration = self.world.decoration.get(position)

        if thing is not None:
            return thing.draw()
        elif decoration is not None:
            return decoration.draw()
        else:
            return u' '

    def play(self, frames_per_second=2.0):
        '''Game main loop.'''
        while True:
            self.world.step()

            zombies = [thing for thing in self.world.things.values()
                       if isinstance(thing, Zombie)]
            if len(zombies) < self.minimum_zombies:
                self.spawn_zombies(self.minimum_zombies - len(zombies))

            self.draw()

            if self.debug:
                raw_input()
            else:
                time.sleep(1.0 / frames_per_second)

            if self.game_ended():
                return

    def draw(self):
        '''Draw the world'''
        os.system('clear')

        # print the world
        print '\n'.join(u''.join(self.position_draw((x, y))
                                 for x in xrange(self.world.size[0]))
                        for y in xrange(self.world.size[1]))

        # print player stats
        players = sorted(self.players, key=lambda x: x.name)
        for player in players:
            try:
                weapon_name = player.weapon.name
            except:
                weapon_name = u'unarmed'

            if player.life > 0:
                life_chars_count = int((10.0 / player.MAX_LIFE) * player.life)
                life = u'\u2665 %s%s %i' % (life_chars_count * u'\u2588',
                                            (10 - life_chars_count) * u'\u2591',
                                            player.life)
            else:
                life = u'\u2620 dead'

            print colored(u'%s %s (%s): %s' % (life,
                                               player.name,
                                               weapon_name,
                                               player.status or u'-'),
                          player.color)

        # print events for debugging
        if self.debug:
            print u'\n'.join([colored(u'%s: %s' % (thing.name, event),
                                      thing.color)
                              for t, thing, event in self.world.events
                              if t == self.world.t])

    def import_map(self, file_path):
        '''Import things from a utf-8 map file.'''
        with open(file_path) as map_file:
            lines = unicode(map_file.read(), 'utf-8').split('\n')

            zombie_spawns = []
            player_spawns = []
            objetives = []

            for row_index, line in enumerate(lines):
                for col_index, char in enumerate(line):
                    position = (col_index, row_index)
                    if char == Box.ICON:
                        self.world.spawn_thing(Box(position))
                    elif char == Wall.ICON:
                        self.world.spawn_thing(Wall(position))
                    elif char == 'p':
                        player_spawns.append(position)
                    elif char == 'z':
                        zombie_spawns.append(position)
                    elif char == 'o':
                        objetives.append(position)
                        self.world.spawn_thing(ObjetiveLocation(position),
                                               decoration=True)

            if player_spawns:
                self.player_spawns = player_spawns
            if zombie_spawns:
                self.zombie_spawns = zombie_spawns
            if objetives:
                self.objetives = objetives


class SafeHouseGame(Game):
    '''A kind of game where players must get into a safe house.

       Team wins when all alive players are inside the safe house.
    '''
    def game_ended(self):
        if self.objetives is None:
            raise Exception('Safe house game requires objetives defined.')

        if not self.players_alive():
            return True
        else:
            in_house = [player.position in self.objetives
                        for player in self.players
                        if player.life > 0]
            return all(in_house)


class EvacuationGame(Game):
    '''A kind of game where players must get together to be evacuated.

       Team wins when all alive players are at 2 or less distance from another
       alive player, and at least half of the team must survive.
    '''
    def game_ended(self):
        alive_players = [player for player in self.players
                         if player.live > 0]
        if len(alive_players) < len(self.players) / 2:
            return True
        else:
            for player in self.players:
                others = [other for other in self.players
                        if other is not player and other.life > 0]
                closest_other = closest(player, others)
                if distance(player.position, closest_other.position) > 2:
                    return False

            return True


class ExterminationGame(Game):
    '''A kind of game where players must exterminate all zombies.

       Team wins when all zombies are dead.
    '''
    def game_ended(self):
        if not self.players_alive():
            return True
        else:
            zombies = [thing for thing in self.world.things.values()
                       if isinstance(thing, Zombie) and thing.life > 0]

            return not zombies
