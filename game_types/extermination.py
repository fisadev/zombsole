# coding: utf-8
from game import Game
from things import Zombie


class ExterminationGame(Game):
    '''A kind of game where players must exterminate all zombies.

       Team wins when all zombies are dead.
    '''
    def game_ended(self):
        if not self.players_alive():
            return True
        else:
            zombies = [thing for thing in self.world.things.values()
                       if isinstance(thing, Zombie) and thing.life > 0]

            return not zombies


def create(*args, **kwargs):
    return ExterminationGame(*args, **kwargs)
