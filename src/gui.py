import PySimpleGUI as sg
from board import Color, Board
from typing import NamedTuple
from collections import namedtuple

# type Position = tuple[int, int]
class Position(NamedTuple):
    row: int
    col: int
    def __repr__(self):
        return f"({self.row}, {self.col})"
def get_tile_color(pos:Position) -> str:
    dark_tile = '#769656'  # Classic chess green
    light_tile = '#eeeed2' # Classic chess cream
    red_tile = '#ff4440' # Classic chess cream
    if (pos.row, pos.col) in [(0,0), (0,10), (10,0), (10,10), (5,5)]:
        return red_tile
    elif (pos.row + pos.col) % 2 == 0:
        return light_tile
    else:
        return dark_tile

def get_piece_image(color:Color) -> str | None:
    if color == Color.WHITE:
        return '../static/defend.png'
    elif color == Color.BLACK:
        return '../static/attacker.png'
    elif color == Color.KING:
        return '../static/king.png'
    else:
        return "../static/empty.png"

class GameState:
    def __init__(self):
        self.board = Board(11)
        self.selected_piece: Position | None = None
        self.window: sg.Window | None = None
        self.__valid_moves: list[Position] = []

    def __get_valid_moves(self, pos:Position) -> list[Position]: # valid moves like rook
        valid_moves = []
        new_row, new_col = pos.row, pos.col
        # Check horizontal and vertical directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = pos.row + dr, pos.col + dc
            while 0 <= new_row < self.board.size and 0 <= new_col < self.board.size:
                if self.board.board[new_row][new_col] == Color.EMPTY:
                    valid_moves.append(Position(new_row, new_col))
                    new_row += dr
                    new_col += dc
                else:
                    break
        if pos in valid_moves:
            valid_moves.remove(pos)
        self.__valid_moves = valid_moves
        return valid_moves

    def highlight_valid_moves(self, pos:Position):
        self.__get_valid_moves(pos)
        for move in self.__valid_moves:
            self.window[(move.row, move.col)].update("",  image_filename=f"../static/{'dark' if self.board.player == Color.BLACK else 'white'}.png", image_size=(50,50))
    def unhighlight_valid_moves(self):
        for move in self.__valid_moves:
            self.window[(move.row, move.col)].update("", button_color=('white', get_tile_color(move)), image_filename=get_piece_image(Color.EMPTY), image_size=(50,50))
        self.__valid_moves = []

    def set_tile(self, pos:Position, color:Color):
        piece_image = get_piece_image(color)
        self.window[(pos.row, pos.col)].update("", 
                                  image_filename=piece_image, 
                                  image_size=(50,50),
                                  )
    def get_tile(self, pos:Position) -> Color:
        return self.board.board[pos.row][pos.col]

    def is_valid_selection(self, pos:Position) -> bool:
        if self.board.player == Color.WHITE and (self.board.board[pos.row][pos.col] == Color.WHITE or self.board.board[pos.row][pos.col] == Color.KING):
            return True
        elif self.board.player == Color.BLACK and self.board.board[pos.row][pos.col] == Color.BLACK:
            return True
        return False

    def select_piece(self, pos:Position) -> bool:
        print(f"Selected piece at {pos} with color {self.get_tile(pos)} current player {self.board.player}")
        if self.is_valid_selection(pos):
            self.selected_piece = pos
            self.window[(pos.row, pos.col)].update("", button_color=('white', 'yellow'))
            self.highlight_valid_moves(pos)
            return True
        else:
            self.selected_piece = None
            return False
    def unselect_piece(self):
        print(f"Unselected piece at {self.selected_piece}")
        if self.selected_piece is not None:
            (row, col) = self.selected_piece
            self.window[(row,col)].update("", button_color=('white', get_tile_color(self.selected_piece)))
            self.selected_piece = None
            self.unhighlight_valid_moves()
    def select_tile(self, pos:Position) -> bool:
        print(f"Selected tile at {pos} with color {self.get_tile(pos)} current player {self.board.player}")
        if self.selected_piece is not None and self.get_tile(pos) == Color.EMPTY:
            # # Example: Move the piece to the new tile (you would add your game logic here)
            # self.set_tile(pos, self.get_tile(self.selected_piece))
            # self.set_tile(self.selected_piece, Color.EMPTY)
            # self.selected_piece = None
            return True
        return False
    def set_turn_text(self, text:str):
        self.window['turn'].update(text)
    def move_piece(self, from_pos:Position, to_pos:Position):
        # if self.select_piece(from_pos) and self.select_tile(to_pos):
            # Example: Move the piece to the new tile (you would add your game logic here)
            if not self.board.is_valid_move(from_pos.row, from_pos.col, to_pos.row, to_pos.col):
                print(f"Invalid move from {from_pos} to {to_pos}")
                self.unselect_piece()
                return
            self.unhighlight_valid_moves()
            print(f"Moving piece from {from_pos} to {to_pos}")
                # raise ValueError("Invalid move")
            self.set_tile(to_pos, self.get_tile(from_pos))
            self.set_tile(from_pos, Color.EMPTY)
            self.board.move_piece(from_pos.row, from_pos.col, to_pos.row, to_pos.col)
            self.board.player = Color.WHITE if self.board.player == Color.BLACK else Color.BLACK
            self.set_turn_text(f'Turn: {"Black" if self.board.player == Color.BLACK else "White"}')
            self.unselect_piece()
    def handle_click(self, pos:Position):
        if self.selected_piece is None:
            self.select_piece(pos)
        elif self.selected_piece == pos:
            self.unselect_piece()
        elif self.get_tile(pos) != Color.EMPTY and self.board.player == self.get_tile(pos):
            self.unselect_piece()
            self.select_piece(pos)
        else:
            if self.select_tile(pos):
                self.move_piece(self.selected_piece, pos)
                if self.board.is_win() and False:
                    sg.popup(f"{'Black' if self.board.player == Color.WHITE else 'White'} wins!")
                    self.set_turn_text(f"{'Black' if self.board.player == Color.WHITE else 'White'} wins!")
            self.selected_piece = None

    def create_board(self) -> sg.Window:
        # Configuration
        board_size = 11
        dark_tile = '#769656'  # Classic chess green
        light_tile = '#eeeed2' # Classic chess cream
        red_tile = '#ff4440' # Classic chess cream
        
        layout = []
        
        for row in range(board_size):
            row_layout = []
            for col in range(board_size):
                row_layout.append(
                    sg.Button(
                        '', 
                        size=(4, 2), 
                        key=(row, col), 
                        button_color=('white', get_tile_color(Position(row, col))),
                        image_filename=get_piece_image(self.board.board[row][col]),
                        image_size=(50,50),
                        pad=(0, 0),
                        border_width=0,
                        auto_size_button=False
                        )
                )
            layout.append(row_layout)
        # Wrap the board in a column and add a 'Close' button
        final_layout = [
            [sg.Text('11x11 Custom Board', font=('Any', 18))],
            [sg.Text('Turn: Black', font=('Any', 14), key='turn')],
            [sg.Column(layout, pad=(10, 10))],
            [sg.Button('Exit', size=(10, 1))]
        ]

        self.window: sg.Window = sg.Window('Chess-style Grid', final_layout, element_justification='center')
        return self.window

if __name__ == '__main__':
    game = GameState()
    window = game.create_board()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break 
        # Example: Show which tile was clicked
        # if isinstance(event, tuple):
        #     print(f"You clicked row {event[0]}, column {event[1]}")
        if isinstance(event, tuple):
            # game.set_tile(Position(event[0], event[1]), Color.BLACK) # Example: Place a knight on the clicked tile
            game.handle_click(Position(event[0], event[1]))

    window.close()

