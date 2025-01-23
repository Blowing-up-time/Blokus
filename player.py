from typing import List, Tuple
import pygame
from piece import Piece
from constants import *

class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.pieces: List[Piece] = []

        for name, shape in PIECES.items():
            self.pieces.append(Piece(name, shape))
    
    def remove_piece(self, id):

        for i, piece in enumerate(self.pieces):
            if piece.name == id:
                self.pieces.pop(i)
