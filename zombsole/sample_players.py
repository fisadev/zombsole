#coding: utf-8
import random

from zombsole.utils import closest
from zombsole.things import Human, Zombie


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


class ZombieShooter(Human):
    def next_step(self, things):
        zombies = [thing for thing in things.values()
                   if isinstance(thing, Zombie)]
        target = closest(self, zombies)
        return 'attack', target


class AutoHealer(Human):
    def next_step(self, things):
        return 'heal', self
