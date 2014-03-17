#coding: utf-8
from things import Human


class Troll(Human):
    def next_step(self, things):
        return 'heal', self

# (trolls have regenerative capabilities)


def create():
    return Troll('troll', 'blue')
