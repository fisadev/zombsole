#coding: utf-8
import time
import os


class World(object):
    '''World where to play the game.'''
    def __init__(self, size):
        self.size = size
        self.things = {}
        self.t = None

    def draw(self):
        '''Draw the world'''
        os.system('clear')
        return '\n'.join(''.join(str(self.things.get((x, y), ' '))
                                 for x in xrange(self.size[0]))
                         for y in xrange(self.size[1]))

    def time(self):
        '''Forward one instant of time.'''
        if self.t is None:
            self.t = -1
        self.t += 1
        for thing in self.things:
            thing.time(t)


def main_loop(world):
    '''Game main loop.'''
    playing = True

    while playing:
        world.time()
        print world.draw()
        time.sleep(0.5)


class Thing(object):
    '''Something in the world.'''
    def __init__(self, position, world, objetive):
        self.position = position
        self.world = world
        self.objetive = objetive
        self.t = None

    def time(self, t):
        '''Forward one instant of time.'''
        self.t = t


class MovingThing(Thing):
    '''Something that's able to move by it's own.'''
    def __init__(self, position, world, speed):
        super(MovingThing, self).__init__(position, world)
        self.speed = speed

