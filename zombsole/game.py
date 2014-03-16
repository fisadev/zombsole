#coding: utf-8
import os
import time

from termcolor import colored

from zombsole.core import World


class Game(object):
    def __init__(self, world_size, players, map, debug=False):
        self.world = World(world_size, debug=debug)
        self.players = players
        self.debug = debug

    def play(self, frames_per_second=2.0):
        '''Game main loop.'''
        while True:
            self.world.step()
            self.draw()

            if self.debug:
                raw_input()
            else:
                time.sleep(1.0 / frames_per_second)

            if self.game_ended():
                return

    def game_ended(self):
        return False

    def position_draw(self, position):
        thing = self.world.things.get(position)
        decoration = self.world.decoration.get(position)

        if thing is not None:
            return thing.draw()
        elif decoration is not None:
            return decoration.draw()
        else:
            return u' '

    def draw(self):
        '''Draw the world'''
        os.system('clear')

        # print the world
        print '\n'.join(u''.join(self.position_draw((x, y))
                                 for x in xrange(self.world.size[0]))
                        for y in xrange(self.world.size[1]))

        # print player stats
        players = sorted(self.players, key=lambda x: x.name)
        for player in players:
            try:
                weapon_name = player.weapon.name
            except:
                weapon_name = u'unarmed'

            if player.life > 0:
                life_chars_count = int((10.0 / player.MAX_LIFE) * player.life)
                life = u'\u2665 %s%s %i' % (life_chars_count * u'\u2588',
                                            (10 - life_chars_count) * u'\u2591',
                                            player.life)
            else:
                life = u'\u2620 dead'

            print colored(u'%s - %s: %s' % (player.name, weapon_name, life),
                          player.color)

        # print events for debugging
        if self.debug:
            print u'\n'.join([colored(u'%s: %s' % (thing.name, event),
                                      thing.color)
                              for t, thing, event in self.world.events
                              if t == self.world.t])
