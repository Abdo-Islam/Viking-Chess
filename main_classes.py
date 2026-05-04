class Board : 
    def __init__(self): 
        self.board = [['-' for i in range(11)] for j in range(11)]
        for i in range(3, 8):
            self.board[i][0] = 'B'
            self.board[i][10] = 'B'
            self.board[10][i] = 'B'
            self.board[0][i] = 'B'
        self.board[5][1] = 'B'
        self.board[1][5] = 'B'
        self.board[10][1] = 'B'
        self.board[1][10] = 'B'
        for i in range(4, 7):
            for j in range(4, 7): 
                self.board[i][j] = 'W'
        self.board[5][3] = 'W'
        self.board[3][5] = 'W'
        self.board[5][7] = 'W'
        self.board[7][5] = 'W'
        self.board[5][5] = 'K'

    def display(self):
        for i in range(11):
            for j in range(11):
                print(self.board[i][j], end=' ')
            print()
            

    

class player : 
    def __init__(self, color, board): 
        self.color = color 
        self.board = board 

    def win(self): 
        if self.color == 'W': 
            if self.board.board[0][0] == 'K' or self.board.board[0][10] == 'K' or self.board.board[10][0] == 'K' or self.board.board[10][10] == 'K':
                return True
        else:
            i,j = self.find_king(self.board.board)
            if self.is_sandwiched(i, j):
                return True
        return False
            
    def is_sandwiched(self, x, y):
        if self.board.board[x][y] == 'K':
            if (x > 0 and self.board.board[x-1][y] == 'B') or (x == 0):
                if (x < 10 and self.board.board[x+1][y] == 'B') or (x == 10):
                    if (y > 0 and self.board.board[x][y-1] == 'B') or (y == 0):
                        if (y < 10 and self.board.board[x][y+1] == 'B') or (y == 10):
                            return True
        if self.board.board[x][y] == '-':
            return False
        if x > 0 and self.board.board[x-1][y] != '-' and self.board.board[x-1][y] != self.color:
            if x < 10 and self.board.board[x+1][y] != '-' and self.board.board[x+1][y] != self.color:
                return True
        if y > 0 and self.board.board[x][y-1] != '-' and self.board.board[x][y-1] != self.color:
            if y < 10 and self.board.board[x][y+1] != '-' and self.board.board[x][y+1] != self.color:
                return True
        return False

    def find_king(self, board):
        for i in range(11):
            for j in range(11):
                if board[i][j] == 'K':
                    return i,j

                    
    def is_valid_move(self, x1, y1, x2, y2):
        if self.board.board[x1][y1] != self.color:
            return False
        if self.board.board[x2][y2] != '-':
            return False
        if x1 != x2 and y1 != y2:
            return False
        if x1 == x2:
            for i in range(min(y1, y2) + 1, max(y1, y2)):
                if self.board.board[x1][i] != '-':
                    return False
        else:
            for i in range(min(x1, x2) + 1, max(x1, x2)):
                if self.board.board[i][y1] != '-':
                    return False
        if x2 < 0 or x2 > 10 or y2 < 0 or y2 > 10:
            return False
        return True


    def move(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2): 
            self.board.board[x2][y2] = self.color
            self.board.board[x1][y1] = '-'
            return True
        return False