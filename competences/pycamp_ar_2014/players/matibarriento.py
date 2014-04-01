# coding: utf-8
from things import Player,Zombie,Box,Wall
from weapons import Rifle, Shotgun, Gun
from utils import closest, possible_moves, distance
import random
from core import World

class Mati(Player):
	"""docstring for Mati"""

	vida = Player.MAX_LIFE
	next_move = 'heal'

	def next_step(self, things,t):
		if self.life < self.vida :
			if self.next_move == 'move':
				action = self.next_move
				target = tuple(random.choice(emptyPlace(self,things)))
				self.next_move = 'heal'
			elif self.next_move == 'heal':
				action = self.next_move
				target = self
				self.vida = self.life
				self.next_move = 'move'
			else:
				self.next_move = 'move'

		else:
			target = getClosestZombie(self,things)
			if (canAttack(self,target)):
				action = 'attack'
			else:
				action = 'move'
				target = closest(target,possible_moves(self,things))
		try:
			name = target.name
		except:
			name = target
		self.status = str(action)#, str(name)#, self.weapon.max_range
		self.vida = self.life
		if action:
			return action, target

def moveInteligent(self,thing):
	pass

def emptyPlace(self,things):
	return possible_moves(self,things)

def getClosestZombie(self,things):
	zombies = []
	other = [thing for thing in things.values() if isinstance(thing, Zombie)]
	zombies = closest(self, other)
	return zombies

def canAttack(self,zombies):
	if(distance(self,zombies) > self.weapon.max_range):
		return False
	else:
		return True

def getPlayerDieying(things):
	dieying = []
	other_players = getPlayers(things)
	for item in other_players:
			dieying.append([item.name,item.life])
	dieying = sorted(dieying,key = lambda x:x[1])
	return dieying

def getPlayers(things):
	other = [thing for thing in things.values() if isinstance(thing, Player)]
	return other

def create(rules, objectives=None):
	color = random.choice(['red','yellow','blue','white'])
	nomb = random.choice(['Mati','Buff','ElMati','Matias','Fernet'])
	return Mati(nomb, color, weapon = Rifle(),objectives = objectives)
