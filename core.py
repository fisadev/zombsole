# coding: utf-8
import random

from utils import distance


DEFAULT_COLOR = 'white'
HEALING_RANGE = 3


class World(object):
    """World where to play the game."""
    def __init__(self, size, debug=True):
        self.size = size
        self.debug = debug
        self.things = {}
        self.decoration = {}
        self.t = -1
        self.events = []
        self.deaths = 0

    def spawn_thing(self, thing):
        """Add a thing to the world, or to the decoration layer.

           The thing will be spawned into the position it has in its .position
           attribute.
        """
        if thing.is_decoration:
            self.decoration[thing.position] = thing
        else:
            other = self.things.get(thing.position)
            if other is None:
                self.things[thing.position] = thing
            else:
                message = u"Can't place %s in a position occupied by %s."
                raise Exception(message % (thing.name, other.name))

    def spawn_in_random(self, things, possible_positions=None,
                        fail_if_cant=True):
        """Spawn a group of things  in random positions."""
        # if no positions provided, use all the world positions
        if not possible_positions:
            spawns = [(x, y)
                      for x in range(self.size[0])
                      for y in range(self.size[1])]
        else:
            spawns = possible_positions[:]

        # remove occupied positions, and shuffle
        spawns = [spawn for spawn in spawns
                  if self.things.get(spawn) is None]
        random.shuffle(spawns)

        # try  to spawn each thing
        for thing in things:
            if spawns:
                thing.position = spawns.pop()
                self.spawn_thing(thing)
            else:
                if fail_if_cant:
                    error = 'Not enough space to spawn %s' % thing.name
                    raise Exception(error)
                else:
                    return

    def event(self, thing, message):
        """Log an event."""
        self.events.append((self.t, thing, message))

    def step(self):
        """Forward one instant of time."""
        self.t += 1
        actions = self.get_actions()
        random.shuffle(actions)
        self.execute_actions(actions)
        self.clean_dead_things()

    def get_actions(self):
        """For each thing, call its next_step to get its desired action."""
        actions = []
        actors = [thing for thing in self.things.values()
                  if thing.ask_for_actions]
        for thing in actors:
            try:
                next_step = thing.next_step(self.things, self.t)
                if isinstance(next_step, (tuple, list)) and len(next_step) == 2:
                    action, parameter = next_step
                    actions.append((thing, action, parameter))
                elif next_step is None:
                    self.event(thing, u'idle')
                else:
                    event = u'invalid next_step result: %s' % repr(next_step)
                    raise Exception(event)
            except Exception as err:
                self.event(thing, u'error with next_step: %s' % err.message)
                if self.debug:
                    raise

        return actions

    def execute_actions(self, actions):
        """Execute actions, and add their results as events."""
        for thing, action, parameter in actions:
            try:
                # the method which applies the action is something like:
                # self.thing_ACTION(parameter)
                method = getattr(self, 'thing_' + str(action), None)
                if method:
                    event = method(thing, parameter)
                    self.event(thing, event)
                else:
                    self.event(thing, u'unknown action "%s"' % action)
            except Exception as err:
                event = u'error executing %s action: %s' % (action, err.message)
                self.event(thing, event)
                if self.debug:
                    raise

    def clean_dead_things(self):
        """Remove dead things, and add dead decorations."""
        dead_things = [thing for thing in self.things.values()
                       if thing.life <= 0]
        for thing in dead_things:
            if thing.dead_decoration is not None:
                thing.dead_decoration.position = thing.position
                self.spawn_thing(thing.dead_decoration)

            del self.things[thing.position]
            self.event(thing, u'died')
            self.deaths += 1

    def thing_move(self, thing, destination):
        """Apply move action of a thing.

           target: the position to go to.
        """
        if not isinstance(destination, tuple):
            raise Exception(u'Destination of movement should be a tuple or list')

        obstacle = self.things.get(destination)
        if obstacle is not None:
            event = u'hit %s with his head' % obstacle.name
        elif distance(thing.position, destination) > 1:
            event = u'tried to walk too fast, but physics forbade it'
        else:
            # we store position in the things, because they need to know it,
            # but also in our dict, for faster access
            self.things[destination] = thing
            del self.things[thing.position]
            thing.position = destination

            event = u'moved to ' + str(destination)

        return event

    def thing_attack(self, thing, target):
        """Apply attack action of a thing.

           target: the thing to attack.
        """
        if not isinstance(target, Thing):
            raise Exception(u'Target of attack should be a thing')

        if distance(thing.position, target.position) > thing.weapon.max_range:
            event = u'tried to attack %s, but it is too far for a %s'
            event = event % (target.name, thing.weapon.name)
        else:
            damage = random.randint(*thing.weapon.damage_range)
            target.life -= damage
            event = u'injured %s with a %s' % (target.name, thing.weapon.name)

        return event

    def thing_heal(self, thing, target):
        """Apply heal action of a thing.

           target: the thing to heal.
        """
        if not isinstance(target, Thing):
            raise Exception(u'Target of healing should be a thing')

        if distance(thing.position, target.position) > HEALING_RANGE:
            event = u'tried to heal %s, but it is too far away' % target.name
        else:
            # heal avoiding health overflow
            heal = random.randint(target.MAX_LIFE / 10, target.MAX_LIFE / 4)
            target.life = min(target.MAX_LIFE, target.life + heal)
            event = u'healed ' + target.name

        return event


class Thing(object):
    """Something in the world."""
    MAX_LIFE = 1

    def __init__(self, name, icon, icon_basic, color, life, position=None,
                 ask_for_actions=False, dead_decoration=None,
                 is_decoration=False):
        if len(icon) != 1:
            raise Exception(u'The icon must be a 1 char unicode or string.')

        self.name = name
        self.icon = icon
        self.icon_basic = icon_basic
        self.color = color
        self.life = life
        self.position = position
        self.status = u''
        self.ask_for_actions = ask_for_actions
        self.dead_decoration = dead_decoration
        self.is_decoration = is_decoration

    def next_step(self, things, t):
        return None


class Weapon(object):
    """Weapon, capable of doing damage to things."""
    def __init__(self, name, max_range, damage_range):
        self.name = name
        self.max_range = max_range
        self.damage_range = damage_range


class FightingThing(Thing):
    """Thing that has a weapon."""
    def __init__(self, name, icon, icon_basic, color, life, weapon,
                 position=None, dead_decoration=None):
        super(FightingThing, self).__init__(name, icon, icon_basic, color,
                                            life, position,
                                            ask_for_actions=True,
                                            dead_decoration=dead_decoration)

        self.weapon = weapon
