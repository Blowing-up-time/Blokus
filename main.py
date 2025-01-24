from player import Player
from constants import *
from blokus import Blokus

if __name__ == "__main__":
    pygame.init()
    playerRed = Player(1, RED)
    playerBlue = Player(2, BLUE)
    playerGreen = Player(3, GREEN)
    playerYellow = Player(4, YELLOW)

    #playerList = [playerRed]
    #playerList = [playerRed, playerBlue]
    playerList = [playerRed, playerBlue, playerGreen, playerYellow]

    config = {
        'grid_offset': 20,
        'grid_cellsize': 30,
        'remaining_offset': 20,
        'remaining_overflow': 620,
        'remaining_cellsize': 10,
        'score_offset': (620, 40)
    }

    game = Blokus(playerList, 1200, 800, config)
    game.play()