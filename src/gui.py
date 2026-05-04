import PySimpleGUI as sg
from board import Color, Board
from typing import NamedTuple
from collections import namedtuple

# type Position = tuple[int, int]
class Position(NamedTuple):
    row: int
    col: int

def get_piece_image(color:Color) -> str | None:
    if color == Color.WHITE:
        return '../static/white.png'
    elif color == Color.BLACK:
        return '../static/dark.png'
    elif color == Color.KING:
        return '../static/circle.png'
    else:
        return ""

class GameState:
    def __init__(self):
        self.board = Board(11)
        self.selected_piece: Position | None = None
        self.window: sg.Window | None = None


    def set_tile(self, pos:Position, color:Color):
        piece_image = get_piece_image(color)
        self.window[(pos.row, pos.col)].update("", 
                                  image_filename=piece_image, 
                                  image_size=(50,48),
                                  )
    def get_tile(self, pos:Position) -> Color:
        return self.board.board[pos.row][pos.col]

    def select_piece(self, pos:Position) -> bool:
        if self.get_tile(pos) != Color.EMPTY and self.board.player == self.get_tile(pos):
            self.selected_piece = pos
            return True
        else:
            self.selected_piece = None
            return False
    def select_tile(self, pos:Position) -> bool:
        if self.selected_piece is not None and self.get_tile(pos) == Color.EMPTY:
            # # Example: Move the piece to the new tile (you would add your game logic here)
            # self.set_tile(pos, self.get_tile(self.selected_piece))
            # self.set_tile(self.selected_piece, Color.EMPTY)
            # self.selected_piece = None
            return True
        return False

    def move_piece(self, from_pos:Position, to_pos:Position):
        if self.select_piece(from_pos) and self.select_tile(to_pos):
            # Example: Move the piece to the new tile (you would add your game logic here)
            self.set_tile(to_pos, self.get_tile(from_pos))
            self.set_tile(from_pos, Color.EMPTY)
            self.selected_piece = None
            self.board.player = Color.WHITE if self.board.player == Color.BLACK else Color.BLACK
    def handle_click(self, pos:Position):
        if self.selected_piece is None:
            self.select_piece(pos)
        else:
            if self.select_tile(pos):
                self.move_piece(self.selected_piece, pos)
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
                # Determine color: if (row + col) is even, it's light; if odd, it's dark
                color = light_tile if (row + col) % 2 == 0 else dark_tile
                if (row, col) in [(0,0), (0,10), (10,0), (10,10), (5,5)]:  # Example: Highlight the top-left tile in red
                    color = red_tile
                
                row_layout.append(
                    sg.Button(
                        '', 
                        size=(4, 2), 
                        key=(row, col), 
                        button_color=('white', color),
                        image_filename=get_piece_image(self.board.board[row][col]),
                        image_size=(50,48),
                        pad=(0, 0),
                        border_width=0,
                        auto_size_button=False
                        )
                )
            layout.append(row_layout)
        # Wrap the board in a column and add a 'Close' button
        final_layout = [
            [sg.Text('11x11 Custom Board', font=('Any', 18))],
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

