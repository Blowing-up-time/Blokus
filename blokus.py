import pygame
from typing import Union, List, Tuple
from player import Player
from constants import *
from board import Board
from piece import Piece
import numpy as np
from cProfile import Profile
from pstats import SortKey, Stats



class Blokus:

    """
    
    """

    def __init__(self, players: List[Player], width: int, height: int, ui_config: dict):
        if not pygame.get_init():
            pygame.init()
        
        self.ui_config = ui_config
        self.players = players
        self.current_player = 0
        self.selected = None
        self.selected_name = None
        self.turncount = 0
        self.render = ui_config['render']

        self.board = Board()
        if self.render:
            self.display = pygame.display.set_mode((width, height))
            self.display.fill(WHITE)
            self.update_display()


    
    def update_display(self):
        if self.render:
            pygame.display.flip()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in self.players[self.current_player].pieces:
                    if piece.check_collision(event.pos[0], event.pos[1]):
                        self.selected_name = piece.name
                        self.selected = Piece(piece.name, piece.shape)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSLASH:
                    self.board.any_remaining_moves(self.players[self.current_player])
                elif event.key == pygame.K_RSHIFT:
                    with Profile(timeunit=0.000001) as profile:
                        m = self.board.gen_random_moves(self.players[self.current_player])
                        Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()
                        print(m)

                if self.selected is not None:
                    if event.key == pygame.K_a:
                        self.selected.rotateD(270)
                    elif event.key == pygame.K_d:
                        self.selected.rotateD(90)
                    elif event.key == pygame.K_w:
                        self.selected.flipHorizontal()
                    elif event.key == pygame.K_s:
                        self.selected.flipVertical()
                    

                    if event.key == pygame.K_SPACE:
                        # if move is successful
                        if self.make_player_move():
                            self.next_player()

    def next_player(self):
        if not self.is_game_over():
            # remove players piece
            # clear currently selected
            # move up players
            # increase the turncount if its gone full circle
            if self.players[self.current_player].game_over:
                self.selected_name = None
                self.selected = None

                self.current_player += 1
                if self.current_player >= len(self.players):
                    self.current_player = 0
                    self.turncount += 1
                return 
            self.players[self.current_player].remove_piece(self.selected_name)
            if not self.board.any_remaining_moves(self.players[self.current_player]):
                self.players[self.current_player].game_over = True
                print(f"Player {self.current_player} is out of moves.")
            if len(self.players[self.current_player].pieces) == 0:
                self.players[self.current_player].game_over = True
                print(f"Player {self.current_player} has no more pieces.")

            self.selected_name = None
            self.selected = None

            self.current_player += 1
            if self.current_player >= len(self.players):
                self.current_player = 0
                self.turncount += 1
            if self.players[self.current_player].game_over:
                self.next_player()
        
            

    def make_player_move(self):
        
        _x, _y = pygame.mouse.get_pos()
        x, y = self.snap_xy_to_grid(_x, _y)
        gridx, gridy = self.to_grid_coords(x, y)

        return self.board.place_piece(self.selected, gridx, gridy, self.players[self.current_player].id, (self.turncount == 0))
        
    
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
                color = (player.color+pygame.Color(127, 127, 127)) if n == self.current_player else GREY
                if piece.name == self.selected_name and player.id == self.players[self.current_player].id:
                    color = player.color
                minY = np.min(piece.shape[:, 0])
                minX = np.min(piece.shape[:, 1])
                maxX = max(maxX, piece.xbounds)
                piece.draw(self.display, xoffset+abs(minX*cellsize), yoffset+abs(minY*cellsize), cellsize, color)
                yoffset += cellsize//2 + (abs(piece.ybounds) * cellsize)
            xoffset += (maxX*cellsize)+cellsize
    
    def is_game_over(self):
        return all([player.game_over for player in self.players])
    
    def play(self):
        while not self.is_game_over():
            if self.handle_input():
                break
            self.draw()
        
        for player in sorted(self.players, key=lambda x:x.calculate_score()):
            print(f"Player {player.id} with {player.calculate_score()}")
        


    
    
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
        if self.selected_name is not None:
            for piece in self.players[self.current_player].pieces:
                if piece.name == self.selected_name:
                    if self.selected is not None:
                        _x, _y = pygame.mouse.get_pos()
                        x, y = self.snap_xy_to_grid(_x, _y)
                        gridx, gridy = self.to_grid_coords(x, y)
                        pygame.display.set_caption(f"{_x}, {_y} -> {gridx}, {gridy}")
                        self.selected.draw(self.display, x, y, self.ui_config['grid_cellsize'], self.players[self.current_player].color)
    
    def draw(self):
        if self.render:
            self.display.fill(WHITE)
            pygame.display.set_caption(f"CURRENT TURN: Player {self.current_player}")
            self.draw_selected()
            self.draw_remaining()
            self.draw_board()
            self.draw_grid()
            self.update_display()
