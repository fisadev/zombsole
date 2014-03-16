#coding: utf-8
from zombsole.game import Game
from zombsole.things import Human



def run():
    g = Game(players=[Human('player1', 'blue')],
             size=(80, 20),
             initial_zombies=10)
    g.play()


if __name__ == '__main__':
    run()
