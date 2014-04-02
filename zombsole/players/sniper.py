# coding: utf-8
from zombsole.things import Player, Zombie
from zombsole.utils import closest
from zombsole.weapons import Rifle


class Sniper(Player):
    """A player that stays still and shoots zombies."""
    def next_step(self, things, t):
        zombies = [thing for thing in things.values()
                   if isinstance(thing, Zombie)]

        if zombies:
            self.status = u'shooting stuff'
            target = closest(self, zombies)
            return 'attack', target
        else:
            self.status = u'waiting for targets'
            return None


def create(rules, objectives=None):
    return Sniper('sniper', 'yellow', weapon=Rifle(), rules=rules,
                  objectives=objectives)
