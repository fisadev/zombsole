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
            thing.time(self.t)


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
        self.to_do = []

    def time(self, t):
        '''Forward one instant of time.'''
        self.t = t
        for to_do in self.to_do:
            to_do()


class MovingThing(Thing):
    '''Something that's able to move by it's own.'''
    def __init__(self, position, world, speed):
        super(MovingThing, self).__init__(position, world)
        self.speed = speed
        self.to_do.append(self._move)
        self.moving_to = None

    def move_to(self, objetive):
        '''Order thing to move to a target (thing or position).'''
        self.moving_to = objetive

    def stop_moving(self):
        '''Order thing to stop moving.'''
        self.moving_to = None

    def _move(self):
        '''Perform movement for time instant.'''
        if self.moving_to:
            move_to = self.moving_to
            if isinstance(move_to, Thing):
                move_to = move_to.position
            # TODO move to position in direction to move_to

