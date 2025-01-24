from typing import List, Tuple
import pygame
from piece import Piece
from constants import *

class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.pieces: List[Piece] = []
        self.game_over = False

        for name, shape in PIECES.items():
            self.pieces.append(Piece(name, shape))
        self.starting_score = sum([len(x.shape) for x in self.pieces])
    

    def calculate_score(self):

        return self.starting_score-sum([len(x.shape) for x in self.pieces])
    
    def remaining_piece_ids(self):
        return [p.name for p in self.pieces]
    def remove_piece(self, id):

        for i, piece in enumerate(self.pieces):
            if piece.name == id:
                self.pieces.pop(i)
