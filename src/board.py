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
        self.board[5][9] =Color.BLACK
        self.board[9][5] =Color.BLACK
        for i in range(4, 7):
            for j in range(4, 7): 
                self.board[i][j] = Color.WHITE
        self.board[5][3] = Color.WHITE
        self.board[3][5] = Color.WHITE
        self.board[5][7] = Color.WHITE
        self.board[7][5] = Color.WHITE
        self.board[5][5] = Color.KING


    def is_corner(self, x, y):
        return (x == 0 and y == 0) or (x == 0 and y == 10) or (x == 10 and y == 0) or (x == 10 and y == 10)
        
    def is_sandwiched(self, x, y):
        if self.board[x][y] == Color.KING:
            if (x > 0 and self.board[x-1][y] == Color.BLACK) or (x == 0) or self.is_corner(x-1, y):
                if (x < 10 and self.board[x+1][y] == Color.BLACK) or (x == 10) or self.is_corner(x+1, y):
                    if (y > 0 and self.board[x][y-1] == Color.BLACK) or (y == 0) or self.is_corner(x, y-1): 
                        if (y < 10 and self.board[x][y+1] == Color.BLACK) or (y == 10) or self.is_corner(x, y+1):
                            return True
        if self.board[x][y] == Color.EMPTY:
            return False
        if x > 0 and (self.board[x-1][y] != Color.EMPTY and self.board[x-1][y] != self.player) or self.is_corner(x-1, y):
            if x < 10 and (self.board[x+1][y] != Color.EMPTY and self.board[x+1][y] != self.player) or self.is_corner(x+1, y):
                return True
        if y > 0 and (self.board[x][y-1] != Color.EMPTY and self.board[x][y-1] != self.player) or self.is_corner(x, y-1):
            if y < 10 and (self.board[x][y+1] != Color.EMPTY and self.board[x][y+1] != self.player) or self.is_corner(x, y+1):
                return True
        
        return False

    def find_king(self):
        for i in range(11):
            for j in range(11):
                if self.board[i][j] == Color.KING:
                    return i,j
        return -1,-1

                    
    def is_valid_move(self, x1, y1, x2, y2):
        if self.board[x1][y1] != self.player or (self.board[x1][y1] == Color.KING and self.player != Color.WHITE):
            return False
        if self.board[x2][y2] != Color.EMPTY:
            return False
        if x1 != x2 and y1 != y2:
            return False
        if x1 == x2:
            for i in range(min(y1, y2) + 1, max(y1, y2)):
                if self.board[x1][i] != Color.EMPTY:
                    return False
        else:
            for i in range(min(x1, x2) + 1, max(x1, x2)):
                if self.board[i][y1] != Color.EMPTY:
                    return False
        if x2 < 0 or x2 > 10 or y2 < 0 or y2 > 10:
            return False
        return True


    def move_piece(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2): 
            self.board[x2][y2] = self.player
            self.board[x1][y1] = Color.EMPTY
            if self.is_sandwiched(x2, y2):
                self.board[x2][y2] = Color.EMPTY
            return True
        return False

    def is_win(self): 
        if self.player == Color.WHITE: 
            if self.board[0][0] == Color.KING or self.board[0][10] == Color.KING or self.board[10][0] == Color.KING or self.board[10][10] == Color.KING:
                return True
        else:
            i,j = self.find_king()
            if i,j == -1, -1 or self.is_sandwiched(i, j):
                return True
        return False

    def display(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
