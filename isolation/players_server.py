#!/usr/bin/python
# coding: utf-8
'''Serve the players logic as a http service.'''
import json

from flask import Flask, request

from game import create_player


app = Flask('zombsole_isolator')
players = {}


@app.route('/create_player')
def create_server_player():
    player_name = request.form['player_name']
    rules_name = request.form['rules_name']
    objetives = json.loads(request.form['objetives'])

    player = create_player(player_name, rules_name, objetives)
    players[player_name] = player

    return 'ok'


@app.route('/next_step')
def next_step():
    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
