#!/usr/bin/python
# coding: utf-8
'''Zomsole game runner.

Usage:
    ./play.py --help
    ./play.py RULES SIZE PLAYERS [-m MAP] [-i INITIAL_ZOMBIES] [-n MINIMUM_ZOMBIES] [-d] [-s ISOLATION_PORT [-p]]
    ./play.py list_rules
    ./play.py list_maps

    GAME:     Should be the name of a type of game. Use list_rules to see a complete list.
    SIZE:     COLUMNSxROWS
    PLAYERS:  Should be a list with the structure player1,player2,player3,...

Options:
    -h --help            Show this help.
    -m MAP               The map name to use (an empty world by default)
                         Use list_maps to list available maps.
    -i INITIAL_ZOMBIES   The initial amount of zombies [default: 0]
    -n MINIMUM_ZOMBIES   The minimum amount of zombies at all times [default: 0]
    -d                   Debug mode (lots of extra info, and step by step game play)
    -s                   Isolate the players process using docker, to prevent hacks to
                         the world (you will need docker installed for this to work).
    -p ISOLATION_PORT    The ISOLATION_PORT is the port on which the isolator will run.

list_rules:
    Will list available game rules.

list_maps:
    Will list available game maps.
'''
from __future__ import print_function

from os import path, listdir

from docopt import docopt
from termcolor import colored

from game import Game


def get_creator(module_name):
    '''Get the create() function from a module.'''
    module = __import__(module_name, fromlist=['create',])
    create_function = getattr(module, 'create')

    return create_function


def play():
    '''Initiate a game, using the command line arguments as configuration.'''
    arguments = docopt(__doc__)

    if arguments['list_rules']:
        # list all posible game rules
        names = [name.replace('.py', '')
                 for name in listdir('rules')
                 if '__init__' not in name and '.pyc' not in name]
        print('\n'.join(names))
    elif arguments['list_maps']:
        # list all posible maps
        print('\n'.join(listdir('maps')))
    else:
        # start a game
        # parse arguments
        rules_creator = get_creator('rules.' + arguments['RULES'])
        size = tuple(map(int, arguments['SIZE'].split('x')))
        player_names = arguments['PLAYERS'].split(',')
        map_file = path.join('maps', arguments['-m'])
        initial_zombies = int(arguments['-i'])
        minimum_zombies = int(arguments['-n'])
        docker_isolation = arguments['-s']
        debug = arguments['-d']


        if docker_isolation:
            # create the player clients, and start the players server
            # inside a docker container
            # player creators will be those proxying the real players
            port = int(arguments.get('-p', 8000))
            from isolation.players_server import start_isolator
            from isolation.players_client import player_creator

            player_creators = [player_creator(name, port)
                               for name in player_names]
            start_isolator(port)
        else:
            # just use the create functions of players
            player_creators = [get_creator('players.' + name)
                               for name in player_names]

        # create and start game
        g = Game(rules_creator=rules_creator,
                 player_creators=player_creators,
                 size=size,
                 map_file=map_file,
                 initial_zombies=initial_zombies,
                 minimum_zombies=minimum_zombies,
                 debug=debug)
        won, description = g.play()
        print('')
        if won:
            print(colored(u'WIN! ', 'green'))
        else:
            print(colored(u'GAME OVER ', 'red'))
        print(description)


if __name__ == '__main__':
    play()
