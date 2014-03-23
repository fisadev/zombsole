# coding: utf-8
import random

from things import Player
from utils import possible_moves


class Hamster(Player):
    '''A player allways moves.'''
    def next_step(self, things, t):
        self.status = u'wii wi wiii'
        moves = possible_moves(self, things)
        if moves:
            return 'move', random.choice(moves)


def create(rules, objetives=None):
    return Hamster('hamster', 'white', rules=rules, objetives=objetives)
