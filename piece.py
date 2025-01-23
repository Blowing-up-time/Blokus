from typing import List, Tuple
import pygame

class Piece:
    def __init__(self, name, shape: List[Tuple[int, int]]):
        self.name = name
        self.shape = shape
        self.rects = []
    
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
    
    def get_piece_bounds(self):

        xbounds = abs(max([c[1] for c in self.shape]) - min([c[1] for c in self.shape])) + 1
        ybounds = abs(max([c[0] for c in self.shape]) - min([c[0] for c in self.shape])) + 1
        return ybounds, xbounds
    
    def rotateD(self, deg):
        if deg == 90:
            self.shape = [(x, -y) for y, x in self.shape]
        elif deg == 180:
            self.shape = [(-y, -x) for y, x in self.shape]
        elif deg == 270:
            self.shape = [(-x, y) for y, x in self.shape]
        elif deg == 0 or deg == 360:
            pass
        else:
            raise Exception(f"Tried to rotate the piece by {deg}. This is shit.")
    
    def flipVertical(self):
        self.shape = [(-y, x) for y, x in self.shape]

    def flipHorizontal(self):
        self.shape = [(y, -x) for y, x in self.shape]

    def get_piece_sides(self) -> Tuple[int, int, int, int]: 
        """
        Returns
        -------
        Tuple[int, int, int, int]: minx, maxx, miny, maxy"""
        return min([c[1] for c in self.shape]), max([c[1] for c in self.shape]), min([c[0] for c in self.shape]), max([c[0] for c in self.shape])

