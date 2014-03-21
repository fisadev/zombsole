# coding: utf-8
import random

from core import Thing, FightingThing
from utils import closest, distance, possible_moves
from weapons import ZombieClaws, Knife, Axe, Gun, Rifle, Shotgun


class Box(Thing):
    '''Solid box.'''
    MAX_LIFE = 10
    ICON = u'\u2612'
    ICON_BASIC = u'@'

    def __init__(self, position):
        super(Box, self).__init__(u'box', Box.ICON, Box.ICON_BASIC, 'yellow',
                                  Box.MAX_LIFE, position)


class DeadBody(Thing):
    '''Dead body.'''
    ICON = u'\u2620'
    ICON_BASIC = u'+'

    def __init__(self, name, color, position):
        super(DeadBody, self).__init__(name, DeadBody.ICON,
                                       DeadBody.ICON_BASIC, color, 0, position)


class ObjetiveLocation(Thing):
    '''Objetive location.'''
    ICON = u'\u2591'
    ICON_BASIC = u'*'

    def __init__(self, position):
        super(ObjetiveLocation, self).__init__('objetive',
                                               ObjetiveLocation.ICON,
                                               ObjetiveLocation.ICON_BASIC,
                                               'blue', 0, position)


class Wall(Thing):
    '''Solid section of wall.'''
    MAX_LIFE = 200
    ICON = u'\u2593'
    ICON_BASIC = u'#'

    def __init__(self, position):
        super(Wall, self).__init__(u'wall', Wall.ICON, Wall.ICON_BASIC,
                                   'white', Wall.MAX_LIFE, position)


class Zombie(FightingThing):
    MAX_LIFE = 100
    ICON = u'\u2A30'
    ICON_BASIC = u'x'

    def __init__(self, position=None):
        life = random.randint(Zombie.MAX_LIFE / 2, Zombie.MAX_LIFE)

        dead_decoration = DeadBody('zombie remains', 'green', None)

        super(Zombie, self).__init__(u'zombie', Zombie.ICON, Zombie.ICON_BASIC,
                                     'green', life, ZombieClaws(), position,
                                     dead_decoration)

    def next_step(self, things):
        '''Zombies attack if in range, else move in direction of players.'''
        action = None

        # possible targets for movement and attack
        humans = [thing for thing in things.values()
                  if isinstance(thing, Player)]
        positions = possible_moves(self.position, things)

        if humans:
            # targets available
            target = closest(self, humans)

            if distance(self.position, target.position) < self.weapon.max_range:
                # target in range, attack
                action = 'attack', target
            else:
                # target not in range, _try_ to move
                if positions:
                    by_distance = lambda position: distance(target.position,
                                                            position)
                    best_position = sorted(positions, key=by_distance)[0]
                    action = 'move', best_position
        else:
            # no targets, just wander around
            if positions:
                action = 'move', random.choice(positions)

        return action


class Player(FightingThing):
    MAX_LIFE = 100
    ICON = u'\u2A30'
    ICON_BASIC = u'x'

    def __init__(self, name, color, position=None, weapon=None):
        if weapon is None:
            weapon = random.choice([Gun, Shotgun, Rifle, Knife, Axe])()

        dead_decoration = DeadBody('dead ' + name, color, None)

        super(Player, self).__init__(name, Player.ICON, Player.ICON_BASIC,
                                     color, Player.MAX_LIFE, weapon, position,
                                     dead_decoration)
