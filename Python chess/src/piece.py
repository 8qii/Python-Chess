import os


class Piece:
    # value sử dụng cho đánh giá giá trị quân cờ trong mode AI
    def __init__(self, name , color , value , texture = None , texture_rect = None):
        self.name = name
        self.color = color
        self.moves = []
        self.moved = False
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self, size = 80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )


    # lưu lại các valid moves
    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


# con tốt
class Pawn(Piece):
    def __init__(self, color):
        # xác định hướng di chuyển cho con tốt, dir = 1 thì đi xuống , dir = -1 thì đi lên
        if color == 'white':
            self.dir = -1
        else:
            self.dir = 1

        super().__init__('pawn' , color , 1.0)


# mã
class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

# tịnh
class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.01)

# xe
class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5)


# hậu
class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 10.0)


# vua
class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 1000000.0)

