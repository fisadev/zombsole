#coding: utf-8
import random

from zombsole.things import Human


class RandoMan(Human):
    def next_step(self, things):
        action = random.choice(('move', 'attack', 'heal'))

        if action in ('attack', 'heal'):
            target = random.choice(things.values())
        else:
            target = list(self.position)
            target[random.choice((0, 1))] += random.choice((-1, 1))
            target = tuple(target)

        return action, target


def create():
    return RandoMan('randoman', 'blue')