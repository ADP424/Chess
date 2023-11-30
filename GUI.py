from graphics import *
from chess import *

# the height and width of the window to draw onto
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# the combined border size around the chess board
# (ex. a border size of 100 means 50px borders above, below, left, and right of the board)
WINDOW_BORDERS = 100

# tile colors
EVEN_TILE_COLOR = color_rgb(255, 255, 255)
ODD_TILE_COLOR = color_rgb(75, 10, 10)
HIGHLIGHT_TILE_COLOR = color_rgb(255, 227, 122)

# create the chess window and make the background grey
win = GraphWin("Chess", WINDOW_WIDTH, WINDOW_HEIGHT, False)
win.setBackground(color_rgb(25, 25, 25))

def create_tile_board(chess_board: ChessBoard) -> list:
    """
    Create a board of square tiles for drawing onto the window based on the given chess board.

    Parameters
    ----------
    chess_board : ChessBoard
        The chess board to draw.

    Returns
    -------
    list
        The 2D array of tiles.
    """

    tile_size = min((WINDOW_HEIGHT - WINDOW_BORDERS) / chess_board.board_height, (WINDOW_WIDTH - WINDOW_BORDERS) / chess_board.board_width)

    # create a 2D array of buttons representing tiles on the chess board
    button_board = []
    is_black_tile = False
    y_coord = (WINDOW_HEIGHT - tile_size * chess_board.board_height) / 2

    for i in range(chess_board.board_height):
        x_coord = (WINDOW_WIDTH - tile_size * chess_board.board_width) / 2
        button_board.append([])

        for j in range(chess_board.board_width):
            button_board[i].append(Rectangle(Point(x_coord, y_coord + tile_size), Point(x_coord + tile_size, y_coord)))

            if is_black_tile:
                button_board[i][j].setFill(ODD_TILE_COLOR)
            else:
                button_board[i][j].setFill(EVEN_TILE_COLOR)
            is_black_tile = not is_black_tile

            x_coord += tile_size
        y_coord += tile_size
        is_black_tile = not is_black_tile

    return button_board

def create_piece_board(tile_board: list, chess_board: ChessBoard) -> list:
    """
    Create a board of images of pieces for drawing onto the window based on the given chess board.

    Parameters
    ----------
    tile_board : list
        The 2D array of squares representing the tiles on the chess board.

    chess_board : ChessBoard
        The chess board to draw the pieces from.

    Returns
    -------
    list
        The 2D array of images.
    """

    tile_size = min((WINDOW_HEIGHT - WINDOW_BORDERS) / chess_board.board_height, (WINDOW_WIDTH - WINDOW_BORDERS) / chess_board.board_width)

    # create a 2D array of images representing pieces on the board
    piece_board = []
    for i in range(len(chess_board.board)):
        piece_board.append([])
        for j in range(len(chess_board.board[i])):

            # if the space is empty, draw nothing
            if chess_board.board[i][j].piece == Piece.EMPTY:
                piece_board[i].append(
                Image(Point((tile_board[i][j].getP1().getX() + tile_board[i][j].getP2().getX()) / 2, 
                            (tile_board[i][j].getP1().getY() + tile_board[i][j].getP2().getY()) / 2), 
                            "images/empty.png", int(tile_size), int(tile_size)))
                continue

            img_name = "images/"

            if chess_board.board[i][j].color == Color.BLACK:
                img_name += "black-"
            elif chess_board.board[i][j].color == Color.WHITE:
                img_name += "white-"

            if chess_board.board[i][j].piece == Piece.PAWN:
                img_name += "pawn"
            elif chess_board.board[i][j].piece == Piece.KNIGHT:
                img_name += "knight"
            elif chess_board.board[i][j].piece == Piece.BISHOP:
                img_name += "bishop"
            elif chess_board.board[i][j].piece == Piece.ROOK:
                img_name += "rook"
            elif chess_board.board[i][j].piece == Piece.QUEEN:
                img_name += "queen"
            elif chess_board.board[i][j].piece == Piece.KING:
                img_name += "king"

            img_name += ".png"
            piece_board[i].append(
                Image(Point((tile_board[i][j].getP1().getX() + tile_board[i][j].getP2().getX()) / 2, 
                            (tile_board[i][j].getP1().getY() + tile_board[i][j].getP2().getY()) / 2), 
                            img_name, int(tile_size), int(tile_size)))
            
    return piece_board

