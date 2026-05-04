import PySimpleGUI as sg
from board import Color, Board

board = Board(11)

def get_piece_image(color:Color) -> str | None:
    if color == Color.WHITE:
        return '../static/white.png'
    elif color == Color.BLACK:
        return '../static/dark.png'
    elif color == Color.KING:
        return '../static/circle.png'
    else:
        return None

def set_tile(window, row, col, color:Color):
    piece_image = get_piece_image(color)
    window[(row, col)].update("", 
                              image_filename=piece_image, 
                              image_size=(50,48),
                              )

def create_board():
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
                    image_filename=get_piece_image(board.board[row][col]),
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

    window: sg.Window = sg.Window('Chess-style Grid', final_layout, element_justification='center')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break 
        # Example: Show which tile was clicked
        # if isinstance(event, tuple):
        #     print(f"You clicked row {event[0]}, column {event[1]}")
        if isinstance(event, tuple):
            set_tile(window, event[0], event[1], Color.BLACK) # Example: Place a knight on the clicked tile

    window.close()

if __name__ == '__main__':
    create_board()
