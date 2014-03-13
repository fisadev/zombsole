#coding: utf-8
import time
import os
import random

from termcolor import colored

from zombsole.utils import distance


DEFAULT_COLOR = 'white'
HEALING_RANGE = 3


class World(object):
    '''World where to play the game.'''
    def __init__(self, size):
        self.size = size
        self.logs = []
        self.things = {}

    def add_thing(self, thing):
        if isinstance(thing, ComplexThingBuilder):
            map(self.add_thing, thing.create_parts())
        else:
            if self.things.get(thing.position) is None:
                self.things[thing.position] = thing
            else:
                raise Exception('Trying to place %s in a position already occupied by %s.' % (thing.name,
                                                                                              self.things[thing.position].name))

    def draw(self):
        '''Draw the world'''
        os.system('clear')
        empty_thing = Thing('air', ' ', DEFAULT_COLOR, None, None)
        print '\n'.join(''.join(self.things.get((x, y), empty_thing).draw()
                                for x in xrange(self.size[0]))
                        for y in xrange(self.size[1]))

    def step(self):
        '''Forward one instant of time.'''
        things = self.things.items()
        random.shuffle(things)
        actions = []

        for position, thing in things:
            intended_action = thing.next_step(self.things)
            if intended_action:
                actions.append(intended_action)

        for action, parameter in actions:
            method = getattr(self, 'thing_' + action)
            if method:
                method(thing, parameter)

    def thing_move(self, thing, destination):
        obstacle = self.things.get(destination)
        if obstacle is not None:
            result = 'hit %s with his head' % obstacle.name
        else:
            self.things[destination] = thing
            del self.things[thing.position]
            thing.position = destination

            result = 'moved to ' + str(destination)

        return result

    def thing_attack(self, thing, target_position):
        target = self.things.get(target_position)

        if target is None:
            result = 'attacked and missed'
        elif distance(thing.position, target_position) > thing.weapon.max_range:
            result = 'tried to attack %s, but it is too far for a %s' % (target.name, thing.weapon.name)
        else:
            damage = random.randint(thing.weapon.damage_range)
            target.life -= damage
            if target.life <= 0:
                del self.things[target_position]
                result = 'killed %s with a %s' % (target.name, thing.weapon.name)
            else:
                result = 'injured %s with a %s' % (target.name, thing.weapon.name)

        return result

    def thing_heal(self, thing, heal_position):
        target = self.things.get(heal_position)

        if target is None:
            result = 'healed a nearby fly'
        elif distance(thing.position, heal_position) > HEALING_RANGE:
            result = 'tried to heal %s, but it is too far away' % target.name
        else:
            # heal half max_life, avoiding health overflow
            target.life = min(target.life + target.MAX_LIFE / 2,
                              target.MAX_LIFE)
            result = 'healed ' + target.name

        return result

    def play(self, frames_per_second=2.0):
        '''Game main loop.'''
        while True:
            self.step()
            self.draw()
            time.sleep(1.0 / frames_per_second)


class Thing(object):
    '''Something in the world.'''
    MAX_LIFE = 1

    def __init__(self, name, icon, color, life, position):
        self.name = name
        self.icon = icon
        self.color = color
        self.life = life
        self.position = position
        self.status = ''

    def next_step(self, things):
        return None

    def draw(self):
        return colored(self.icon, self.color)


class Weapon(object):
    '''Weapon, capable of doing damage to things.'''
    def __init__(self, name, max_range, damage_range):
        self.name = name
        self.max_range = max_range
        self.damage_range = damage_range


class FightingThing(Thing):
    '''Thing that has a weapon.'''
    def __init__(self, name, icon, color, life, position, weapon):
        super(FightingThing, self).__init__(name, icon, color, life, position)
        self.weapon = weapon


class ComplexThingBuilder(object):
    def create_parts(self, position):
        '''
        Create the things that compose this complex thing.

        Should return a list of tuples, each of one having the thing (part)
        as first element, and the desired position as seccond element.
        '''
        raise NotImplementedError('Implement the complex thing parts builder')
