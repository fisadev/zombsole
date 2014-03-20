# coding: utf-8
from docker import Client


def build():
    '''Build the docker image to use as isolator.'''
    print('Building docker image...')
    client = Client(base_url='unix://var/run/docker.sock', timeout=10)
    client.build(path='.', tag='zombsole_isolator')
    print('Done!')


def start(port):
    '''Start running the isolator container, with the players server inside.'''
    pass
