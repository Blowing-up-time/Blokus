from player import Player
from constants import *
from blokus import Blokus

if __name__ == "__main__":
    pygame.init()
    playerRed = Player(1, RED)
    playerBlue = Player(2, BLUE)

    config = {
        'grid_offset': 20,
        'grid_cellsize': 30,
        'remaining_offset': 20,
        'remaining_overflow': 620,
        'remaining_cellsize': 10,
    }

    game = Blokus([playerRed, playerBlue], 800, 800, config)
    game.play()