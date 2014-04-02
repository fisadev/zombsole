# coding: utf-8
import random

from zombsole.things import Player


class RandoMan(Player):
    """A player that decides what to do with a dice."""
    def next_step(self, things, t):
        action = random.choice(('move', 'attack', 'heal'))

        if action in ('attack', 'heal'):
            self.status = action + 'ing'
            target = random.choice(list(things.values()))
        else:
            self.status = u'moving'
            target = list(self.position)
            target[random.choice((0, 1))] += random.choice((-1, 1))
            target = tuple(target)

        return action, target


def create(rules, objectives=None):
    return RandoMan('randoman', 'red', rules=rules, objectives=objectives)
