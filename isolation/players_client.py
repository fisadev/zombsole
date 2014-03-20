# coding: utf-8
import json

import requests

from things import Player
import weapons


class IsolatedPlayer(Player):
    def __init__(self, name, rules_name, objetives, isolator_port):
        self.isolator_port = isolator_port
        create_parameters = {
            'player_name': name,
            'rules_name': rules_name,
            'objetives': json.dumps(objetives),
        }
        color, weapon_name = self.do_at_server('create_player',
                                               create_parameters)
        weapon = getattr(weapons, weapon_name)()

        super(IsolatedPlayer, self).__init__(name, color, weapon=weapon)

    def next_step(self, things):
        next_step_parameters = {
            'player_name': self.name,
            'life': self.life,
            'position': json.dumps(self.position),
            'things': json.dumps(things),
        }
        step_result, status = self.do_at_server('next_step',
                                                next_step_parameters)
        self.status = status
        return step_result

    def do_at_server(self, url, parameters):
        full_url = 'http://localhost:%i/%s' % (self.isolator_port, url)
        response = requests.post(full_url, parameters).content
        return json.loads(response)


def create_player_client(player_name, rules_name, objetives, isolator_port):
    '''Create a proxy which mimicks a player, but calling players on the
       isolated server.'''

    return IsolatedPlayer(player_name, rules_name, objetives, isolator_port)
