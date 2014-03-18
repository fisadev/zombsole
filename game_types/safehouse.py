# coding: utf-8
from game import Game


class SafeHouseGame(Game):
    '''A kind of game where players must get into a safe house.

       Team wins when all alive players are inside the safe house.
    '''
    def game_ended(self):
        if self.objetives is None:
            raise Exception('Safe house game requires objetives defined.')

        if not self.players_alive():
            return True
        else:
            in_house = [player.position in self.objetives
                        for player in self.players
                        if player.life > 0]
            return all(in_house)


def create(*args, **kwargs):
    return SafeHouseGame(*args, **kwargs)
