# coding: utf-8
from zombsole.things import Player


class Troll(Player):
    """A player that always heals itself.

       (trolls have regenerative capabilities, hence the name).
    """
    def next_step(self, things, t):
        self.status = u'healing myself'
        return 'heal', self


def create(rules, objectives=None):
    return Troll('troll', 'blue', rules=rules, objectives=objectives)
