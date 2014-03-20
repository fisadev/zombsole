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
        color, weapon_name = self.get('create_player', create_parameters)
        weapon = getattr(weapons, weapon_name)()

        super(IsolatedPlayer, self).__init__(name, color, weapon=weapon)

    def next_step(self, things):
        pass

    def get(self, url, parameters):
        full_url = 'http://localhost:%i/%s' % (self.isolator_port, url)
        response = requests.get(full_url, parameters).content
        return json.loads(response)


def create_player_client(player_name, rules_name, objetives, isolator_port):
    '''Create a proxy which mimicks a player, but calling players on the
       isolated server.'''

    return IsolatedPlayer(player_name, rules_name, objetives, isolator_port)
