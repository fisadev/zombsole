# coding: utf-8
import json
import pickle

import requests

from zombsole.things import Player
from zombsole import weapons


class IsolatedPlayer(Player):
    def __init__(self, name, rules_name, objectives, isolator_port):
        self.isolator_port = isolator_port
        parameters = {
            'player_name': name,
            'rules_name': rules_name,
            'objectives': objectives,
        }
        color, weapon_name = self.do_at_server('create_player', parameters)
        weapon = getattr(weapons, weapon_name)()

        super(IsolatedPlayer, self).__init__(name, color, weapon=weapon)

    def next_step(self, things, t):
        parameters = {
            'player_name': self.name,
            'life': self.life,
            'position': self.position,
            'things': things,
            't': t,
        }
        step_result, status, target_replace = self.do_at_server('next_step',
                                                                parameters)
        self.status = status

        if step_result:
            action, target = step_result
            target = tuple(target)
            step_result = action, target

        if target_replace:
            target = step_result[1]
            target = things.get(target)
            if target:
                step_result = step_result[0], target
            else:
                raise Exception('Target is not in that location anymore '
                                '(outdated instance).')

        return step_result

    def do_at_server(self, url, parameters):
        full_url = 'http://localhost:%i/%s' % (self.isolator_port, url)
        post_data = {'parameters': pickle.dumps(parameters)}
        response = requests.post(full_url, post_data).content
        return json.loads(response)


def create_player_client(player_name, rules_name, objectives, isolator_port):
    """Create a proxy which mimics a player, but calling players on the
       isolated server."""

    return IsolatedPlayer(player_name, rules_name, objectives, isolator_port)
