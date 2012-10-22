#coding: utf-8
import time
import os


class World(object):
    '''World where to play the game.'''
    def __init__(self, size):
        self.size = size
        self.terrain = {}
        self.actors = {}

    def thing_at(self, x, y):
        '''Return the thing at the given position.'''
        return self.actors.get((x, y)) or self.terrain.get((x, y))

    def draw(self):
        '''Draw the world'''
        os.system('clear')
        return '\n'.join(''.join(str(self.thing_at(x, y))
                                 for x in xrange(self.size[0]))
                         for y in xrange(self.size[1]))

    def t(self):
        '''Forward one instant of time.'''
        pass


def main_loop(world):
    '''Game main loop.'''
    playing = True

    while playing:
        world.t()
        print world.draw()
        time.sleep(0.5)

