from typing import List, Tuple
import pygame
from constants import *
import numpy as np
class Piece:
    def __init__(self, name, shapeDef):
        self.name = name
        self.shape = np.array(shapeDef)
        self.rects = []
        self.xbounds = 0
        self.ybounds = 0
        self.recalculate_piece_bounds()
        self.rotation = 0
        self.flipped_hor = False
        self.flipped_ver = False
    
    def draw(self, display: pygame.Surface, x, y, cellsize, color):
        rects = []  
        for cell in self.shape:
            cell_rect = pygame.Rect(
                x + cell[1] * cellsize,
                y + cell[0] * cellsize,
                cellsize,
                cellsize
            )
            rects.append(display. fill(color, cell_rect))
        self.rects = rects
    

    def check_collision(self, x, y):
        for r in self.rects:
            if r.collidepoint(x, y):
                return True
        return False
    
    def recalculate_piece_bounds(self):

        self.xbounds = abs(np.max(self.shape[:,1]) - np.min(self.shape[:,1])) + 1
        self.ybounds = abs(np.max(self.shape[:,0]) - np.min(self.shape[:,0])) + 1
    
    def rotateD(self, deg):
        if deg == 90:
            self.shape = np.column_stack((self.shape[:, 1], -self.shape[:, 0]))
        elif deg == 180:
            self.shape = np.column_stack((-self.shape[:, 0], -self.shape[:, 1]))
        elif deg == 270:
            self.shape = np.column_stack((-self.shape[:, 1], self.shape[:, 0]))
        elif deg == 0 or deg == 360:
            pass
        else:
            raise Exception(f"Tried to rotate the piece by {deg}. This is shit try again.")
        self.rotation = (self.rotation+deg) % 360
        self.recalculate_piece_bounds()
    
    def flipVertical(self):
        self.shape = np.column_stack((-self.shape[:, 0], self.shape[:, 1]))
        self.flipped_ver = not self.flipped_ver
        self.recalculate_piece_bounds()

    def flipHorizontal(self):
        self.shape = np.column_stack((self.shape[:, 0], -self.shape[:, 1]))
        self.flipped_hor = not self.flipped_hor
        self.recalculate_piece_bounds()

    def get_piece_sides(self) -> Tuple[int, int, int, int]: 
        """
        Returns
        -------
        Tuple[int, int, int, int]: minx, maxx, miny, maxy"""
        return np.min(self.shape[:, 1]), np.max(self.shape[:, 1]), np.min(self.shape[:, 0]), np.max(self.shape[:, 0])
    

