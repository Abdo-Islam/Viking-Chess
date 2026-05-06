from enum import Enum
from copy import deepcopy

class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    KING  = 3
class Board:
    def __init__(self, size=11):
        self.size = size
        self.player = Color.BLACK  # BLACK (attackers) move first
        self.board : list[list[Color]] = [[Color.EMPTY for _ in range(size)] for _ in range(size)]
        
        # Separate data structures for piece positions
        self.white_pieces: list[tuple[int, int]] = []  # List of (x, y) positions for white pieces (defenders)
        self.black_pieces: list[tuple[int, int]] = []  # List of (x, y) positions for black pieces (attackers)
        self.king_position: tuple[int, int] = (5, 5)   # King position
        self.THRONE = (5, 5) 
        self.CORNERS = [(0, 0), (0, 10), (10, 0), (10, 10)]  # Corner squares
        
        # Setup attackers (BLACK) - 24 pieces around edges
        for i in range(3, 8):
            self.board[i][0] = Color.BLACK
            self.black_pieces.append((i, 0))
            self.board[i][10] = Color.BLACK
            self.black_pieces.append((i, 10))
            self.board[10][i] = Color.BLACK
            self.black_pieces.append((10, i))
            self.board[0][i] = Color.BLACK
            self.black_pieces.append((0, i))
        self.board[5][1] = Color.BLACK
        self.black_pieces.append((5, 1))
        self.board[1][5] = Color.BLACK
        self.black_pieces.append((1, 5))
        self.board[5][9] = Color.BLACK
        self.black_pieces.append((5, 9))
        self.board[9][5] = Color.BLACK
        self.black_pieces.append((9, 5))
        
        # Setup defenders (WHITE) - 12 pieces around king
        for i in range(4, 7):
            for j in range(4, 7): 
                self.board[i][j] = Color.WHITE
                self.white_pieces.append((i, j))
        self.board[5][3] = Color.WHITE
        self.white_pieces.append((5, 3))
        self.board[3][5] = Color.WHITE
        self.white_pieces.append((3, 5))
        self.board[5][7] = Color.WHITE
        self.white_pieces.append((5, 7))
        self.board[7][5] = Color.WHITE
        self.white_pieces.append((7, 5))
        self.board[5][5] = Color.KING
        self.king_position = (5, 5)
        
    def is_corner(self, x, y):
        return (x, y) in self.CORNERS or (x, y) == self.THRONE
    
    def is_escape_square(self, x, y):
        return (x, y) in self.CORNERS 
    
    def enemy_color(self, x, y):
        """Get the enemy color of the piece at position"""
        piece = self.board[x][y]
        if piece == Color.BLACK:
            return Color.WHITE
        elif piece == Color.WHITE or piece == Color.KING:
            return Color.BLACK
        return Color.EMPTY
    
    def is_sandwiched(self, x, y):
        piece = self.board[x][y]
        if piece == Color.EMPTY:
            return False
        if piece == Color.KING:
            return self.is_king_captured()
        enemy = self.enemy_color(x, y)
        left_is_hostile = False
        if self.board[x][y-1] == enemy:
            left_is_hostile = True
        elif self.is_corner(x, y-1) :
            left_is_hostile = True

        right_is_hostile = False
        if self.board[x][y+1] == enemy:
            right_is_hostile = True
        elif self.is_corner(x, y+1) :
            right_is_hostile = True

        if left_is_hostile and right_is_hostile:
            return True

        up_is_hostile = False
        if self.board[x-1][y] == enemy:
            up_is_hostile = True
        elif self.is_corner(x-1, y):
            up_is_hostile = True

        down_is_hostile = False
        if self.board[x+1][y] == enemy:
            down_is_hostile = True
        elif self.is_corner(x+1, y) :
            down_is_hostile = True

        if up_is_hostile and down_is_hostile:
            return True

        return False

    def is_king_captured(self):
        if self.king_position == (-1, -1):
            return True
        x, y = self.king_position
        hostile_sides = 0
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < self.size and 0 <= ny < self.size): 
                hostile_sides += 1
                continue
            if self.is_corner(nx, ny): 
                hostile_sides += 1
                continue
            if self.board[nx][ny] == Color.BLACK: 
                hostile_sides += 1
                continue
            else:
                break;                    
        return hostile_sides >= 4

    def is_valid_move(self, x1, y1, x2, y2):
       
        if not (0 <= x2 < self.size and 0 <= y2 < self.size):
            return False

        piece = self.board[x1][y1]

       
        if self.player == Color.WHITE:
            if piece != Color.WHITE and piece != Color.KING:
                return False
        elif self.player == Color.BLACK:
            if piece != Color.BLACK:
                return False

        
        if self.board[x2][y2] != Color.EMPTY:
            return False

       
        if piece != Color.KING and self.is_corner(x2, y2):
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

        return True
    def move_piece(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2): 
            piece = self.board[x1][y1]
            
            if piece == Color.WHITE and (x1, y1) in self.white_pieces:
                self.white_pieces.remove((x1, y1))
                self.white_pieces.append((x2, y2))
            elif piece == Color.BLACK and (x1, y1) in self.black_pieces:
                self.black_pieces.remove((x1, y1))
                self.black_pieces.append((x2, y2))
            elif piece == Color.KING:
                self.king_position = (x2, y2)
            
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = Color.EMPTY
            
            if self.is_sandwiched(x2, y2):
                if self.board[x2][y2] == Color.WHITE and (x2, y2) in self.white_pieces:
                    self.white_pieces.remove((x2, y2))
                elif self.board[x2][y2] == Color.BLACK and (x2, y2) in self.black_pieces:
                    self.black_pieces.remove((x2, y2))
                self.board[x2][y2] = Color.EMPTY
            
            # check the 4 cells around the moved piece for sandwiching
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x2 + dx, y2 + dy
                if 0 <= nx < 11 and 0 <= ny < 11:
                    if self.is_sandwiched(nx, ny):
                        piece_at = self.board[nx][ny]
                        if piece_at == Color.KING:
                            self.king_position = (-1, -1)
                        elif piece_at == Color.WHITE and (nx, ny) in self.white_pieces:
                            self.white_pieces.remove((nx, ny))
                        elif piece_at == Color.BLACK and (nx, ny) in self.black_pieces:
                            self.black_pieces.remove((nx, ny))
                        self.board[nx][ny] = Color.EMPTY
            return True
        return False
    def is_win(self): 
        if self.player == Color.WHITE: 
            if self.king_position in self.CORNERS:
                return True
        else:
            if self.is_king_captured():
                return True
        return False
    def evaluate(self) -> int:
        black_score = 12-len(self.white_pieces)  # Count white pieces
        white_score = 24-len(self.black_pieces)  # Count black pieces
        
        if self.king_position == (-1, -1):
            black_score += 25
        elif self.king_position in self.CORNERS:
            white_score += 25
        return white_score - black_score
    def get_all_valid_moves(self, player: Color) -> list[tuple[int, int, int, int]]:
        moves = []
        if player == Color.WHITE:
            pieces = self.white_pieces + [self.king_position]
        else:
            pieces = self.black_pieces
        for x, y in pieces:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                while 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == Color.EMPTY:
                        moves.append((x, y, nx, ny))
                        nx += dx
                        ny += dy
                    else:
                        break
        return moves
    def alpha_beta(self, depth: int, alpha: int, beta: int, maximizing: bool=True) -> tuple[int, tuple[int, int, int, int] | None]:
        if depth == 0 or self.is_win():
            score = self.evaluate()
            return (score, None)
        if maximizing:
            max_eval = float('-inf')
            best_move = None
            moves = self.get_all_valid_moves(Color.WHITE)
            if not moves:
                return (self.evaluate(), None)
            for x1, y1, x2, y2 in moves:
                board_copy = deepcopy(self)
                board_copy.move_piece(x1, y1, x2, y2)
                board_copy.player = Color.BLACK
                
                # Recursive call
                eval_score, _ = board_copy.alpha_beta(depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (x1, y1, x2, y2)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        
        else:  # BLACK's turn (minimize)
            min_eval = float('inf')
            best_move = None
            moves = self.get_all_valid_moves(Color.BLACK)
            
            if not moves:  # No valid moves
                return (self.evaluate(), None)
            
            for x1, y1, x2, y2 in moves:
                # Make a copy of the board state
                board_copy = deepcopy(self)
                board_copy.move_piece(x1, y1, x2, y2)
                board_copy.player = Color.WHITE
                
                # Recursive call
                eval_score, _ = board_copy.alpha_beta(depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (x1, y1, x2, y2)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break 
            return (min_eval, best_move)
    def get_best_move(self, max_depth: int = 2) -> tuple[int, int, int, int] | None:
        maximizing = self.player == Color.WHITE
        _, best_move = self.alpha_beta(max_depth, float('-inf'), float('inf'), maximizing)
        return best_move