# coding: utf-8
from zombsole.game import Rules
from zombsole.things import Zombie


class ExterminationRules(Rules):
    """A kind of game where players must exterminate all zombies.

       Team wins when all zombies are dead.
    """
    def zombies_alive(self):
        """Is there any zombie left?"""
        zombies = [thing for thing in self.game.world.things.values()
                   if isinstance(thing, Zombie) and thing.life > 0]
        return bool(zombies)

    def game_ended(self):
        """Has the game ended?"""
        return not self.players_alive() or not self.zombies_alive()

    def game_won(self):
        """Was the game won?"""
        if self.players_alive():
            return True, 'zombies exterminated! :)'
        else:
            return False, 'players exterminated! :('


def create(game):
    return ExterminationRules(game)
