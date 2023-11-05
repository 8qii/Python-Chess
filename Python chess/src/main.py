import pygame
import sys
from const import *
from game import Game
from board import *
from square import Square


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

        self.game = Game()
        self.PLAY_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/start_button.png"),
                                                 (400, 400))
        self.Time = pygame.time.Clock()
        self.BG = pygame.transform.scale(pygame.image.load("assets/images/back.jpg"), (760, 760))

    # màn hình bắt đầu
    def start_screen(self):
        while True:
            self.Time.tick(60)

            self.screen.blit(self.BG, (0, 0))
            # blit play button
            image_width, image_height = self.PLAY_IMAGE.get_size()
            play_rect = pygame.Rect((WIDTH - image_width) // 2, (HEIGHT - image_height) // 2 + 120,
                                    image_width, image_height)
            self.screen.blit(self.PLAY_IMAGE, play_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if play_rect.collidepoint((mouse_x, mouse_y)):
                        pygame.time.wait(200)
                        return
            pygame.display.flip()

    #khởi tạo vòng lặp chính
    def mainloop(self):

        global call_restart
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_piece(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    print(dragger.mouseY, clicked_row)
                    print(dragger.mouseX, clicked_col)

                    # nếu ô được chọn có cờ
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            # lưu lại ô được chọn
                            dragger.save_initial(event.pos)
                            # set quân cờ được chọn
                            dragger.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_piece(screen)


                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_piece(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # mouse release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            game.play_sound(captured)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_piece(screen)

                            game.next_turn()

                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    # press t to change the theme
                    if event.key == pygame.K_t:
                        game.change_theme()
                    # press r to restart
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board

                # quit game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # dòng update này luôn được đặt ở cuối vòng lặp
            pygame.display.update()


main = Main()
main.start_screen()
main.mainloop()