def get_clicked_piece_coords(point: Point, chess_board: ChessBoard):
    """ 
    Find the coordinates of the tile that was clicked, based on the tile size.

    Parameters
    ----------
    point : Point
        The mouse point to check the position of.

    chess_board : ChessBoard
        The game object representation of the board holding the tile information.

    Returns
    -------
    tuple
        The row and column of the tile that was clicked, in the form (row, col).

    Notes
    -----
    The row and column values are calculated by taking the point's x and y coordinates, subtracting the window borders, and dividing by the tile size.
    """

    tile_size = min((WINDOW_HEIGHT - WINDOW_BORDERS) / chess_board.board_height, (WINDOW_WIDTH - WINDOW_BORDERS) / chess_board.board_width)
    row = (point.getY() - (WINDOW_HEIGHT - tile_size * chess_board.board_height) / 2) // tile_size
    col = (point.getX() - (WINDOW_WIDTH - tile_size * chess_board.board_width) / 2) // tile_size

    return (int(row), int(col))

def draw_tile_board(tile_board: list):
    """
    Draw the given board of rectangular tiles onto the window.

    Parameters
    ----------
    tile_board : list
        The board of tiles to draw onto the window.
    """

    for row in tile_board:
        for button in row:
            button.draw(win)

def draw_piece_board(piece_board: list):
    """
    Draw the given board of pieces onto the window.

    Parameters
    ----------
    piece_board: list
        The board of pieces to draw on top of the tiles.
    """

    for row in piece_board:
        for piece in row:
            piece.draw(win)

def clear_board_highlights(tile_board: list):
    """
    Set the tiles back to their default color.

    Parameters
    ----------
    tile_board : list
        The board of tiles to reset to their default color.
    """
    tile_is_black = False
    for row in tile_board:
        for button in row:
            if tile_is_black:
                button.setFill(ODD_TILE_COLOR)
            else:
                button.setFill(EVEN_TILE_COLOR)
            tile_is_black = not tile_is_black
        tile_is_black = not tile_is_black

def reset_piece_board(piece_board: list):
    """
    Undraw all pieces on the board.

    Parameters
    ----------
    piece_board : list
        The board of pieces to undraw.
    """

    for row in piece_board:
        for piece in row:
            piece.undraw()

# set up the initial boardstate and draw it into the window
chess_board = ChessBoard()
tile_board = create_tile_board(chess_board)
piece_board = create_piece_board(tile_board, chess_board)
draw_tile_board(tile_board)
draw_piece_board(piece_board)

# loop until the game is over
game_running = True
while game_running:
    
    # get tile the user clicked until it's a piece that has moves
    legal_moves = []
    while len(legal_moves) == 0:
        clicked_point = win.getMouse()
        clicked_tile = get_clicked_piece_coords(clicked_point, chess_board)

        # get all possible moves at that location and highlight them, based on whose turn it is
        if Color(chess_board.curr_player) == chess_board.board[clicked_tile[0]][clicked_tile[1]].color:
            legal_moves = chess_board.find_legal_moves(clicked_tile[0], clicked_tile[1])
            for move in legal_moves:
                tile_board[move.to_location[0]][move.to_location[1]].setFill(HIGHLIGHT_TILE_COLOR)

    # get next tile the user clicked
    clicked_point = win.getMouse()
    clicked_tile = get_clicked_piece_coords(clicked_point, chess_board)

    # if that tile was in the list of moves, make that move
    for move in legal_moves:
        if move.to_location == clicked_tile:
            chess_board.make_move(move)

            # if the captured piece was a king, end the game
            if move.captured_piece.piece == Piece.KING:
                game_running = False

    # remove highlights
    clear_board_highlights(tile_board)

    # redraw the board
    reset_piece_board(piece_board)
    piece_board = create_piece_board(tile_board, chess_board)
    draw_piece_board(piece_board)
    
# win.close()