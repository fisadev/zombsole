#coding: utf-8
from zombsole.utils import closest
from zombsole.things import Human, Zombie
from zombsole.weapons import Rifle


class Sniper(Human):
    def next_step(self, things):
        zombies = [thing for thing in things.values()
                   if isinstance(thing, Zombie)]
        target = closest(self, zombies)
        return 'attack', target


def create():
    return Sniper('sniper', 'blue', weapon=Rifle())
