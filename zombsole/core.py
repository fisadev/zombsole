#coding: utf-8
import time
import os


class World(object):
    def __init__(self, size):
        self.size = size
        self.terrain = {}
        self.actors = {}

    def thing_at(self, x, y):
        return self.actors.get((x, y)) or \
               self.terrain.get((x, y)) or \
               ' '

    def draw(self):
        os.system('clear')
        print '\n'.join(''.join(self.thing_at(x, y)
                                for x in xrange(self.size[0]))
                        for y in xrange(self.size[1]))

    def t(self):
        pass


def main_loop(world):
    playing = True

    while playing:
        world.t()
        world.draw()
        time.sleep(0.5)
