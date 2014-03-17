#coding: utf-8
'''Zomsole game runner.

Usage:
    run.py --help
    run.py GAME SIZE PLAYERS [-m MAP_FILE] [-i INITIAL_ZOMBIES] [-n MINIMUM_ZOMBIES]
    run.py list_game_types

    GAME:     Should be the name of a type of game. Use list_game_types to see
              a complete list.
    SIZE:     COLUMNSxROWS
    PLAYERS:  Should be a list with the structure player1,player2,player3,...

Options:
    -h --help            Show this help.
    -m MAP_FILE          The map file to use (an empty world by default)
    -i INITIAL_ZOMBIES   The initial amount of zombies [default: 0]
    -n MINIMUM_ZOMBIES   The minimum amount of zombies at all times [default: 0]
'''
from docopt import docopt

import zombsole.game


def get_game_classes():
    classes_dict = {}
    for name in dir(zombsole.game):
        thing = getattr(zombsole.game, name)
        if type(thing) == type and 'Game' in name:
            name = name.replace('Game', '').lower()
            if name:
                classes_dict[name] = thing

    return classes_dict


def run():
    arguments = docopt(__doc__)
    game_classes = get_game_classes()

    if arguments['list_game_types']:
        for name, game_class in game_classes.items():
            print name, ':'
            print game_class.__doc__.strip()
            print '--'
    else:
        # parse arguments
        game_class = game_classes[arguments['GAME']]
        size = map(int, arguments['SIZE'].split('x'))
        player_names = arguments['PLAYERS'].split(',')
        map_file=arguments['-m']
        initial_zombies = int(arguments['-i'])
        minimum_zombies = int(arguments['-n'])

        # create players
        players = []
        for player_name in player_names:
            player_module = __import__(player_name)
            create_function = getattr(player_module, 'create')
            players.append(create_function())

        # create and start game
        g = game_class(players=players,
                    size=size,
                    map_file=map_file,
                    initial_zombies=initial_zombies,
                    minimum_zombies=minimum_zombies)
        g.play()


if __name__ == '__main__':
    run()
