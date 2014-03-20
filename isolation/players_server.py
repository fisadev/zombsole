#!/usr/bin/python
# coding: utf-8
'''Serve the players logic as a http service.'''
import json
import pickle

from flask import Flask, request

from game import create_player
from things import Thing


app = Flask('zombsole_isolator')
players = {}


@app.route('/create_player', methods=['POST'])
def create_server_player():
    input_data = pickle.loads(request.form['input_data'])

    player_name = input_data['player_name']
    rules_name = input_data['rules_name']
    objetives = input_data['objetives']

    player = create_player(player_name, rules_name, objetives)
    players[player_name] = player

    return json.dumps([player.color, player.weapon.name])


@app.route('/next_step', methods=['POST'])
def next_step():
    input_data = pickle.loads(request.form['input_data'])

    player_name = input_data['player_name']
    life = input_data['life']
    position = input_data['position']
    things = input_data['things']

    player = players[player_name]
    player.life = life
    player.position = position
    things[position] = player

    step_result = player.next_step(things)
    status = player.status

    target_replace = None

    if step_result is not None:
        target = step_result[1]
        if target is player:
            target = None
            target_replace = 'self'
        elif isinstance(target, Thing):
            target = target.position
            target_replace = 'thing'

        step_result = step_result[0], target

    return json.dumps((step_result, status, target_replace))


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
