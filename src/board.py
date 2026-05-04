class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def place_piece(self, x, y, player):
        if self.board[y][x] == 0:
            self.board[y][x] = player
            return True
        return False

    def check_win(self, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for step in range(1, 5):
                nx, ny = x + step * dx, y + step * dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == player:
                    count += 1
                else:
                    break
            for step in range(1, 5):
                nx, ny = x - step * dx, y - step * dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def display(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
