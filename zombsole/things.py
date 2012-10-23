#coding: utf-8
import random
from zombsole.core import Thing, FightingThing, ComplexThingBuilder, Weapon


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


class ZombieClaws(Weapon):
    def __init__(self):
        super(ZombieClaws, self).__init__('claws',
                                          1,
                                          random.randint(5, 10))

class Zombie(FightingThing):
    def __init__(self):
        super(Zombie, self).__init__('z',
                                     'green',
                                     random.randint(50, 100),
                                     random.randint(1, 2),
                                     ZombieClaws())
