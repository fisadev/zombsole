# coding: utf-8
from things import Player, Zombie
from utils import closest, distance, adyacent_positions
from weapons import Shotgun


class Terminator(Player):
    '''A player that stays still and shoots zombies.'''
    def next_step(self, things, t):
        zombies = [thing for thing in things.values()
                   if isinstance(thing, Zombie)]

        if zombies:
            target = closest(self, zombies)
            if distance(self, target) > self.weapon.max_range:
                best_move = closest(target, adyacent_positions(self))
                obstacle = things.get(best_move)
                if obstacle:
                    if isinstance(obstacle, Player) and \
                       obstacle.name == 'terminator':
                        # zombie not in range. Terminator blocking path. Heal
                        # it.
                        return 'heal', obstacle
                    else:
                        # zombie not in range. Obstacle in front. Shoot it.
                        self.status = u'shooting obstacle to chase target'
                        return 'attack', obstacle
                else:
                    # zombie not in range. Not obstacle. Move.
                    self.status = u'chasing target'
                    return 'move', best_move
            else:
                # zombie in range. Shoot it.
                self.status = u'shooting target'
                return 'attack', target
        else:
            # no zombies. Heal.
            self.status = u'no targets, healing'
            return 'heal', self


def create(rules, objetives=None):
    return Terminator('terminator', 'cyan', weapon=Shotgun(), rules=rules,
                      objetives=objetives)
