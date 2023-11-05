import pygame

from const import *
from board import *
from dragger import Dragger
from config import Config
from square import Square
from piece import *
import sys



class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.Time = pygame.time.Clock()
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()


    # show methods

    def show_bg(self, surface):

        theme = self.config.theme


        for row in range(ROWS):
            for col in range(COLS):

                color = theme.bg.light if (row + col) % 2 ==0 else theme.bg.dark

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface , color , rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5,5+ row * SQSIZE)
                    surface.blit(lbl , lbl_pos)

                if row == 7:
                    color = theme.bg.dark if (col + row) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20 ,HEIGHT - 20)
                    surface.blit(lbl , lbl_pos)


    def show_piece(self , surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    #hiển thị tất cả quân cờ ngoại trừ quân Dragging
                    if piece is not self.dragger.piece:

                        #reset chess size after dragging
                        piece.set_texture(size = 80)

                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)

                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):

        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:

                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark

                rect = (move.final.col * SQSIZE , move.final.row * SQSIZE , SQSIZE , SQSIZE)

                pygame.draw.rect(surface, color , rect)

    def show_last_move(self, surface):

        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:

                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark

                rect = (pos.col * SQSIZE, pos.row * SQSIZE , SQSIZE , SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)

            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)

            pygame.draw.rect(surface, color, rect, width = 3)

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        has_next_move = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece() and self.board.squares[row][col].piece.color == self.next_player:
                    p = self.board.squares[row][col].piece
                    self.board.calc_moves(p, row, col, bool=True)
                    lp = len(p.moves)
                    p.moves = []
                    if lp != 0:
                        has_next_move = True
                        break

        if not has_next_move:
            self.end_screen()


    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()

    def end_screen(self):
        if self.next_player == 'white':
            BG = pygame.transform.scale(pygame.image.load("assets/images/black_win2.jpg"), (760, 760))
        else:
            BG = pygame.transform.scale(pygame.image.load("assets/images/white_win2.jpg"), (760, 760))

        while True:
            # self.Time.tick(60)

            self.screen.blit(BG, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()