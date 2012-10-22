#coding: utf-8
from zombsole.core import Thing, ComplexThingBuilder


class SolidBox(Thing):
    '''Solid box.'''
    def __init__(self):
        super(SolidBox, self).__init__('#')


class BigSolidBoxBuilder(ComplexThingBuilder):
    '''Big solid box builder.'''
    def __init__(self, size):
        self.size = size

    def create_parts(self, position):
        '''Create parts for a solid box of the given size.'''
        return [(SolidBox(), (x, y))
                for x in range(position[0], position[0] + self.size[0])
                for y in range(position[1], position[1] + self.size[1])]
