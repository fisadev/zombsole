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
        self.t = -1

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
        self.t += 1

        things = self.things.values()
        random.shuffle(things)
        actions = []
        events = []

        for thing in things:
            next_step = thing.next_step(self.things)
            if next_step is not None:
                action, parameter = next_step
                actions.append((thing, action, parameter))

        for thing, action, parameter in actions:
            method = getattr(self, 'thing_' + action)
            if method:
                event = method(thing, parameter)
                events.append((self.t, event))

        return events

    def thing_move(self, thing, destination):
        obstacle = self.things.get(destination)
        if obstacle is not None:
            event = 'hit %s with his head' % obstacle.name
        else:
            self.things[destination] = thing
            del self.things[thing.position]
            thing.position = destination

            event = 'moved to ' + str(destination)

        return event

    def thing_attack(self, thing, target_position):
        target = self.things.get(target_position)

        if target is None:
            event = 'attacked and missed'
        elif distance(thing.position, target_position) > thing.weapon.max_range:
            event = 'tried to attack %s, but it is too far for a %s' % (target.name, thing.weapon.name)
        else:
            damage = random.randint(thing.weapon.damage_range)
            target.life -= damage
            if target.life <= 0:
                del self.things[target_position]
                event = 'killed %s with a %s' % (target.name, thing.weapon.name)
            else:
                event = 'injured %s with a %s' % (target.name, thing.weapon.name)

        return event

    def thing_heal(self, thing, heal_position):
        target = self.things.get(heal_position)

        if target is None:
            event = 'healed a nearby fly'
        elif distance(thing.position, heal_position) > HEALING_RANGE:
            event = 'tried to heal %s, but it is too far away' % target.name
        else:
            # heal half max_life, avoiding health overflow
            target.life = min(target.life + target.MAX_LIFE / 2,
                              target.MAX_LIFE)
            event = 'healed ' + target.name

        return event

    def play(self, frames_per_second=2.0):
        '''Game main loop.'''
        self.t = -1
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
    def create_parts(self):
        '''
        Create the things that compose this complex thing.
        Should return a list of things.
        '''
        raise NotImplementedError('Implement the complex thing parts builder')
