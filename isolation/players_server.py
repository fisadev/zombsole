#!/usr/bin/python
# coding: utf-8
'''Serve the players logic as a http service.'''
from docker import Client
from flask import Flask


app = Flask('zombsole_isolator')


@app.route('/')
def index():
    return 'ok'


def start_isolator(port):
    '''Build the docker image to use as isolator of players, and then start
       it.
    '''
    print('Building docker image...')
    client = Client(base_url='unix://var/run/docker.sock', timeout=10)
    client.build(path='.', tag='zombsole_isolator')
    print('Done!')


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
