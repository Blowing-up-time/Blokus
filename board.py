from typing import List, Tuple, Union, Dict 
import pygame
from piece import Piece
from player import Player
from constants import *
import numpy as np



class Board:
    def __init__(self):
        self.board = np.array([[0 for _ in range(20)] for _ in range(20)])
        self.transformations = self.gen_pieces()
        print("D")

    
    def gen_pieces(self) -> Dict[str, List[Piece]]:
        trans_dict = {}
        for piece_name, shapeDef in PIECES.items():
            trans_dict[piece_name] = []
            # generate rotations.
            rotations = [x*90 for x in range(4)] if PIECES[piece_name][1] else [0]
            flips = [(0, 0)]
            # can this piece be flipped?
            if PIECES[piece_name][2]:
                flips = [(0,0), (0, 1), (1,0), (1,1)]
            for rotation in rotations:
                for flipHor, flipVer in flips:
                    p = Piece(piece_name, shapeDef[0])
                    p.rotateD(rotation)
                    if flipHor:
                        p.flipHorizontal()
                    if flipVer:
                        p.flipVertical()
                    trans_dict[piece_name].append(p)
        return trans_dict
                    
    
    def any_remaining_moves(self, player: Player) -> bool:
        # yes, check every single piece, position and permutation.
        for piece_name in player.remaining_piece_ids():
            for x in range(20):
                for y in range(20):
                    if self.board[y][x] != 0:
                        continue
                    for piece in self.transformations[piece_name]:
                        if self.is_valid_move(piece, x, y, player.id, False):
                            print(f"Found move for {player.id} with {piece.name} at {x}, {y}")
                            return True
        return False
    

    # not currently used. will be used later.
    def gen_random_moves(self, player: Player, i=5):

        moves = []
        for piece_name in np.random.permutation(player.remaining_piece_ids()):
            for x in np.random.permutation(20):
                for y in np.random.permutation(20):
                    if self.board[y][x] != 0:
                        continue
                    for piece in self.transformations[piece_name]:
                        if self.is_valid_move(piece, x, y, player.id, False):
                            moves.append((piece, x, y))
            if len(moves) >= i:
                break
        return moves


    def place_piece(self, piece: Piece, x: int, y: int, playerId: int, firstTurn: bool) -> bool:
        """
        Returns true if successfully placed the piece
        """
        if self.is_valid_move(piece, x, y, playerId, firstTurn):
            # place piece

            for dy, dx in piece.shape: 
                self.board[dy+y][dx+x] += playerId
            return True
        return False


    def is_valid_move(self, piece: Piece, x: int, y: int, playerId: int, firstTurn: bool) -> bool:
        # make sure all are zeroes
        # y, x
        cell_coords = piece.shape + [y, x]
        # if any are less than 0 or bigger than the board, exit early.
        if np.any(cell_coords < 0) or np.any(cell_coords >= len(self.board)):
            return False
        # are any cells occupied, exit early.
        if np.any(self.board[cell_coords[:,0], cell_coords[:, 1]] != 0):
            return False
        

        # first turn corner check.
        if firstTurn:
            corners = np.array([(0,0), (0, 19), (19, 0), (19, 19)])
            # all
            if np.isin(cell_coords, corners).all(axis=1).any():
                return True 
            return False


        sides_vectors = np.array([(-1, 0), (1, 0), (0, 1), (0, -1)])
        corners_vectors = np.array([(-1,-1), (-1,1), (1,-1), (1,1)])
        board_length = len(self.board)

        sides_coords = (cell_coords[:, None, :] + sides_vectors).reshape(-1, 2)
        corners_coords = (cell_coords[:, None, :] + corners_vectors).reshape(-1, 2)


        sides_mask = (sides_coords[:, 0] >= 0) & (sides_coords[:, 0] < board_length) &\
                        (sides_coords[:, 1] >= 0) & (sides_coords[:, 1] < board_length)
        corners_mask = (corners_coords[:, 0] >= 0) & (corners_coords[:, 0] < board_length) &\
                        (corners_coords[:, 1] >= 0) & (corners_coords[:, 1] < board_length)
        
        sides_coords = sides_coords[sides_mask]
        corners_coords = corners_coords[corners_mask]



        if np.any(self.board[sides_coords[:, 0], sides_coords[:, 1]] == playerId):
            return False
        
        if np.any(self.board[corners_coords[:, 0], corners_coords[:, 1]] == playerId):
            return True
        else:
            return False
