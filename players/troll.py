#coding: utf-8
from things import Player


class Troll(Player):
    def next_step(self, things):
        self.status = u'healing myself'
        return 'heal', self

# (trolls have regenerative capabilities)


def create(rules, objetives=None):
    return Troll('troll', 'blue')
