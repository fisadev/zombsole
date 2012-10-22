#coding: utf-8
import time
import os


class World(object):
    '''World where to play the game.'''
    def __init__(self, size):
        self.size = size
        self.t = None
        self.things = {}

    def _check_free_position(self, position):
        if self.things.get(position) is not None:
            raise Exception('two things in the same place!')

    def add_thing(self, thing, position):
        '''Add something to the world.'''
        self._check_free_position(position)
        thing.position = position
        thing.world = self
        self.things[position] = thing

    def move_thing(self, old_position, new_position):
        '''Move one thing on the world.'''
        self._check_free_position(new_position)

        thing = self.things[old_position]
        thing.position = new_position
        self.things[old_position], self.things[new_position] = None, thing


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
        for thing in self.things.values():
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
    def __init__(self, label):
        if len(label) != 1:
            raise ValueError('label must be a string of length 1')
        self.label = label
        self.x, self.y = None, None
        self.world = None
        self.t = None
        self.to_do = []

    def position_get(self):
        return self.x, self.y

    def position_set(self, value):
        self.x, self.y = value

    position = property(position_get, position_set)

    def time(self, t):
        '''Forward one instant of time.'''
        self.t = t
        for to_do in self.to_do:
            to_do()


class MovingThing(Thing):
    '''Something that's able to move by it's own.'''
    def __init__(self, label, speed):
        super(MovingThing, self).__init__(label)
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
            x, y = self.position
            move_to = self.moving_to
            if isinstance(move_to, Thing):
                move_to = move_to.position

            # TODO fix this to avoid obstacles
            if move_to == (x, y):
                self.stop_moving()
            else:
                if move_to[0] > x:
                    x += self.speed
                elif move_to[0] < x:
                    x -= self.speed
                elif move_to[1] > y:
                    y += self.speed
                elif move_to[1] < y:
                    y -= self.speed
                self.world.move_thing(self.position, (x, y))

