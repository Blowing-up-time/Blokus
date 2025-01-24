from typing import List, Tuple
import pygame
from piece import Piece

class Board:
    def __init__(self):
        self.board = [[0 for _ in range(20)] for _ in range(20)]
    
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
                if 0 <= ax < len(self.board) or 0 <= ay < len(self.board):
                # within the boundaries of the board
                    if (ay, ax) in corners:
                        return True
            return False
        
        
        for dy, dx in piece.shape:
            ax = x + dx
            ay = y + dy
            if 0 < ax < len(self.board) or 0 < ay < len(self.board):
                if self.board[ay][ax] != 0:
                    print("on top of other shit")
                    return False
        
        if self.touching_sides(piece, x, y, playerId):
            print("touching sides")
            return False
        
        if not self.touching_corners(piece, x, y, playerId):
            print("no corners")
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
            if 0 < ax < len(self.board) or 0 < ay < len(self.board):
                # within the boundaries of the board
                if self.board[ay][ax] != 0:
                    return True
                for vx, vy in vectors:
                    if 0 <= (vx+ax) < len(self.board) and 0 <= (vy+ay) < len(self.board):
                        if self.board[vy+ay][vx+ax] == playerId:
                            return True
        return False