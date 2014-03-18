# coding: utf-8
from game import Game
from utils import closest, distance


class EvacuationGame(Game):
    '''A kind of game where players must get together to be evacuated.

       Team wins when all alive players are at 2 or less distance from another
       alive player, and at least half of the team must survive.
    '''
    def game_ended(self):
        alive_players = [player for player in self.players
                         if player.live > 0]
        if len(alive_players) < len(self.players) / 2:
            return True
        else:
            for player in self.players:
                others = [other for other in self.players
                        if other is not player and other.life > 0]
                closest_other = closest(player, others)
                if distance(player.position, closest_other.position) > 2:
                    return False

            return True


def create(*args, **kwargs):
    return EvacuationGame(*args, **kwargs)
