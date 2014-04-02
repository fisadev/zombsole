#!/usr/bin/env python
# coding: utf-8
"""Serve the players logic as a http service."""
import json
import pickle

from flask import Flask, request
from zombsole.game import create_player
from zombsole.things import Thing


app = Flask('zombsole_isolator')
players = {}


@app.route('/create_player', methods=['POST'])
def create_server_player():
    parameters = pickle.loads(request.form['parameters'])

    player_name = parameters['player_name']
    rules_name = parameters['rules_name']
    objectives = parameters['objectives']

    player = create_player(player_name, rules_name, objectives)
    players[player_name] = player

    return json.dumps([player.color, player.weapon.name])


@app.route('/next_step', methods=['POST'])
def next_step():
    parameters = pickle.loads(request.form['parameters'])

    player_name = parameters['player_name']
    life = parameters['life']
    position = parameters['position']
    things = parameters['things']
    t = parameters['t']

    player = players[player_name]
    player.life = life
    player.position = position
    things[position] = player

    step_result = player.next_step(things, t)
    status = player.status

    target_replace = False

    if step_result:
        target = step_result[1]
        if isinstance(target, Thing):
            target = target.position
            target_replace = True

        step_result = step_result[0], target

    return json.dumps((step_result, status, target_replace))


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
