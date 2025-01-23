import pygame
from typing import Union, List, Tuple
from player import Player
from constants import *
from board import Board
from piece import Piece




    



class Blokus:

    def __init__(self, players: List[Player], width, height, ui_config):
        if not pygame.get_init():
            pygame.init()
        self.ui_config = ui_config
        self.players = players
        self.current_player = 0
        self.display = pygame.display.set_mode((width, height))
        self.display.fill(WHITE)
        self.selected = None
        self.turncount = 0

        self.board = Board()
        self.update_display()


        self.selected_piece = None
    
    def update_display(self):
        pygame.display.flip()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in self.players[self.current_player].pieces:
                    if piece.check_collision(event.pos[0], event.pos[1]):
                        self.selected_piece = piece.name
                        self.selected = Piece(piece.name, piece.shape)
                        #print("Collision")
            if self.selected is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.selected.rotateD(270)
                    elif event.key == pygame.K_d:
                        self.selected.rotateD(90)
                    elif event.key == pygame.K_w:
                        self.selected.flipHorizontal()
                    elif event.key == pygame.K_s:
                        self.selected.flipVertical()
                    

                    if event.key == pygame.K_SPACE:
                        # place piece logic.
                        
                        _x, _y = pygame.mouse.get_pos()
                        x, y = self.snap_xy_to_grid(_x, _y)
                        gridx, gridy = self.to_grid_coords(x, y)
                        # TODO: Add logic for switching players after this.
                        self.board.place_piece(self.selected, gridx, gridy, self.players[self.current_player].id, (self.turncount == 0))
                        self.turncount += 1
                        print("K_SPACE")

    
    def get_player_color(self, id):

        for p in self.players:
            if p.id == id:
                return p.color
        
    def draw_board(self):
        xoffset = yoffset = self.ui_config['grid_offset']
        cellsize = self.ui_config['grid_cellsize']
        for y, row in enumerate(self.board.board):
            for x, col in enumerate(row):
                if self.board.board[y][x] != 0:
                    self.display.fill(self.get_player_color(self.board.board[y][x]), pygame.Rect(
                        (xoffset+(x*cellsize)),
                        (yoffset+(y*cellsize)),
                        cellsize,
                        cellsize
                    ))


    def draw_grid(self):
        xoffset = yoffset = self.ui_config['grid_offset']
        rows = cols = 20
        cellsize = self.ui_config['grid_cellsize']
        linesize = cellsize*rows



        for i in range(rows+1):

            pygame.draw.line(self.display, BLACK, 
                (xoffset, yoffset + i*cellsize),
                (xoffset + linesize, yoffset + i*cellsize)
            )
        for i in range(cols+1):
            pygame.draw.line(self.display, BLACK, 
                (xoffset + i*cellsize, yoffset),
                (xoffset + i*cellsize, yoffset + linesize)
            )

    def draw_remaining(self):
        xoffset = self.ui_config['remaining_overflow']+20
        yoffset = self.ui_config['remaining_offset']
        overflow = self.ui_config['remaining_overflow']
        cellsize = self.ui_config['remaining_cellsize']
        maxX = 0
        for n, player in enumerate(self.players):
            yoffset = self.ui_config['remaining_offset']
            for piece in player.pieces:
                color = player.color if n == self.current_player else GREY
                if piece.name != self.selected_piece:
                    color = color.grayscale()
                #print(piece.shape)
                minY = min([c[0] for c in piece.shape])
                minX = min([c[1] for c in piece.shape])
                maxX = max(maxX, piece.get_piece_bounds()[1])
                piece.draw(self.display, xoffset+abs(minX*cellsize), yoffset+abs(minY*cellsize), cellsize, color)
                yoffset += cellsize//2 + (abs(piece.get_piece_bounds()[0]) * cellsize)
            xoffset += (maxX*cellsize)+cellsize
    

    def play(self):
        while True:
            if self.handle_input():
                break
            self.draw()
    
    
    def to_grid_coords(self, x, y) -> Tuple[int, int]:
        return (x-self.ui_config['grid_offset'])//self.ui_config['grid_cellsize'], (y-self.ui_config['grid_offset'])//self.ui_config['grid_cellsize']
    
    def snap_xy_to_grid(self, x, y) -> Tuple[int, int]:
        gridoffset = self.ui_config['grid_offset']
        cellsize = self.ui_config['grid_cellsize']
        gridsize = (self.ui_config['grid_cellsize']*20)-gridoffset
        minx, maxx, miny, maxy = self.selected.get_piece_sides()
        x = x - gridoffset - cellsize//2
        y = y - gridoffset - cellsize//2


        x = max(0+abs(minx*cellsize), min(gridsize-(maxx*cellsize), x))
        y = max(0+abs(miny*cellsize), min(gridsize-(maxy*cellsize), y))
        x = (round(x / self.ui_config['grid_cellsize']) * self.ui_config['grid_cellsize']) + gridoffset
        y = (round(y / self.ui_config['grid_cellsize']) * self.ui_config['grid_cellsize']) + gridoffset
        
        return x, y
        
    
    def draw_selected(self):
        if self.selected_piece is not None:
            for piece in self.players[self.current_player].pieces:
                if piece.name == self.selected_piece:
                    if self.selected is not None:
                        _x, _y = pygame.mouse.get_pos()
                        x, y = self.snap_xy_to_grid(_x, _y)
                        gridx, gridy = self.to_grid_coords(x, y)
                        pygame.display.set_caption(f"{_x}, {_y} -> {gridx}, {gridy}")
                        self.selected.draw(self.display, x, y, self.ui_config['grid_cellsize'], self.players[self.current_player].color)


            
    def draw(self):
        self.display.fill(WHITE)
        self.draw_selected()
        self.draw_remaining()
        self.draw_board()
        self.draw_grid()
        self.update_display()
