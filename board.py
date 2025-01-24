from typing import List, Tuple, Union
import pygame
from piece import Piece
from player import Player
from constants import *
class Board:
    def __init__(self):
        self.board = [[0 for _ in range(20)] for _ in range(20)]
    

    def any_remaining_moves(self, player: Player) -> bool:
        # yes, check every single piece, position and permutation.
        for piece_name in player.remaining_piece_ids():
            for x in range(20):
                for y in range(20):
                    # only check an empty space.
                    if self.board[y][x] == 0:
                        for rotation in range(4):
                            for flipVer in range(2):
                                for flipHor in range(2):
                                    checkMe = Piece(piece_name, PIECES[piece_name])
                                    checkMe.rotateD(rotation*90)
                                    if flipVer == 1:
                                        checkMe.flipVertical()
                                    if flipHor == 1:
                                        checkMe.flipHorizontal()
                                    if self.is_valid_move(checkMe, x, y, player.id, False):
                                        # exit this loop early since we found a valid move.
                                        print(f"Found move for {player.id} with {checkMe.name} at {x}, {y} with R:{rotation*90}, V:{flipVer}, H:{flipHor}")
                                        return True
        return False

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
        if firstTurn:
            corners = [(0,0), (0, 19), (19, 0), (19, 19)]
            for dy, dx in piece.shape:
                ax = x + dx
                ay = y + dy
                if 0 <= ax < len(self.board) and 0 <= ay < len(self.board):
                # within the boundaries of the board
                    if (ay, ax) in corners:
                        return True
            return False
        
        
        for dy, dx in piece.shape:
            ax = x + dx
            ay = y + dy
            if 0 <= ax < len(self.board) and 0 <= ay < len(self.board):
                if self.board[ay][ax] != 0:
                    return False
            else:
                return False
        
        if self.touching_sides(piece, x, y, playerId):
            return False
        
        if not self.touching_corners(piece, x, y, playerId):
            return False
        

        return True
    
    def touching_corners(self, piece, x, y, playerId):
        for dy, dx in piece.shape:
            vectors = [(-1,-1), (-1,1), (1,-1), (1,1)]
            for vy, vx in vectors:
                if 0 <= (y+dy+vy) < len(self.board) and 0 <= (x+dx+vx) < len(self.board):
                    if self.board[y+dy+vy][x+dx+vx] == playerId:
                        return True
        return False


    def touching_sides(self, piece, x, y, playerId):
        for dy, dx in piece.shape:
            ax = x + dx
            ay = y + dy
            vectors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            if 0 <= ax < len(self.board) and 0 <= ay < len(self.board):
                # within the boundaries of the board
                if self.board[ay][ax] != 0:
                    return True
                for vx, vy in vectors:
                    if 0 <= (vx+ax) < len(self.board) and 0 <= (vy+ay) < len(self.board):
                        if self.board[vy+ay][vx+ax] == playerId:
                            return True
        return False