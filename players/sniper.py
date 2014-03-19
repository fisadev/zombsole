#coding: utf-8
from things import Player, Zombie
from utils import closest
from weapons import Rifle


class Sniper(Player):
    def next_step(self, things):
        zombies = [thing for thing in things.values()
                   if isinstance(thing, Zombie)]

        if zombies:
            self.status = 'shooting stuff'
            target = closest(self, zombies)
            return 'attack', target
        else:
            self.status = 'waiting for targets'
            return None


def create(rules, objetives=None):
    return Sniper('sniper', 'blue', weapon=Rifle())
