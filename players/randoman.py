#coding: utf-8
import random

from things import Player


class RandoMan(Player):
    def next_step(self, things):
        action = random.choice(('move', 'attack', 'heal'))

        if action in ('attack', 'heal'):
            self.status = action + 'ing'
            target = random.choice(things.values())
        else:
            self.status = 'moving'
            target = list(self.position)
            target[random.choice((0, 1))] += random.choice((-1, 1))
            target = tuple(target)

        return action, target


def create():
    return RandoMan('randoman', 'blue')
