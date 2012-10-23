#coding: utf-8
import random
from zombsole.core import Thing, FightingThing, ComplexThingBuilder, Weapon
from zombsole.utils import closest


class SolidBox(Thing):
    '''Solid box.'''
    def __init__(self):
        super(SolidBox, self).__init__('#', 'grey', 100)


class BigSolidBoxBuilder(ComplexThingBuilder):
    '''Big solid box builder.'''
    def __init__(self, size):
        self.size = size

    def create_parts(self, position):
        '''Create parts for a solid box of the given size.'''
        return [(SolidBox(), (x, y))
                for x in range(position[0], position[0] + self.size[0])
                for y in range(position[1], position[1] + self.size[1])]


def _new_weapon_class(name, max_range, damage_range):
    '''Create new weapon class.'''
    class NewWeapon(Weapon):
        def __init__(self):
            super(NewWeapon, self).__init__(name,
                                            max_range,
                                            damage_range)

    NewWeapon.__name__ = name
    return NewWeapon


ZombieClaws = _new_weapon_class('ZombieClaws', 1, (5, 10))
Gun = _new_weapon_class('Gun', 10, (10, 50))
Shotgun = _new_weapon_class('Shotgun', 6, (50, 150))
Rifle = _new_weapon_class('Rifle', 15, (50, 75))
Knife = _new_weapon_class('Knife', 1, (5, 10))
Sword = _new_weapon_class('Sword', 2, (25, 100))


class Zombie(FightingThing):
    def __init__(self):
        super(Zombie, self).__init__('z',
                                     'green',
                                     random.randint(50, 100),
                                     random.randint(1, 2),
                                     ZombieClaws())


class Survivor(FightingThing):
    def __init__(self, weapon=None):
        if weapon is None:
            weapon = random.choice([Gun, Shotgun, Rifle, Knife, Sword])()
        super(Survivor, self).__init__('s',
                                       'blue',
                                       100,
                                       1,
                                       weapon)
        self.to_do.append(self._think)

    def _think(self):
        '''Think and decide what to do.'''
        zombies = [thing for thing in self.world.things
                   if isinstance(thing, Zombie)]
        closest_zombie = closest(self, zombies)
        self.attack(closest_zombie)
