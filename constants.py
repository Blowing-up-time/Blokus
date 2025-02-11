import pygame

# Shape, Rotate, flip

PIECES = {
    # the only single
    'single': [[(0,0)], False, False],
    # the only double
    'double': [[(0,0), (0,1)], True, False],
    # triple pieces

    'triple_line': [[(0,-1), (0,0), (0,1)], True, False],
    'triple_L': [[(0,0), (1,0), (0,1)], True, False],

    # fours
    'four_line': [[(0,-1), (0,0), (0,1), (0,2)], True, False],
    'four_L': [[(0,-1), (0,0), (0,1), (1,1)], True, True],
    'square': [[(0,0), (0,1), (1,0), (1,1)], False, False],
    'four_T': [[(0,-1), (0,0), (1,0), (0,1)], True, False],
    'four_wiggle': [[(0,-1), (0,0), (1,0), (1,1)], True, False],  

    # fives
    'five_line': [[(0,-2), (0,-1), (0,0), (0,1), (0,2)], True, False],
    'five_L': [[(0,-2), (0,-1), (0,0), (0,1), (1,1)], True, True],
    'five_T': [[(0, -1), (0,0), (0, 1), (1, 0), (2,0)], True, False],
    'five_edge': [[(0,0), (1,0), (2,0), (0,1), (0,2)], True, False],
    'five_shovel': [[(1, -1), (1, 0), (0,0), (0, 1), (0, 2)], True, True],
    'five_Z': [[(1, -1), (0, -1), (0,0), (0,1), (-1,1)], True, True],

    'five_D': [[(-1,0), (-1,-1), (0, -1), (0,0), (0,1)], True, True],
    'five_W': [[(-1,-1), (0, -1), (0,0), (1, 0), (1,1)], True, False],
    'five_C': [[(1,-1), (0, -1), (0,0), (0, 1), (1,1)], True, False],
    'wtf': [[(0, -1), (0,0), (1, 0), (0, 1), (-1, 1)], True, True],
    'five_cross': [[(-1, 0), (0, -1), (0,0), (1, 0), (0, 1)], False, False],
    'halberd': [[(0, -2), (0, -1), (0,0), (1, 0), (0, 1)], True, False]
}

# RGBA
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GREY = pygame.Color(128, 128, 128)

