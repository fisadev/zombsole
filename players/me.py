#coding: utf-8
from things import Player, Zombie
from utils import closest
from weapons import Rifle


class Me(Player):
    '''An interactive player.'''
    def next_step(self, things):
        print 'Which action?'
        print 'w, a, s, d: movement (up, left down, right, like all games)'
        print 'j: attack closest zombie'
        print 'k: heal self'
        print 'l: heal closest player'
        action = raw_input()

        if action in 'wasd':
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
            self.status = u'confused, trying something which is not a valid action'

        if action:
            return action, target


def create(rules, objetives=None):
    return Me('me', 'red', weapon=Rifle())
