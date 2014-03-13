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
    def __init__(self, size, debug=True):
        self.size = size
        self.debug = debug

        self.things = {}
        self.t = -1
        self.events = []

    def add_thing(self, thing):
        if isinstance(thing, ComplexThingBuilder):
            map(self.add_thing, thing.create_parts())
        else:
            if self.things.get(thing.position) is None:
                self.things[thing.position] = thing
            else:
                raise Exception('Trying to place %s in a position already occupied by %s.' % (thing.name,
                                                                                              self.things[thing.position].name))

    def event(self, thing, message):
        self.events.append((self.t, thing, message))

    def draw(self):
        '''Draw the world'''
        os.system('clear')
        empty_thing = Thing('air', ' ', DEFAULT_COLOR, None, None, False, False)

        # print the world
        print '\n'.join(''.join(self.things.get((x, y), empty_thing).draw()
                                for x in xrange(self.size[0]))
                        for y in xrange(self.size[1]))

        # print player stats
        stats_things = [thing for thing in self.things.values()
                        if thing.show_in_stats]
        stats_things = sorted(stats_things, key=lambda x: x.name)
        for thing in stats_things:
            try:
                weapon_name = thing.weapon.name
            except:
                weapon_name = 'unarmed'

            life_chars_count = int((10.0 / thing.MAX_LIFE) * thing.life)
            life_chars = '[%s%s]' % (life_chars_count * '*', (10 - life_chars_count) * ' ')

            print colored('%s - %s: %s %i' % (thing.name, weapon_name, life_chars, thing.life),
                          thing.color)

        # print events for debugging
        if self.debug:
            print '\n'.join([colored('%s: %s'% (thing.name, event), thing.color)
                            for t, thing, event in self.events
                            if t == self.t])

    def step(self):
        '''Forward one instant of time.'''
        self.t += 1
        things = self.things.values()
        random.shuffle(things)
        actions = []

        # for each thing, call its next_step and add its desired action to the
        # queue
        actors = [thing for thing in things if thing.ask_for_actions]
        for thing in actors:
            try:
                next_step = thing.next_step(self.things.values())
                if next_step is not None:
                    action, parameter = next_step
                    actions.append((thing, action, parameter))
                else:
                    self.event(thing, 'idle')
            except Exception as err:
                self.event(thing, 'error with next_step or its result (%s)' % err.message)
                if self.debug:
                    raise err

        # execute the actions on the queue, and add their results as events
        for thing, action, parameter in actions:
            try:
                method = getattr(self, 'thing_' + action, None)
                if method:
                    event = method(thing, parameter)
                    self.event(thing, event)
                else:
                    self.event(thing, 'unknown action "%s"' % action)
            except Exception as err:
                self.event(thing, 'error excuting %s action (%s)' % (action, err.message))
                if self.debug:
                    raise err

        # remove dead things at the end
        for thing in self.things.values():
            if thing.life <= 0:
                del self.things[thing.position]
                self.event(thing, 'died')

    def thing_move(self, thing, destination):
        if not isinstance(destination, tuple):
            raise Exception('Destination of movement should be a tuple')

        obstacle = self.things.get(destination)
        if obstacle is not None:
            event = 'hit %s with his head' % obstacle.name
        elif distance(thing.position, destination) > 1:
            event = 'tried to walk too fast, but physics forbade it'
        else:
            self.things[destination] = thing
            del self.things[thing.position]
            thing.position = destination

            event = 'moved to ' + str(destination)

        return event

    def thing_attack(self, thing, target):
        if not isinstance(target, Thing):
            raise Exception('Target of attack should be a thing')

        if distance(thing.position, target.position) > thing.weapon.max_range:
            event = 'tried to attack %s, but it is too far for a %s' % (target.name, thing.weapon.name)
        else:
            damage = random.randint(*thing.weapon.damage_range)
            target.life -= damage
            event = 'injured %s with a %s' % (target.name, thing.weapon.name)

        return event

    def thing_heal(self, thing, target):
        if not isinstance(target, Thing):
            raise Exception('Target of healing should be a thing')

        if distance(thing.position, target.position) > HEALING_RANGE:
            event = 'tried to heal %s, but it is too far away' % target.name
        else:
            # heal half max_life, avoiding health overflow
            target.life = min(target.life + target.MAX_LIFE / 2,
                              target.MAX_LIFE)
            event = 'healed ' + target.name

        return event

    def play(self, frames_per_second=2.0):
        '''Game main loop.'''
        while True:
            self.step()
            self.draw()
            if self.debug:
                raw_input()
            else:
                time.sleep(1.0 / frames_per_second)


class Thing(object):
    '''Something in the world.'''
    MAX_LIFE = 1

    def __init__(self, name, icon, color, life, position, ask_for_actions, show_in_stats):
        self.name = name
        self.icon = icon
        self.color = color
        self.life = life
        self.position = position
        self.status = ''
        self.ask_for_actions = ask_for_actions
        self.show_in_stats = show_in_stats

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
    def __init__(self, name, icon, color, life, position, weapon, show_in_stats):
        super(FightingThing, self).__init__(name, icon, color, life, position, True, show_in_stats)
        self.weapon = weapon


class ComplexThingBuilder(object):
    def create_parts(self):
        '''
        Create the things that compose this complex thing.
        Should return a list of things.
        '''
        raise NotImplementedError('Implement the complex thing parts builder')
