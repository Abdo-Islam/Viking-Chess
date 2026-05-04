from enum import Enum
class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    KING  = 3

class Board:
    def __init__(self, size):
        self.size = size
        self.player = Color.BLACK
        self.board : list[list[Color]] = [[Color.EMPTY for _ in range(size)] for _ in range(size)]
        for i in range(3, 8):
            self.board[i][0] = Color.BLACK
            self.board[i][10] =Color.BLACK
            self.board[10][i] =Color.BLACK
            self.board[0][i] = Color.BLACK
        self.board[5][1] = Color.BLACK
        self.board[1][5] = Color.BLACK
        self.board[10][1] =Color.BLACK
        self.board[1][10] =Color.BLACK
        for i in range(4, 7):
            for j in range(4, 7): 
                self.board[i][j] = Color.WHITE
        self.board[5][3] = Color.WHITE
        self.board[3][5] = Color.WHITE
        self.board[5][7] = Color.WHITE
        self.board[7][5] = Color.WHITE
        self.board[5][5] = Color.KING

    def move_piece(self, from_row, from_col, to_row, to_col, color):
        if self.board[from_row][from_col] == color and self.board[to_row][to_col] == Color.EMPTY:
            pass
            self.player = Color.BLACK if self.player == Color.WHITE else Color.WHITE
            return True
        return False
    def is_valid_move(self, from_row, from_col, to_row, to_col, color) -> bool:
        if False:
            return False
        return True
    def check_win(self) -> Color:
        return Color.EMPTY


    def display(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
