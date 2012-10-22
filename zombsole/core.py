#coding: utf-8
import time
import os


class World(object):
    '''World where to play the game.'''
    def __init__(self, size):
        self.size = size
        self.t = None
        self.things = {}

    def thing_in(self, position):
        '''Get thing in position (or None if nothing there).'''
        return self.things.get(position)

    def add_thing(self, thing, position):
        '''Add something to the world.'''
        if isinstance(thing, ComplexThingBuilder):
            new_things = thing.create_parts(position)
        else:
            new_things = [(thing, position),]

        for new_thing, new_position in new_things:
            if self.thing_in(new_position):
                raise Exception('position occupied!')
            new_thing.position = new_position
            new_thing.world = self
            self.things[new_position] = new_thing

    def move_thing(self, old_position, new_position):
        '''Move one thing on the world.'''
        if self.thing_in(new_position):
            raise Exception('position occupied!')

        thing = self.things[old_position]
        thing.position = new_position
        self.things[new_position] = thing
        del self.things[old_position]

    def draw(self):
        '''Draw the world'''
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
        os.system('clear')
        print world.draw()
        time.sleep(1)


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

    def __str__(self):
        return self.label


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
        self.path = []

        x, y = self.position
        move_to = self.moving_to
        if isinstance(move_to, Thing):
            move_to = move_to.position

        # TODO fix this to avoid obstacles
        while (x, y) != move_to:
            if move_to[0] > x:
                x += self.speed
            elif move_to[0] < x:
                x -= self.speed
            elif move_to[1] > y:
                y += self.speed
            elif move_to[1] < y:
                y -= self.speed
            self.path.append((x, y))

    def stop_moving(self):
        '''Order thing to stop moving.'''
        self.moving_to = None

    def _move(self):
        '''Perform movement for time instant.'''
        if self.moving_to:
            # TODO what if pursuing moving target? recalculate path?
            if self.path:
                next_position = self.path.pop(0)
                if self.world.thing_in(next_position):
                    # TODO find new path? something different?
                    pass
                else:
                    self.world.move_thing(self.position, next_position)
            else:
                # TODO find new path? something different?
                self.stop_moving()


class ComplexThingBuilder(object):
    def create_parts(self, position):
        '''
        Create the things that compose this complex thing.

        Should return a list of tuples, each of one having the thing (part)
        as first element, and the desired position as seccond element.
        '''
        raise NotImplementedError('Implement the complex thing parts builder')
