# coding: utf-8
from game import Rules


class SafeHouseRules(Rules):
    '''A kind of game where players must get into a safe house.

       Team wins when all alive players are inside the safe house.
    '''
    def alive_players_in_house(self):
        '''Are the alive players in the safe house (objetive locations)?'''
        in_house = [player.position in self.game.objetives
                    for player in self.game.players
                    if player.life > 0]
        return all(in_house)

    def game_ended(self):
        '''Has the game ended?'''
        if self.game.objetives is None:
            raise Exception('Safe house game requires objetives defined.')

        if self.players_alive():
            return self.alive_players_in_house()
        else:
            return True

    def game_won(self):
        '''Was the game won?'''
        if self.players_alive():
            return True, u'everybody made it into the safehouse :)'
        else:
            return False, u'nobody made it into the safehouse :('


def create(game):
    return SafeHouseRules(game)
