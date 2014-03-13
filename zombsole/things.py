#coding: utf-8
import random
from zombsole.core import Thing, FightingThing, ComplexThingBuilder, Weapon


class SolidBox(Thing):
    '''Solid box.'''
    def __init__(self):
        super(SolidBox, self).__init__('#', 'grey', 100)


class Building(ComplexThingBuilder):
    '''Building builder.'''
    def __init__(self, position, size, doors=2):
        self.position = position
        self.size = size
        self.doors = doors

    def create_parts(self):
        '''Create parts for a building of the given size.'''
        start_x, start_y = self.position
        end_x = start_x + self.size[0]
        end_y = start_y + self.size[1]

        # building walls
        top = [(x, start_y) for x in range(start_x, end_x)]
        bottom = [(x, end_y) for x in range(start_x, end_x)]
        left = [(start_x, y) for y in range(start_y, end_y)]
        right = [(end_x, y) for y in range(start_y, end_y)]

        walls = top + bottom + left + right

        # create doors by removing random wall segments
        random.shuffle(walls)
        walls = walls[self.doors:]


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
Shotgun = _new_weapon_class('Shotgun', 6, (50, 100))
Rifle = _new_weapon_class('Rifle', 15, (25, 75))
Knife = _new_weapon_class('Knife', 1, (5, 10))
Sword = _new_weapon_class('Sword', 2, (75, 100))


class Zombie(FightingThing):
    def __init__(self, position, life=None):
        if life is None:
            life = random.randint(50, 100)
        super(Zombie, self).__init__('zombie', 'z', 'green', life, position, ZombieClaws())


class Human(FightingThing):
    def __init__(self, name, color, position, weapon=None):
        if weapon is None:
            weapon = random.choice([Gun, Shotgun, Rifle, Knife, Sword])()
        super(Human, self).__init__(name, 'h', color, 100, position, weapon)
