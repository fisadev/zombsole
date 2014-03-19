# coding: utf-8
from game import Rules
from utils import closest, distance


class EvacuationRules(Rules):
    '''A kind of game where players must get together to be evacuated.

       Team wins when all alive players are at 2 or less distance from another
       alive player, and at least half of the team must survive.
    '''
    def get_alive_players(self):
        return [player for player in self.game.players
                if player.live > 0]

    def alive_players_together(self):
        alive_players = self.get_alive_players()

        for player in alive_players:
            others = [other for other in alive_players
                      if other is not player and other.life > 0]
            closest_other = closest(player, others)
            if distance(player.position, closest_other.position) > 2:
                return False

    def half_team_alive(self):
        alive_players = self.get_alive_players()
        return len(alive_players) >= len(self.game.players) / 2

    def game_ended(self):
        if self.half_team_alive():
            return self.alive_players_together()
        else:
            return True

    def game_won(self):
        if self.half_team_alive():
            return True, u'players got together and were evacuated :)'
        else:
            return False, u'too few survivors to send a rescue helicopter :('


def create(game):
    return EvacuationRules(game)
