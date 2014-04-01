#!/usr/bin/env python
# coding: utf-8
"""Zomsole game runner.

Usage:
    ./play.py --help
    ./play.py RULES PLAYERS [-m MAP] [-s SIZE] [-z INITIAL_ZOMBIES] [-n MINIMUM_ZOMBIES] [-d] [-i [-p ISOLATOR_PORT ]] [-b] [-f MAX_FRAMES] [-a [-v ARDUINO_DEVICE] [-u ARDUINO_BAUDS]]
    ./play.py list_rules
    ./play.py list_maps

    GAME:     Should be the name of a type of game. Use list_rules to see a complete list.
    PLAYERS:  Should be a list with the structure playerA,playerB,playerC,...
              You can also specify how much instances of each player, like this:
              playerA:3,playerB,playerC:10,...

Options:
    -h --help            Show this help.
    -m MAP               The map name to use (an empty world by default)
                         Use list_maps to list available maps.
    -s SIZE              The size of the world. Format: COLUMNSxROWS
    -z INITIAL_ZOMBIES   The initial amount of zombies [default: 0]
    -n MINIMUM_ZOMBIES   The minimum amount of zombies at all times [default: 0]
    -d                   Debug mode (lots of extra info, and step by step game play)
    -f MAX_FRAMES        Maximum frames per second [default: 2].
    -i                   Isolate the players process using docker, to prevent hacks to
                         the world (you will need docker installed for this to work,
                         and the isolator built and running. See the project docs for
                         more info).
    -p ISOLATOR_PORT     The ISOLATOR_PORT is the port on which the isolator is
                         running [default: 8000].
    -b                   Use basic icons if you have trouble with the normal icons.
    -a                   Use external arduino screen.
    -v ARDUINO_DEVICE    When using arduino screen, the device path of the serial
                         connection [default: /dev/ttyACM0]
    -u ARDUINO_BAUDS     When using arduino screen, the bauds of the serial
                         connection [default: 9600]

list_rules:
    Will list available game rules.

list_maps:
    Will list available game maps.
"""
from __future__ import print_function

from os import path, listdir

from docopt import docopt

from game import Game, Map


def play():
    """Initiate a game, using the command line arguments as configuration."""
    arguments = docopt(__doc__)

    if arguments['list_rules']:
        # list all possible game rules
        names = [name.replace('.py', '')
                 for name in listdir('rules')
                 if '__init__' not in name and '.pyc' not in name]
        print('\n'.join(names))
    elif arguments['list_maps']:
        # list all possible maps
        print('\n'.join(listdir('maps')))
    else:
        # start a game
        # parse arguments
        rules_name = arguments['RULES']
        initial_zombies = int(arguments['-z'])
        minimum_zombies = int(arguments['-n'])
        docker_isolator = arguments['-i']
        debug = arguments['-d']
        isolator_port = int(arguments['-p'])
        use_basic_icons = arguments['-b']
        max_frames = int(arguments['-f'])
        use_arduino = arguments['-a']
        arduino_device = arguments['-v']
        arduino_bauds = int(arguments['-u'])

        player_names = []
        for player_part in arguments['PLAYERS'].split(','):
            if ':' in player_part:
                player_name, count = player_part.split(':')
                count = int(count)
            else:
                player_name = player_part
                count = 1
            player_names.extend([player_name, ] * count)

        size = arguments['-s']
        if size:
            size = tuple(map(int, size.split('x')))

        map_name = arguments['-m']
        if map_name:
            map_file = path.join('maps', map_name)
            map_ = Map.from_file(map_file)

            if size:
                if size[0] < map_.size[0] or size[1] < map_.size[1]:
                    message = "Map (%s) doesn't fit in specified size (%s) " \
                              "(leave it empty to use best fit)"
                    raise Exception(message % (str(map_.size), str(size)))
                else:
                    map_.size = size
        else:
            if not size:
                size = 30, 10

            map_ = Map(size, [])

        # create and start game
        g = Game(rules_name=rules_name,
                 player_names=player_names,
                 map_=map_,
                 initial_zombies=initial_zombies,
                 minimum_zombies=minimum_zombies,
                 docker_isolator=docker_isolator,
                 isolator_port=isolator_port,
                 debug=debug,
                 use_basic_icons=use_basic_icons,
                 use_arduino=use_arduino,
                 arduino_device=arduino_device,
                 arduino_bauds=arduino_bauds)
        g.play(max_frames)


if __name__ == '__main__':
    play()
