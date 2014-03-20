#!/usr/bin/python
# coding: utf-8
'''Serve the players logic as a http service.'''
import json

from flask import Flask, request

from game import get_creator


app = Flask('zombsole_isolator')
players = {}


@app.route('/create_player')
def create_player():
    player_name = request.form['player_name']
    rules = request.form['rules']
    objetives = json.loads(request.form['objetives'])

    player_creator = get_creator('players.' + player_name)
    player = player_creator(rules, objetives)
    players[player_name] = player

    return 'ok'


@app.route('/next_step')
def next_step():
    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
