# coding: utf-8
from zombsole.game import Rules
from zombsole.utils import adjacent_positions


class EvacuationRules(Rules):
    """A kind of game where players must get together to be evacuated.

       Team wins when all alive players are at 2 or less distance from another
       alive player, and at least half of the team must survive.
    """

    def get_alive_players(self):
        """Get the alive players."""
        return [player for player in self.game.players
                if player.life > 0]

    def alive_players_together(self):
        """Are the alive players together (close to each other)?"""
        alive_players = self.get_alive_players()
        players_by_pos = dict((player.position, player)
                              for player in alive_players)
        together = set()
        pending = [alive_players[0], ]

        while pending:
            player = pending.pop()
            together.add(player)

            neighbors = [players_by_pos[position]
                         for position in adjacent_positions(player)
                         if position in players_by_pos]

            for neighbor in neighbors:
                if neighbor not in together:
                    pending.append(neighbor)

        return len(together) == len(alive_players)

    def half_team_alive(self):
        """At least half of the original team alive?"""
        alive_players = self.get_alive_players()
        return len(alive_players) >= len(self.game.players) / 2.0

    def game_ended(self):
        """Has the game ended?"""
        if self.half_team_alive():
            return self.alive_players_together()
        else:
            return True

    def game_won(self):
        """Was the game won?"""
        if self.half_team_alive():
            return True, u'players got together and were evacuated :)'
        else:
            return False, u'too few survivors to send a rescue helicopter :('


def create(game):
    return EvacuationRules(game)
