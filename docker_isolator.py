#!/usr/bin/python
# coding: utf-8
'''Zomsole players isolation utility.

Usage:
    ./docker_isolator.py build
    ./docker_isolator.py serve_players


build_isolator:
    Will build the docker container to use as docker isolation. Run this to update
    the isolator with the changes made to players, maps, game, etc.

serve_players:
    Will start the players server. This is used inside the docker isolator, you
    shouldn't need to call this command manually.
'''
from __future__ import print_function

from docker import Client
from docopt import docopt


def build():
    print('Building docker image...')
    client = Client(base_url='unix://var/run/docker.sock', timeout=10)
    client.build(path='.')
    print('Done!')


def serve_players():
    '''Serve the players logic as a http service.'''
    pass


def player_creator(player_name):
    '''Create a player creator function, mimicking the real function,
       but returning a proxy to players served with serve_players.'''
    pass


def main():
    arguments = docopt(__doc__)

    if arguments['build']:
        # build the docker image to use as players isolation
        build()
    elif arguments['serve_players']:
        # start the players server
        serve_players()

if __name__ == '__main__':
    main()
