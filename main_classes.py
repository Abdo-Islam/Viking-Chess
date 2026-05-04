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
            

    

class player : 
    def __init__(self, color, board): 
        self.color = color 
        self.board = board 

