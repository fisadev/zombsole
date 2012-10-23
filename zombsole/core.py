#coding: utf-8
import time
import os

from termcolor import colored

from zombsole.utils import get_position, distance


DEFAULT_COLOR = 'white'


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
            new_things = [(thing, position), ]

        for new_thing, new_position in new_things:
            if self.thing_in(new_position):
                raise Exception('position occupied!')
            new_thing.position = new_position
            new_thing.world = self
            self.things[new_position] = new_thing

    def move_thing(self, thing, new_position):
        '''Move one thing on the world.'''
        if self.thing_in(new_position):
            raise Exception('position occupied!')

        del self.things[thing.position]
        thing.position = new_position
        self.things[new_position] = thing

    def remove_thing(self, thing):
        '''Removen a thing from the world.'''
        del self.things[thing.position]

    def draw(self):
        '''Draw the world'''
        empty_thing = Thing(' ', DEFAULT_COLOR)
        return '\n'.join(''.join(self.things.get((x, y), empty_thing).draw()
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
    def __init__(self, label, color, life):
        if len(label) != 1:
            raise ValueError('label must be a string of length 1')
        self.label = label
        self.color = color
        self.life = life
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

    def draw(self):
        '''Return the thing bit to add on the draw of the world.'''
        return colored(self.label, self.color)


class MovingThing(Thing):
    '''Something that's able to move by it's own.'''
    def __init__(self, label, color, life, speed):
        super(MovingThing, self).__init__(label, color, life)
        self.speed = speed
        self.moving_to = None
        self.to_do.append(self._move)

    def move(self, objective):
        '''Order thing to move to an objective (thing or position).'''
        self.moving_to = objective
        self.path = []

    def calculate_path(self):
        '''Calculates path to the moving_to objective.'''
        x, y = self.position
        to_position = get_position(self.moving_to)

        self.path = []

        # TODO fix this to avoid collisions
        while (x, y) != to_position:
            if to_position[0] > x:
                x += self.speed
            elif to_position[0] < x:
                x -= self.speed
            elif to_position[1] > y:
                y += self.speed
            elif to_position[1] < y:
                y -= self.speed
            self.path.append((x, y))

    def stop_moving(self):
        '''Order thing to stop moving.'''
        self.moving_to = None

    def _move(self):
        '''Perform movement for time instant.'''
        if self.moving_to:
            if not self.path or self.path[-1] != get_position(self.moving_to):
                self.calculate_path()

            if self.path:
                next_position = self.path.pop(0)
                if self.world.thing_in(next_position):
                    self.path = []
                else:
                    self.world.move_thing(self, next_position)


class Weapon(object):
    '''Weapon, capable of doing damage to things.'''
    def __init__(self, name, max_range, damage):
        self.name = name
        self.max_range = max_range
        self.damage = damage

    def shoot(self, objective):
        '''Shoot the weapon to an objective.'''
        objective.life -= self.damage
        if objective.life <= 0:
            objective.world.remove_thing(objective)


class FightingThing(MovingThing):
    '''Thing that moves and attacks.'''
    def __init__(self, label, color, speed, weapon):
        super(FightingThing, self).__init__(label, color, speed)
        self.weapon = weapon
        self.attacking_to = None
        self.to_do.append(self._attack)

    def attack(self, objective):
        '''Order thing to attack an objective (thing).'''
        self.attacking_to = objective

    def stop_attacking(self):
        '''Order thing to stop attacking.'''
        self.attacking_to = None

    def _attack(self):
        '''Perform movement for time instant.'''
        if self.attacking_to:
            if distance(self, self.attacking_to) <= self.weapon.max_range:
                self.weapon.shoot(self.attacking_to)


class ComplexThingBuilder(object):
    def create_parts(self, position):
        '''
        Create the things that compose this complex thing.

        Should return a list of tuples, each of one having the thing (part)
        as first element, and the desired position as seccond element.
        '''
        raise NotImplementedError('Implement the complex thing parts builder')
