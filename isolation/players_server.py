#!/usr/bin/python
# coding: utf-8
'''Serve the players logic as a http service.'''
import json

from flask import Flask, request

from game import create_player


app = Flask('zombsole_isolator')
players = {}


@app.route('/create_player', methods=['POST'])
def create_server_player():
    player_name = request.form['player_name']
    rules_name = request.form['rules_name']
    objetives = json.loads(request.form['objetives'])

    player = create_player(player_name, rules_name, objetives)
    players[player_name] = player

    return json.dumps([player.color, player.weapon.name])


@app.route('/next_step', methods=['POST'])
def next_step():
    player_name = request.form['player_name']
    life = int(request.form['life'])
    position = json.loads(request.form['position'])
    if position is not None:
        position = tuple(position)
    things = json.loads(request.form['things'])

    player = players[player_name]
    player.life = life
    player.position = position

    step_result = player.next_step(things)
    status = player.status

    return json.dumps((step_result, status))


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
