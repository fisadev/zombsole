# coding: utf-8
import random

from things import *
from utils import *
from core import *
from weapons import *
from decimal import Decimal
from os import system
from time import sleep

HEALTH_LIMIT = 65

class Teamfamaf(Player):
    '''A player that pretends to be a ninja.'''
    def __init__(self, name, color, weapon, status='chilling out', state='grouping', rules=None, objective=None):
        super(Teamfamaf, self).__init__(name, color, weapon=weapon)
        self.rules = rules
        self.objective = objective
        self.status = status
        self.state = state
        self.assigned = None

    def koikoi(self, source, destination, things):
        possible = []
        if distance(source, destination) <= 1:
            self.status = u'standing by'
            return None
        elif self.rules != 'safehouse':
            if source[0] < destination[0]:
                possible.append('r')
            elif source[0] > destination[0]:
                possible.append('l')
            if source[1] < destination[1]:
                possible.append('u')
            elif source[1] > destination[1]:
                possible.append('d')
        else:
            if source[1] < destination[1]:
                possible.append('u')
            elif source[1] > destination[1]:
                possible.append('d')
            if source[0] < destination[0]:
                possible.append('r')
            elif source[0] > destination[0]:
                possible.append('l')

        deltas = {
            'd': (0, -1),
            'u': (0, 1),
            'l': (-1, 0),
            'r': (1, 0),
        }
        delta = deltas[random.choice(possible)]
        tgt = (self.position[0] + delta[0],
               self.position[1] + delta[1])
        if things.get(tgt) is not None:
            adjacents = sort_by_distance(destination, adjacent_positions(self))
            for position in adjacents:
                thing = things.get(position)
                if isinstance(thing, (Box, Wall)) and distance(position, tgt) < distance(self.position, tgt):
                    adj = sort_by_distance(destination, adjacent_positions(thing))
                    posi = (tgt[0] + delta[0],
                            tgt[1] + delta[1])
                    thg = things.get(posi)
                    return 'attack', thing
                elif isinstance(thing, Player):
                    return 'heal', thing
        return 'move', tgt

    def closest_conn_comp(self, my_conn_comp, list_of_others):
        objective = None
        dist = None
        for partner in my_conn_comp:
            for other in list_of_others:
                if objective is None:
                    objective = other
                    dist = distance(partner.position, objective.position)
                elif distance(partner.position, other.position) < dist:
                    objective = other
                    dist = distance(partner.position, objective.position)
        return objective

    def next_step(self, things, t):
        zombies = [thing for thing in things.values() if isinstance(thing, Zombie) and thing.life > 0]
        zombies_in_range = [zombie for zombie in zombies if distance(zombie.position, self.position) <= self.weapon.max_range]
        players = [thing for thing in things.values() if isinstance(thing, Player) and thing is not self]
        players = sort_by_distance(self, players)
        allplayers = [thing for thing in things.values() if isinstance(thing, Player)]
        allplayers = sort_by_distance(self, allplayers)

        # sacar la componente conexa del jugador
        conex = [self]
        for player in players:
            for fixed in conex:
                if distance(fixed.position, player.position) == 1 and player not in conex:
                    conex.append(player)

        if self.rules == "extermination":
            return self.extermination(zombies, zombies_in_range, players, allplayers, conex, things)
        elif self.rules == "safehouse":
            return self.safehouse(zombies, zombies_in_range, players, allplayers, conex, things)
        else:
            return self.evacuation(zombies, zombies_in_range, players, allplayers, conex, things)

    def extermination(self, zombies, zombies_in_range, players, allplayers, conex, things):
        if conex != allplayers:
            if self.state == "grouping" or self.state == "regrouping":
                injured = [player for player in players if player.life <= HEALTH_LIMIT and distance(player.position, self.position) <= HEALING_RANGE]
                if self.life <= HEALTH_LIMIT:
                    self.status = u'healing myself'
                    return 'heal', self
                elif len(conex) > 1 and len(injured):
                    return 'heal', injured[0]
                elif len([zombie for zombie in zombies if distance(self.position, zombie.position) <= self.weapon.max_range]) >= 1:
                    target = closest(self, zombies)
                    self.status = u'shooting closest opponent'
                    return 'attack', target
                else:
                    # correr como nena, con el algoritmo koikoi(c)
                    others = [thing for thing in allplayers if thing not in conex]
                    goal = self.closest_conn_comp(conex, others)
                    if goal is not None:
                        return self.koikoi(self.position, goal.position, things)
            elif self.state == "hunting":
                zombi = (sort_by_distance(self, zombies))[0]
                if distance(self, zombi) <= self.weapon.max_range:
                    self.status = u'attacking zombie'
                    return 'attack', zombi
                else:
                    return self.koikoi(self.position, zombi.position, things)
            else:
                self.status = u'Not grouped and in healing state'
                return None
        else:
            if self.state == "grouping" or self.state == "regrouping":
                self.state = 'hunting'
            injured = [player for player in players if player.life <= HEALTH_LIMIT]
            iir = [player for player in injured if distance(player.position, self.position) <= HEALING_RANGE]
            injured_in_range = sort_by_distance(self, iir)
            if injured_in_range is not None:
                return 'heal', injured_in_range[0]
            else:
                zombi = (sort_by_distance(self, zombies))[0]
                if distance(self, zombi) <= self.weapon.max_range:
                    self.status = u'attacking zombie'
                    return 'attack', zombi
                else:
                    return self.koikoi(self.position, zombi.position, things)

    def safehouse(self, zombies, zombies_in_range, players, allplayers, conex, things):
        if self.assigned is None:
            keep_assigning = True
            while keep_assigning:
                flag = True
                self.assigned = random.choice(self.objective)
                for x in players:
                    if x.assigned == self.assigned:
                        flag = False
                if flag:
                    keep_assigning = False
        if self.position in self.objective and (self.position[0] - 1, self.position[1]) in self.objective:
            return 'move', (self.position[0] - 1, self.position[1])
        elif self.position in self.objective and not ((self.position[0] - 1, self.position[1]) in self.objective):
            target = closest(self, zombies)
            if distance(self, target) <= self.weapon.max_range:
                return 'attack', target
            else:
                cf = closest(self, players)
                return 'heal', cf
        if conex != allplayers:
            if self.state == "grouping" or self.state == "regrouping":
                injured = [player for player in players if player.life <= HEALTH_LIMIT and distance(player.position, self.position) <= HEALING_RANGE]
                if self.life <= HEALTH_LIMIT:
                    self.status = u'healing myself'
                    return 'heal', self
                elif len(conex) > 1 and len(injured):
                    return 'heal', injured[0]
                elif len([zombie for zombie in zombies if distance(self.position, zombie.position) <= self.weapon.max_range]) >= 1:
                    target = closest(self, zombies)
                    self.status = u'shooting closest opponent'
                    return 'attack', target
                else:
                    # correr como nena, con el algoritmo koikoi(c)
                    others = [thing for thing in allplayers if thing not in conex]
                    goal = self.closest_conn_comp(conex, others)
                    if goal is not None:
                        return self.koikoi(self.position, goal.position, things)
            else:
                injured = [player for player in players if player.life <= HEALTH_LIMIT and distance(player.position, self.position) <= HEALING_RANGE]
                if len(conex) > 1 and len(injured):
                    self.status = u'healing ally'
                    return 'heal', injured[0]
                elif self.life <= HEALTH_LIMIT:
                    self.status = u'healing myself'
                    return 'heal', self
                elif len([zombie for zombie in zombies if distance(self.position, zombie.position) <= self.weapon.max_range]) >= 1:
                    target = closest(self, zombies)
                    self.status = u'shooting closest opponent'
                    return 'attack', target
                self.status = u'still going to safehouse'
                return self.koikoi(self.position, self.assigned, things)
        else:
            if len([zombie for zombie in zombies if distance(self.position, zombie.position) <= self.weapon.max_range]) >= 1:
                target = closest(self, zombies)
                self.status = u'shooting closest opponent'
                return 'attack', target
            self.state = 'advancing'
            self.status= u'heading for safe house'
            return self.koikoi(self.position, self.assigned, things)

    def evacuation(self, zombies, zombies_in_range, players, allplayers, conex, things):
        if conex != allplayers:
            if self.state == "grouping" or self.state == "regrouping":
                injured = [player for player in players if player.life <= HEALTH_LIMIT and distance(player.position, self.position) <= HEALING_RANGE]
                if self.life <= HEALTH_LIMIT:
                    self.status = u'healing myself'
                    return 'heal', self
                elif len(conex) > 1 and len(injured):
                    return 'heal', injured[0]
                elif len([zombie for zombie in zombies if distance(self.position, zombie.position) <= self.weapon.max_range]) >= 1 and len([zombie for zombie in zombies if distance(self.position, zombie.position) <= self.weapon.max_range - 2]) <= 3:
                    target = closest(self, zombies)
                    self.status = u'shooting closest opponent'
                    return 'attack', target
                else:
                    # correr como nena, con el algoritmo koikoi(c)
                    others = [thing for thing in allplayers if thing not in conex]
                    goal = self.closest_conn_comp(conex, others)
                    if goal is not None:
                        return self.koikoi(self.position, goal.position, things)


def create(rules, objectives=None):
    weapon = None
    if rules == 'extermination':
        weap = Shotgun()
    else:
        weap = Shotgun()
    return Teamfamaf('teamfamaf', 'blue', weapon=weap, rules=rules, objective=objectives)
