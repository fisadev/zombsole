# coding: utf-8
from __future__ import print_function

import os
import sys
import time

from termcolor import colored

from core import World
from things import Box, Wall, Zombie, ObjetiveLocation


def get_creator(module_name):
    '''Get the create() function from a module.'''
    module = __import__(module_name, fromlist=['create', ])
    create_function = getattr(module, 'create')

    return create_function


def create_player(name, rules_name, objetives):
    creator = get_creator('players.' + name)
    return creator(rules_name, objetives)


def create_rules(name, game):
    creator = get_creator('rules.' + name)
    return creator(game)


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


class Map(object):
    '''A map for a world.'''
    def __init__(self, size, things, player_spawns=None, zombie_spawns=None,
                 objetives=None):
        self.size = size
        self.things = things
        self.player_spawns = player_spawns
        self.zombie_spawns = zombie_spawns
        self.objetives = objetives

    @classmethod
    def from_file(cls, file_path):
        '''Import data from a utf-8 map file.'''
        zombie_spawns = []
        player_spawns = []
        objetives = []
        things = []

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
                    things.append(Box(position))
                elif char in (Wall.ICON, 'w', 'W'):
                    things.append(Wall(position))
                elif char.lower() == 'p':
                    player_spawns.append(position)
                elif char.lower() == 'z':
                    zombie_spawns.append(position)
                elif char.lower() == 'o':
                    objetives.append(position)
                    things.append(ObjetiveLocation(position))

        return Map((max_col, max_row),
                   things,
                   player_spawns,
                   zombie_spawns,
                   objetives)


class Game(object):
    '''An instance of game controls the flow of the game.

       This includes player and zombies spawning, game main loop, deciding when
       to stop, importing map data, drawing each update, etc.
    '''
    def __init__(self, rules_name, player_names, map_, initial_zombies=0,
                 minimum_zombies=0, docker_isolator=False, debug=False,
                 isolator_port=8000, use_basic_icons=False):
        self.players = []

        self.rules_name = rules_name
        self.rules = get_creator('rules.' + rules_name)(self)
        self.map = map_
        self.minimum_zombies = minimum_zombies
        self.docker_isolator = docker_isolator
        self.isolator_port = isolator_port
        self.debug = debug
        self.use_basic_icons = use_basic_icons

        self.world = World(self.map.size, debug=debug)

        for thing in self.map.things:
            self.world.spawn_thing(thing)

        if docker_isolator:
            from isolation.players_client import create_player_client
            self.players = [create_player_client(name, rules_name,
                                                 self.map.objetives,
                                                 self.isolator_port)
                            for name in player_names]
        else:
            self.players = [create_player(name, rules_name,
                                          self.map.objetives)
                            for name in player_names]

        self.spawn_players()
        self.spawn_zombies(initial_zombies)

    def spawn_players(self):
        '''Spawn players using the provided player create functinons.'''
        self.world.spawn_in_random(self.players, self.map.player_spawns)

    def spawn_zombies(self, count):
        '''Spawn N zombies in the world.'''
        zombies = [Zombie() for i in range(count)]
        self.world.spawn_in_random(zombies,
                                   self.map.zombie_spawns,
                                   fail_if_cant=False)

    def position_draw(self, position):
        '''Get the string to draw for a given position of the world.'''
        # decorations first, then things over them
        thing = self.world.things.get(position) or \
                self.world.decoration.get(position)

        if thing is not None:
            if self.use_basic_icons:
                icon = thing.icon_basic
            else:
                icon = thing.icon
            return colored(icon, thing.color)
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
        screen = ''

        # print the world
        screen += '\n'.join(u''.join(self.position_draw((x, y))
                                     for x in range(self.world.size[0]))
                            for y in range(self.world.size[1]))

        # game stats
        screen += '\nticks: %i deaths: %i' % (self.world.t, self.world.deaths)

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
                life_chars = life_chars_count * u'\u2588'
                no_life_chars = (10 - life_chars_count) * u'\u2591'
                life_bar = u'\u2665 %s%s' % (life_chars, no_life_chars)
            else:
                life_bar = u'\u2620 [dead]'

            player_stats = u'%s %s <%i %s %s>: %s' % (life_bar,
                                                      player.name,
                                                      player.life,
                                                      str(player.position),
                                                      weapon_name,
                                                      player.status or u'-')

            screen += '\n' + colored(player_stats, player.color)

        # print events (of last step) for debugging
        if self.debug:
            screen += u'\n'
            screen += u'\n'.join([colored(u'%s: %s' % (thing.name, event),
                                          thing.color)
                                  for t, thing, event in self.world.events
                                  if t == self.world.t])
        os.system('clear')
        print(screen)
