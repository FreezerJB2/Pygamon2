import pygame

import Charge_world
from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    charge_monde = Charge_world
    game.run()