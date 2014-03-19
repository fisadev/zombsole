#coding: utf-8
import os
import time

from termcolor import colored

from core import World
from things import Box, Wall, Zombie, ObjetiveLocation


class Rules(object):
    def __init__(self, game):
        self.game = game

    def players_alive(self):
        for player in self.game.players:
            if player.life > 0:
                return True
        return False

    def game_ended(self):
        return not self.players_alive()

    def game_won(self):
        if self.players_alive():
            # never should happen, but ilustrative
            return True, u'you won a game that never ends (?!)'
        else:
            return False, u'everybody is dead :('


class Game(object):
    def __init__(self, rules_creator, player_creators, size, map_file=None,
                 player_spawns=None, zombie_spawns=None, objetives=None,
                 initial_zombies=0, minimum_zombies=0, debug=False):
        self.players = []

        self.rules = rules_creator(self)
        self.player_spawns = player_spawns
        self.zombie_spawns = zombie_spawns
        self.objetives = objetives
        self.minimum_zombies = minimum_zombies
        self.debug = debug

        self.world = World(size, debug=debug)

        if map_file is not None:
            self.import_map(map_file)

        self.spawn_players(player_creators)
        self.spawn_zombies(initial_zombies)

    def spawn_players(self, player_creators):
        for creator_function in player_creators:
            self.players.append(creator_function(self.rules, self.objetives))

        self.world.spawn_in_random(self.players, self.player_spawns)

    def spawn_zombies(self, count):
        zombies = [Zombie() for i in range(count)]
        self.world.spawn_in_random(zombies,
                                   self.zombie_spawns,
                                   fail_if_cant=False)

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

            if self.rules.game_ended():
                return self.rules.game_result()

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

            max_row = 0
            max_col = 0

            for row_index, line in enumerate(lines):
                max_row = row_index

                for col_index, char in enumerate(line):
                    if char:
                        max_col = max(col_index, max_col)

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

            if max_row > self.world.size[1] or max_col > self.world.size[0]:
                message = 'This map is bigger than the choosen size. Needs at least a %ix%i size'
                raise Exception(message % (max_col + 1, max_row + 1))
