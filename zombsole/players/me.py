# coding: utf-8
from __future__ import print_function
import sys

from zombsole.things import Player, Zombie
from zombsole.utils import closest
from zombsole.weapons import Rifle


class Me(Player):
    """An interactive player, controlled with the keyboard."""
    def next_step(self, things, t):
        print('Which action?')
        print('w, a, s, d: movement (up, left down, right, like all games)')
        print('j: attack closest zombie')
        print('k: heal self')
        print('l: heal closest player')
        if sys.version_info > (3,):
            action = input()
        else:
            action = raw_input()
        target = None

        if not action:
            self.status = 'sitting idle'
            action = None
        elif action in 'wasd':
            deltas = {
                'w': (0, -1),
                's': (0, 1),
                'a': (-1, 0),
                'd': (1, 0),
            }

            delta = deltas[action]

            self.status = u'walking'
            action = 'move'
            target = (self.position[0] + delta[0],
                      self.position[1] + delta[1])
        elif action == 'j':
            zombies = [thing for thing in things.values()
                       if isinstance(thing, Zombie)]

            if zombies:
                self.status = u'shooting closest zombie'
                action = 'attack'
                target = closest(self, zombies)
            else:
                self.status = u'killing flies, because no zombies left'
                action = None
        elif action == 'k':
            self.status = u'healing self'
            return 'heal', self
        elif action == 'l':
            players = [thing for thing in things.values()
                       if isinstance(thing, Player) and thing is not self]

            if players:
                self.status = u'healing closest friend'
                action = 'heal'
                target = closest(self, players)
            else:
                self.status = u'healing flies, because no players left'
                action = None
        else:
            action = None
            self.status = u'confused, pressing random keys'

        if action:
            return action, target


def create(rules, objectives=None):
    return Me('me', 'red', weapon=Rifle(), rules=rules, objectives=objectives)
