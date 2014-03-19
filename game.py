#coding: utf-8
import os
import sys
import time

from termcolor import colored

from core import World
from things import Box, Wall, Zombie, ObjetiveLocation


class Rules(object):
    '''Rules to decide when a game ends, and when it's won.'''
    def __init__(self, game):
        self.game = game

    def players_alive(self):
        '''Are there any alive players?'''
        for player in self.game.players:
            if player.life > 0:
                return True
        return False

    def game_ended(self):
        '''Has the game ended?'''
        return not self.players_alive()

    def game_won(self):
        '''Was the game won?'''
        if self.players_alive():
            # never should happen, but ilustrative
            return True, u'you won a game that never ends (?!)'
        else:
            return False, u'everybody is dead :('


class Game(object):
    '''An instance of game controls the flow of the game.

       This includes player and zombies spawning, game main loop, deciding when
       to stop, importing map data, drawing each update, etc.
    '''
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
        '''Spawn players using the provided player create functinons.'''
        for creator_function in player_creators:
            self.players.append(creator_function(self.rules, self.objetives))

        self.world.spawn_in_random(self.players, self.player_spawns)

    def spawn_zombies(self, count):
        '''Spawn N zombies in the world.'''
        zombies = [Zombie() for i in range(count)]
        self.world.spawn_in_random(zombies,
                                   self.zombie_spawns,
                                   fail_if_cant=False)

    def position_draw(self, position):
        '''Get the string to draw for a given position of the world.'''
        # decorations first, then things over them
        thing = self.world.things.get(position)
        decoration = self.world.decoration.get(position)

        if thing is not None:
            return thing.draw()
        elif decoration is not None:
            return decoration.draw()
        else:
            return u' '

    def play(self, frames_per_second=2.0):
        '''Game main loop, ending in a game result with description.'''
        while True:
            self.world.step()

            # mantain the flow of zombies if necessary
            zombies = [thing for thing in self.world.things.values()
                       if isinstance(thing, Zombie)]
            if len(zombies) < self.minimum_zombies:
                self.spawn_zombies(self.minimum_zombies - len(zombies))

            self.draw()

            if self.debug:
                if sys.version_info > (3,):
                    input()
                else:
                    raw_input()
            else:
                time.sleep(1.0 / frames_per_second)

            if self.rules.game_ended():
                return self.rules.game_won()

    def draw(self):
        '''Draw the world.'''
        os.system('clear')

        # print the world
        print('\n'.join(u''.join(self.position_draw((x, y))
                                 for x in range(self.world.size[0]))
                        for y in range(self.world.size[1])))

        # print player stats
        players = sorted(self.players, key=lambda x: x.name)
        for player in players:
            try:
                weapon_name = player.weapon.name
            except:
                weapon_name = u'unarmed'

            if player.life > 0:
                # a small "health bar" with unicode chars, from 0 to 10 chars
                life_chars_count = int((10.0 / player.MAX_LIFE) * player.life)
                life = u'\u2665 %s%s %i' % (life_chars_count * u'\u2588',
                                            (10 - life_chars_count) * u'\u2591',
                                            player.life)
            else:
                life = u'\u2620 [dead]'

            player_stats = u'%s %s (%s): %s' % (life,
                                                player.name,
                                                weapon_name,
                                                player.status or u'-')

            print(colored(player_stats, player.color))

        # print events (of last step) for debugging
        if self.debug:
            print(u'\n'.join([colored(u'%s: %s' % (thing.name, event),
                                      thing.color)
                              for t, thing, event in self.world.events
                              if t == self.world.t]))

    def import_map(self, file_path):
        '''Import things from a utf-8 map file.'''
        zombie_spawns = []
        player_spawns = []
        objetives = []

        max_row = 0
        max_col = 0

        # read the file
        encoding = 'utf-8'
        if sys.version_info > (3,):
            with open(file_path, encoding=encoding) as map_file:
                lines = map_file.read().split('\n')
        else:
            with open(file_path) as map_file:
                lines = map_file.read().decode(encoding).split('\n')

        # for each char, create the corresponding object
        for row_index, line in enumerate(lines):
            max_row = row_index

            for col_index, char in enumerate(line):
                if char:
                    max_col = max(col_index, max_col)

                position = (col_index, row_index)
                if char in (Box.ICON, 'b', 'B'):
                    self.world.spawn_thing(Box(position))
                elif char in (Wall.ICON, 'w', 'W'):
                    self.world.spawn_thing(Wall(position))
                elif char.lower() == 'p':
                    player_spawns.append(position)
                elif char.lower() == 'z':
                    zombie_spawns.append(position)
                elif char.lower() == 'o':
                    objetives.append(position)
                    self.world.spawn_thing(ObjetiveLocation(position),
                                           decoration=True)

        # if had any info, update spawns and objetives
        if player_spawns:
            self.player_spawns = player_spawns
        if zombie_spawns:
            self.zombie_spawns = zombie_spawns
        if objetives:
            self.objetives = objetives

        # be sure everything in the map gets into the world size
        if max_row > self.world.size[1] or max_col > self.world.size[0]:
            message = 'This map is bigger than the choosen size. Needs at least a %ix%i size'
            raise Exception(message % (max_col + 1, max_row + 1))
