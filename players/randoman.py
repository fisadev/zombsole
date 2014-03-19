#coding: utf-8
import random

from things import Player


class RandoMan(Player):
    '''A player that decides what to do with a dice.'''
    def next_step(self, things):
        action = random.choice(('move', 'attack', 'heal'))

        if action in ('attack', 'heal'):
            self.status = action + 'ing'
            target = random.choice(things.values())
        else:
            self.status = u'moving'
            target = list(self.position)
            target[random.choice((0, 1))] += random.choice((-1, 1))
            target = tuple(target)

        return action, target


def create(rules, objetives=None):
    return RandoMan('randoman', 'blue')
