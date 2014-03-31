# coding: utf-8
from __future__ import print_function
import sys

from things import Player, Zombie, DeadBody
from core import FightingThing
from utils import closest, distance
from weapons import *
import time
import random

class God(FightingThing):
    MAX_LIFE = 100
    ICON = u'\u2A30'
    ICON_BASIC = u'G'

    def __init__(self, name, color, position=None, weapon=None, rules=None):
        dead_decoration = DeadBody('dead ' + name, color, None)

        super(God, self).__init__(name, God.ICON, God.ICON_BASIC,
                                     color, God.MAX_LIFE, weapon, position,
                                     dead_decoration)

class Morpheus(God):
    '''An interactive player, controlled with the keyboard.'''
    def __init__(self, name, color, position=None, weapon=None, rules=None):
        self.rules = rules
        self.target_to_kill = None
        super(Morpheus, self).__init__(name, color, position=position, weapon=weapon)

    def next_step(self, things, t):
        zombies = [thing for thing in things.values()
                   if isinstance(thing, Zombie)]
        humans = []
        for thing in things.values():
            if isinstance(thing, Player) and thing.name != 'morpheus':
                humans.append(thing)

        reachable_z = []
        team = []
        target = None
        for z in zombies:
            if (distance(z, self) < self.weapon.max_range):
                reachable_z.append(z)

        if (self.rules == 'extermination'):
            self.set_target_to_kill(zombies)
            if reachable_z:
                self.status = u'shooting closest zombie'
                action = 'attack'
                target = self.target_to_kill
            else:
                self.status = u'walking'
                action = 'move'
                if self.target_to_kill:
                    target = self.move_rigth_angle(self.target_to_kill.position, self.position)
                    print(target)

        elif (self.rules == 'evacuation'):
            pass
        elif (self.rules == 'safehouse'):
            pass
        else:
            print('Objetivo invalido')

        print(action)
        print(target)
        print(type(target))
        return action, target

    def set_target_to_kill(self, zombies):
        if ((self.target_to_kill == None) or (self.target_to_kill.life <= 0)):
            self.target_to_kill = closest(self, zombies)

    def move_rigth_angle(self, dest, pos):
        diff = [0,0]
        diff[0] = dest[0] - pos[0]
        diff[1] = dest[1] - pos[1]
        newpos = list(pos)

        if not(diff[0] == 0):
            newpos[0] += (-1 if (diff[0] < 0) else 1)
        else:
            newpos[1] += (-1 if (diff[1] < 0) else 1)
        return tuple(newpos)

def create(rules, objectives=None):
    return Morpheus('morpheus', 'red', weapon=Shotgun(), rules=rules)
