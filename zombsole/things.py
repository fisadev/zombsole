#coding: utf-8
import random

from zombsole.core import Thing, FightingThing
from zombsole.utils import closest, distance, possible_moves
from zombsole.weapons import ZombieClaws, Knife, Axe, Gun, Rifle, Shotgun


class Box(Thing):
    '''Solid box.'''
    MAX_LIFE = 10
    ICON = u'\u25A4'

    def __init__(self, position):
        super(Box, self).__init__(u'box', Box.ICON, 'yellow',
                                  Box.MAX_LIFE,
                                  position)


class DeadBody(Thing):
    '''Dead body.'''
    MAX_LIFE = 50
    ICON = u'\u2620'

    def __init__(self, name, color, position):
        super(DeadBody, self).__init__(name, DeadBody.ICON, color,
                                       DeadBody.MAX_LIFE,
                                       position)


class Wall(Thing):
    '''Solid section of wall.'''
    MAX_LIFE = 200
    ICON = u'\u2593'

    def __init__(self, position):
        super(Wall, self).__init__(u'wall', Wall.ICON, 'white',
                                   Wall.MAX_LIFE,
                                   position)


class Zombie(FightingThing):
    MAX_LIFE = 100
    ICON = u'\u2A30'

    def __init__(self, position, life=None):
        if life is None:
            life = random.randint(Zombie.MAX_LIFE / 2, Zombie.MAX_LIFE)

        dead_decoration = DeadBody('zombie remains', 'green', None)

        super(Zombie, self).__init__(u'zombie', Zombie.ICON, 'green',
                                     life,
                                     position,
                                     ZombieClaws(),
                                     dead_decoration)

    def next_step(self, things):
        action = None

        humans = [thing for thing in things.values()
                  if isinstance(thing, Human)]
        positions = possible_moves(self.position, things)

        if humans:
            target = closest(self, humans)

            if distance(self.position, target.position) < self.weapon.max_range:
                action = 'attack', target
            else:
                if positions:
                    by_distance = lambda position: distance(target.position,
                                                            position)
                    best_position = sorted(positions, key=by_distance)[0]
                    action = 'move', best_position
        else:
            if positions:
                action = 'move', random.choice(positions)

        return action


class Human(FightingThing):
    MAX_LIFE = 100
    ICON = u'\u2A30'

    def __init__(self, name, color, position, weapon=None):
        if weapon is None:
            weapon = random.choice([Gun, Shotgun, Rifle, Knife, Axe])()

        dead_decoration = DeadBody('dead ' + name, color, None)

        super(Human, self).__init__(name, Human.ICON, color,
                                    Human.MAX_LIFE,
                                    position,
                                    weapon,
                                    dead_decoration)
