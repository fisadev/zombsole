#coding: utf-8
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
                raise Exception(u'Trying to place %s in a position already occupied by %s.' % (thing.name,
                                                                                               self.things[thing.position].name))

    def event(self, thing, message):
        self.events.append((self.t, thing, message))

    def step(self):
        '''Forward one instant of time.'''
        from zombsole.things import DeadBody  # here to avoid circular import

        self.t += 1
        things = self.things.values()
        random.shuffle(things)
        actions = []

        # for each thing, call its next_step and add its desired action to the
        # queue
        actors = [thing for thing in things if thing.ask_for_actions]
        for thing in actors:
            try:
                next_step = thing.next_step(self.things)
                if next_step is not None:
                    action, parameter = next_step
                    actions.append((thing, action, parameter))
                else:
                    self.event(thing, u'idle')
            except Exception as err:
                self.event(thing, u'error with next_step or its result (%s)' % err.message)
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
                    self.event(thing, u'unknown action "%s"' % action)
            except Exception as err:
                self.event(thing, u'error excuting %s action (%s)' % (action, err.message))
                if self.debug:
                    raise err

        # remove dead things at the end
        for thing in self.things.values():
            if thing.life <= 0:
                if thing.leaves_dead_body:
                    self.things[thing.position] = DeadBody(thing.position, thing.color)
                    self.event(thing, u'died')
                else:
                    del self.things[thing.position]
                    self.event(thing, u'destroyed')

    def thing_move(self, thing, destination):
        if not isinstance(destination, tuple):
            raise Exception(u'Destination of movement should be a tuple')

        obstacle = self.things.get(destination)
        if obstacle is not None:
            event = u'hit %s with his head' % obstacle.name
        elif distance(thing.position, destination) > 1:
            event = u'tried to walk too fast, but physics forbade it'
        else:
            self.things[destination] = thing
            del self.things[thing.position]
            thing.position = destination

            event = u'moved to ' + str(destination)

        return event

    def thing_attack(self, thing, target):
        if not isinstance(target, Thing):
            raise Exception(u'Target of attack should be a thing')

        if distance(thing.position, target.position) > thing.weapon.max_range:
            event = u'tried to attack %s, but it is too far for a %s' % (target.name, thing.weapon.name)
        else:
            damage = random.randint(*thing.weapon.damage_range)
            target.life -= damage
            event = u'injured %s with a %s' % (target.name, thing.weapon.name)

        return event

    def thing_heal(self, thing, target):
        if not isinstance(target, Thing):
            raise Exception(u'Target of healing should be a thing')

        if distance(thing.position, target.position) > HEALING_RANGE:
            event = u'tried to heal %s, but it is too far away' % target.name
        else:
            # heal half max_life, avoiding health overflow
            target.life = min(target.life + target.MAX_LIFE / 2,
                              target.MAX_LIFE)
            event = u'healed ' + target.name

        return event


class Thing(object):
    '''Something in the world.'''
    MAX_LIFE = 1

    def __init__(self, name, icon, color, life, position, ask_for_actions=False, leaves_dead_body=False):
        if len(icon) != 1:
            raise Exception(u'The icon must be a 1 char unicode or string.')

        self.name = name
        self.icon = icon
        self.color = color
        self.life = life
        self.position = position
        self.status = u''
        self.ask_for_actions = ask_for_actions
        self.leaves_dead_body = leaves_dead_body

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
        super(FightingThing, self).__init__(name, icon, color, life, position,
                                            ask_for_actions=True,
                                            leaves_dead_body=True)
        self.weapon = weapon


class ComplexThingBuilder(object):
    def create_parts(self):
        '''
        Create the things that compose this complex thing.
        Should return a list of things.
        '''
        raise NotImplementedError(u'Implement the complex thing parts builder')
