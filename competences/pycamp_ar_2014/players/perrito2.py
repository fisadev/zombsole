# coding: utf-8
from things import Player, Zombie
from weapons import Rifle
from utils import closest, possible_moves, distance


class Perrito(Player):
    """docstring for Mati"""
    yo = 'Perrito'
    vida = Player.MAX_LIFE
    next_move = 'heal'

    def next_step(self, things, t):
        # if self.life < self.vida :
        # 	if self.next_move == 'move':
        # 		action = self.next_move
        # 		target = tuple(random.choice(emptyPlace(self,things)))
        # 		self.next_move = 'heal'
        # 	elif self.next_move == 'heal':
        # 		action = self.next_move
        # 		target = self
        # 		self.vida = self.life
        # 		self.next_move = 'move'
        # 	else:
        # 		self.next_move = 'move'

        # else:
        action = 'heal'
        target = self

        try:
            target = getClosestZombie(self, things)
            if canAttack(self, target):
                action = 'attack'
            else:
                action = 'heal'
                target = self
        except:
            pass
        try:
            name = target.name
        except:
            name = target
        self.status = 'Perrito'
        self.vida = self.life
        if action:
            return action, target


def moveInteligent(self, thing):
    pass


def emptyPlace(self, things):
    return possible_moves(self, things)


def getClosestZombie(self, things):
    zombies = []
    other = [thing for thing in things.values() if isinstance(thing, Zombie)]
    zombies = closest(self, other)
    return zombies


def canAttack(self, zombies):
    if distance(self, zombies) > self.weapon.max_range:
        return False
    else:
        return True


def getPlayerDieing(things):
    dieing = []
    other_players = getPlayers(things)
    for item in other_players:
        dieing.append([item.name, item.life])
    dieing = sorted(dieing, key=lambda x: x[1])
    return dieing


def getPlayers(things):
    other = [thing for thing in things.values() if isinstance(thing, Player)]
    return other


def create(rules, objectives=None):
    color = 'red'
    nomb = "Perrito"
    return Perrito(nomb, color, weapon=Rifle(), objectives=objectives)