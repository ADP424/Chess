import copy
from enum import Enum

class Piece(Enum):
    EMPTY = 0
    PAWN = 1 # yes, I know pawns aren't pieces
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class PieceValue(Enum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = float('inf')

class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

class ChessPiece:
    """
    A playable piece for on a chess board.

    Attributes
    ----------
    piece : Piece, default: Piece.Empty
        The type of chess piece it is (i.e. pawn, knight, bishop, etc.).
    
    color : Color, default: Color.NONE
        The color of the player who controls the piece (i.e. white, black).

    captured_by : ChessPiece, default: None
        The chess piece that captured this piece.
    """

    def __init__(self, piece=Piece.EMPTY, color=Color.NONE, captured_by=None):
        self.piece = piece
        self.color = color
        self.has_moved = False
        self.captured_by = captured_by

class Move:
    """
    A single move of a piece from one location to another.

    Attributes
    ----------
    to_location : tuple
        A tuple of the row and col the move ended on, written in the form (row, col).
    
    from_location : tuple
        A tuple of the row and col the move began on, written in the form (row, col).

    captured_piece : ChessPiece, optional
        The piece that was captured in the move, empty by default and if no piece was captured.

    capture_location : tuple, optional
        A tuple of the row and col of the captured piece, equal to `to_location` by default.
    
    special_tag : str, default: ''
        A tag representing special extra information about the move (like 'castle')
    """

    def __init__(self, to_location: tuple, from_location: tuple, captured_piece=ChessPiece(), capture_location=None, special_tag=''):
        self.to_location = to_location
        self.from_location = from_location
        self.captured_piece = captured_piece
        self.capture_location = capture_location if capture_location is not None else to_location
        self.special_tag = special_tag

class ChessBoard:
    """
    The chess board the game will be played on.

    Attributes
    ----------
    num_players : int, default: 2
        The total number of players in the game.

    board : list, default: `DEFAULT_BOARD`
        A list of lists forming a 2D grid of chess pieces.

    board_width : int, default: 8
        The number of columns on the board, should be equal to the width of `board`.
    
    board_height : int, default: 8
        The number of rows on the board, should be equal to the height of `board`.

    curr_player : int, default: 1
        A marker keeping track of whose turn it is, in range (1, num_players).

    last_move : Move, default: Move((-1, -1), (-1, -1))
        The move made in the game the turn before.
    
    captured_pieces : list, default: []
        A list of every captured piece from all players so far in the game.

    move_list : list, default: []
        A list of every move made in the game, in chronological order.
    """

    DEFAULT_BOARD = [
            [ChessPiece(Piece.ROOK, Color.BLACK), ChessPiece(Piece.KNIGHT, Color.BLACK), ChessPiece(Piece.BISHOP, Color.BLACK), ChessPiece(Piece.QUEEN, Color.BLACK), 
            ChessPiece(Piece.KING, Color.BLACK), ChessPiece(Piece.BISHOP, Color.BLACK), ChessPiece(Piece.KNIGHT, Color.BLACK), ChessPiece(Piece.ROOK, Color.BLACK)],

            [ChessPiece(Piece.PAWN, Color.BLACK), ChessPiece(Piece.PAWN, Color.BLACK), ChessPiece(Piece.PAWN, Color.BLACK), ChessPiece(Piece.PAWN, Color.BLACK),
            ChessPiece(Piece.PAWN, Color.BLACK), ChessPiece(Piece.PAWN, Color.BLACK), ChessPiece(Piece.PAWN, Color.BLACK), ChessPiece(Piece.PAWN, Color.BLACK)],

            [ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece(),
            ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece()],
            
            [ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece(),
            ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece()],
            
            [ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece(),
            ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece()],
            
            [ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece(),
            ChessPiece(), ChessPiece(), ChessPiece(), ChessPiece()],

            [ChessPiece(Piece.PAWN, Color.WHITE), ChessPiece(Piece.PAWN, Color.WHITE), ChessPiece(Piece.PAWN, Color.WHITE), ChessPiece(Piece.PAWN, Color.WHITE),
            ChessPiece(Piece.PAWN, Color.WHITE), ChessPiece(Piece.PAWN, Color.WHITE), ChessPiece(Piece.PAWN, Color.WHITE), ChessPiece(Piece.PAWN, Color.WHITE)],

            [ChessPiece(Piece.ROOK, Color.WHITE), ChessPiece(Piece.KNIGHT, Color.WHITE), ChessPiece(Piece.BISHOP, Color.WHITE), ChessPiece(Piece.QUEEN, Color.WHITE), 
            ChessPiece(Piece.KING, Color.WHITE), ChessPiece(Piece.BISHOP, Color.WHITE), ChessPiece(Piece.KNIGHT, Color.WHITE), ChessPiece(Piece.ROOK, Color.WHITE)],
        ]

    def __init__(self, num_players=2, board=DEFAULT_BOARD, board_width=8, board_height=8, curr_player=1, last_move=Move((-1, -1), (-1, -1)), captured_pieces=[], move_list=[]):
        self.num_players = num_players
        self.board = board
        self.board_width = board_width
        self.board_height = board_height
        self.curr_player = curr_player
        self.last_move = last_move
        self.captured_pieces = captured_pieces
        self.move_list = move_list

    def find_legal_moves(self, row: int, col: int) -> list:
        """
        Find every legal move the piece at the given row and column can make.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total list of legal moves the piece could take, assuming it's the controller's turn.
        """

        moves = []

        # if the row or column is out of bounds, return the empty list
        if row < 0 or row >= self.board_height or col < 0 or col >= self.board_width:
            return moves

        # if the tile is empty, then there are no legal moves, since it isn't a piece
        if self.board[row][col].piece == Piece.EMPTY:
            return moves
        
        # get all pawn moves if the piece moves like a pawn
        if self.board[row][col].piece == Piece.PAWN:
            moves += self.__find_legal_pawn_moves(row, col)
        
        # get all knight moves if the piece moves like a knight
        if self.board[row][col].piece == Piece.KNIGHT:
            moves += self.__find_legal_knight_moves(row, col)

        # get all rook moves if the piece moves like a rook
        if self.board[row][col].piece == Piece.ROOK or self.board[row][col].piece == Piece.QUEEN:
            moves += self.__find_legal_rook_moves(row, col)
        
        # get all bishop moves if the piece moves like a bishop
        if self.board[row][col].piece == Piece.BISHOP or self.board[row][col].piece == Piece.QUEEN:
            moves += self.__find_legal_bishop_moves(row, col)

        # get all king moves if the piece moves like a king
        if self.board[row][col].piece == Piece.KING:
            moves += self.__find_legal_king_moves(row, col)
            moves += self.__find_legal_castle_moves(row, col)

        return moves
    
    def __find_legal_pawn_moves(self, row, col):
        """
        Find every legal move the piece at the given row and column can make, assuming it's a pawn.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total list of legal moves the pawn could take, assuming it's the controller's turn.
        """

        moves = []

        # get white pawn moves
        if self.board[row][col].color == Color.WHITE:

            # the pawn can move up one space if that space is empty
            if row > 0 and self.board[row - 1][col].piece == Piece.EMPTY:
                moves.append(Move((row - 1, col), (row, col)))

                # the pawn can move up two spaces if it hasn't moved yet and both spaces above are empty
                if row > 1 and self.board[row - 2][col].piece == Piece.EMPTY and not self.board[row][col].has_moved:
                    moves.append(Move((row - 2, col), (row, col)))

            # the pawn can move up-left diagonally if that captures a piece
            if row > 0 and col > 0 and self.board[row - 1][col - 1].color != Color.NONE and self.board[row - 1][col - 1].color != self.board[row][col].color:
                moves.append(Move((row - 1, col - 1), (row, col), copy.deepcopy(self.board[row - 1][col - 1])))

            # en passant up-left
            elif row > 0 and col > 0 and self.last_move.to_location == (row, col - 1) and self.last_move.from_location == (row - 2, col - 1) and \
                    self.board[row][col - 1].piece == Piece.PAWN and self.board[row][col - 1].color != Color.NONE and self.board[row][col - 1].color != self.board[row][col].color:
                moves.append(Move((row - 1, col - 1), (row, col), copy.deepcopy(self.board[row][col - 1]), (row, col - 1)))

            # the pawn can move up-right diagonally if that captures a piece
            if row > 0 and col < self.board_width - 1 and self.board[row - 1][col + 1].color != Color.NONE and self.board[row - 1][col + 1].color != self.board[row][col].color:
                moves.append(Move((row - 1, col + 1), (row, col), copy.deepcopy(self.board[row - 1][col + 1])))

            # en passant up-right
            elif row > 0 and col < self.board_width - 1 and self.last_move.to_location == (row, col + 1) and self.last_move.from_location == (row - 2, col + 1) and \
                    self.board[row][col + 1].piece == Piece.PAWN and self.board[row][col + 1].color != Color.NONE and self.board[row][col + 1].color != self.board[row][col].color:
                moves.append(Move((row - 1, col + 1), (row, col), copy.deepcopy(self.board[row][col + 1]), (row, col + 1)))

        # get black pawn moves
        elif self.board[row][col].color == Color.BLACK:

            # the pawn can move down one space if that space is empty
            if row < self.board_height - 1 and self.board[row + 1][col].piece == Piece.EMPTY:
                moves.append(Move((row + 1, col), (row, col)))

                # the pawn can move down two spaces if it hasn't moved yet and both spaces above are empty
                if row < self.board_height - 2 and self.board[row + 2][col].piece == Piece.EMPTY and not self.board[row][col].has_moved:
                    moves.append(Move((row + 2, col), (row, col)))

            # the pawn can move down-left diagonally if that captures a piece
            if row < self.board_height - 1 and col > 0 and self.board[row + 1][col - 1].color != Color.NONE and self.board[row + 1][col - 1].color != self.board[row][col].color:
                moves.append(Move((row + 1, col - 1), (row, col), copy.deepcopy(self.board[row + 1][col - 1])))

            # en passant down-left
            elif row < self.board_height - 1 and col > 0 and self.last_move.to_location == (row, col - 1) and self.last_move.from_location == (row + 2, col - 1) and \
                    self.board[row][col - 1].piece == Piece.PAWN and self.board[row][col - 1].color != Color.NONE and self.board[row][col - 1].color != self.board[row][col].color:
                moves.append(Move((row + 1, col - 1), (row, col), copy.deepcopy(self.board[row][col - 1]), (row, col - 1)))

            # the pawn can move down-right diagonally if that captures a piece
            if row < self.board_height - 1 and col < self.board_width - 1 and self.board[row + 1][col + 1].color != Color.NONE and self.board[row + 1][col + 1].color != self.board[row][col].color:
                moves.append(Move((row + 1, col + 1), (row, col), copy.deepcopy(self.board[row + 1][col + 1])))

            # en passant down-right
            elif row < self.board_height - 1 and col < self.board_width - 1 and self.last_move.to_location == (row, col + 1) and self.last_move.from_location == (row + 2, col + 1) and \
                    self.board[row][col + 1].piece == Piece.PAWN and self.board[row][col + 1].color != Color.NONE and self.board[row][col + 1].color != self.board[row][col].color:
                moves.append(Move((row + 1, col + 1), (row, col), copy.deepcopy(self.board[row][col + 1]), (row, col + 1)))

        return moves
    
    def __find_legal_knight_moves(self, row, col):
        """
        Find every legal move the piece at the given row and column can make, assuming it's a knight.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total list of legal moves the knight could take, assuming it's the controller's turn.
        """
        
        moves = []

        # get up 1 - left 2 move
        if row > 0 and col > 1 and self.board[row - 1][col - 2] and self.board[row][col].color != self.board[row - 1][col - 2].color:
            moves.append(Move((row - 1, col - 2), (row, col), copy.deepcopy(self.board[row - 1][col - 2])))

        # get up 2 - left 1 move
        if row > 1 and col > 0 and self.board[row - 2][col - 1] and self.board[row][col].color != self.board[row - 2][col - 1].color:
            moves.append(Move((row - 2, col - 1), (row, col), copy.deepcopy(self.board[row - 2][col - 1])))

        # get up 1 - right 2 move
        if row > 0 and col < self.board_width - 2 and self.board[row - 1][col + 2] and self.board[row][col].color != self.board[row - 1][col + 2].color:
            moves.append(Move((row - 1, col + 2), (row, col), copy.deepcopy(self.board[row - 1][col + 2])))

        # get up 2 - right 1 move
        if row > 1 and col < self.board_width - 1 and self.board[row - 2][col + 1] and self.board[row][col].color != self.board[row - 2][col + 1].color:
            moves.append(Move((row - 2, col + 1), (row, col), copy.deepcopy(self.board[row - 2][col + 1])))

        # get down 1 - left 2 move
        if row < self.board_height - 1 and col > 1 and self.board[row + 1][col - 2] and self.board[row][col].color != self.board[row + 1][col - 2].color:
            moves.append(Move((row + 1, col - 2), (row, col), copy.deepcopy(self.board[row + 1][col - 2])))

        # get down 2 - left 1 move
        if row < self.board_height - 2 and col > 0 and self.board[row + 2][col - 1] and self.board[row][col].color != self.board[row + 2][col - 1].color:
            moves.append(Move((row + 2, col - 1), (row, col), copy.deepcopy(self.board[row + 2][col - 1])))

        # get down 1 - right 2 move
        if row < self.board_height - 1 and col < self.board_width - 2 and self.board[row + 1][col + 2] and self.board[row][col].color != self.board[row + 1][col + 2].color:
            moves.append(Move((row + 1, col + 2), (row, col), copy.deepcopy(self.board[row + 1][col + 2])))

        # get down 2 - right 1 move
        if row < self.board_height - 2 and col < self.board_width - 1 and self.board[row + 2][col + 1] and self.board[row][col].color != self.board[row + 2][col + 1].color:
            moves.append(Move((row + 2, col + 1), (row, col), copy.deepcopy(self.board[row + 2][col + 1])))

        return moves
    
    def __find_legal_rook_moves(self, row, col):
        """
        Find every legal move the piece at the given row and column can make, assuming it's a rook.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total list of legal moves the rook could take, assuming it's the controller's turn.
        """
        
        moves = []

        # get left moves
        c = col
        while c > 0:
            c -= 1
            if self.board[row][c].piece == Piece.EMPTY:
                moves.append(Move((row, c), (row, col)))
            elif self.board[row][c].color != self.board[row][col].color:
                moves.append(Move((row, c), (row, col), copy.deepcopy(self.board[row][c])))
                break
            else:
                break

        # get right moves
        c = col
        while c < self.board_width - 1:
            c += 1
            if self.board[row][c].piece == Piece.EMPTY:
                moves.append(Move((row, c), (row, col)))
            elif self.board[row][c].color != self.board[row][col].color:
                moves.append(Move((row, c), (row, col), copy.deepcopy(self.board[row][c])))
                break
            else:
                break

        # get up moves
        r = row
        while r > 0:
            r -= 1
            if self.board[r][col].piece == Piece.EMPTY:
                moves.append(Move((r, col), (row, col)))
            elif self.board[r][col].color != self.board[row][col].color:
                moves.append(Move((r, col), (row, col), copy.deepcopy(self.board[r][col])))
                break
            else:
                break

        # get down moves
        r = row
        while r < self.board_height - 1:
            r += 1
            if self.board[r][col].piece == Piece.EMPTY:
                moves.append(Move((r, col), (row, col)))
            elif self.board[r][col].color != self.board[row][col].color:
                moves.append(Move((r, col), (row, col), copy.deepcopy(self.board[r][col])))
                break
            else:
                break

        return moves
    
    def __find_legal_bishop_moves(self, row, col):
        """
        Find every legal move the piece at the given row and column can make, assuming it's a bishop.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total list of legal moves the bishop could take, assuming it's the controller's turn.
        """
            
        moves = []

        # get up-left moves
        r = row
        c = col
        while r > 0 and c > 0:
            r -= 1
            c -= 1
            if self.board[r][c].piece == Piece.EMPTY:
                moves.append(Move((r, c), (row, col)))
            elif self.board[r][c].color != self.board[row][col].color:
                moves.append(Move((r, c), (row, col), copy.deepcopy(self.board[r][c])))
                break
            else:
                break

        # get up-right moves
        r = row
        c = col
        while r > 0 and c < self.board_width - 1:
            r -= 1
            c += 1
            if self.board[r][c].piece == Piece.EMPTY:
                moves.append(Move((r, c), (row, col)))
            elif self.board[r][c].color != self.board[row][col].color:
                moves.append(Move((r, c), (row, col), copy.deepcopy(self.board[r][c])))
                break
            else:
                break

        # get down-left moves
        r = row
        c = col
        while r < self.board_height - 1 and c > 0:
            r += 1
            c -= 1
            if self.board[r][c].piece == Piece.EMPTY:
                moves.append(Move((r, c), (row, col)))
            elif self.board[r][c].color != self.board[row][col].color:
                moves.append(Move((r, c), (row, col), copy.deepcopy(self.board[r][c])))
                break
            else:
                break

        # get down-right moves
        r = row
        c = col
        while r < self.board_height - 1 and c < self.board_width - 1:
            r += 1
            c += 1
            if self.board[r][c].piece == Piece.EMPTY:
                moves.append(Move((r, c), (row, col)))
            elif self.board[r][c].color != self.board[row][col].color:
                moves.append(Move((r, c), (row, col), copy.deepcopy(self.board[r][c])))
                break
            else:
                break

        return moves
    
    def __find_legal_king_moves(self, row, col):
        """
        Find every legal move the piece at the given row and column can make, assuming it's a king.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total list of legal moves the king could take, assuming it's the controller's turn.
        """

        moves = []

        # get up-left move
        if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row][col].color != self.board[row - 1][col - 1].color:
            moves.append(Move((row - 1, col - 1), (row, col), copy.deepcopy(self.board[row - 1][col - 1])))

        # get up move
        if row > 0 and self.board[row - 1][col] and self.board[row][col].color != self.board[row - 1][col].color:
            moves.append(Move((row - 1, col), (row, col), copy.deepcopy(self.board[row - 1][col])))

        # get up-right move
        if row > 0 and col < self.board_width - 1 and self.board[row - 1][col + 1] and \
           self.board[row][col].color != self.board[row - 1][col + 1].color:
            moves.append(Move((row - 1, col + 1), (row, col), copy.deepcopy(self.board[row - 1][col + 1])))

        # get left move
        if col > 0 and self.board[row][col - 1] and self.board[row][col].color != self.board[row][col - 1].color:
            moves.append(Move((row, col - 1), (row, col), copy.deepcopy(self.board[row][col - 1])))

        # get right move
        if col < self.board_width - 1 and self.board[row][col + 1] and self.board[row][col].color != self.board[row][col + 1].color:
            moves.append(Move((row, col + 1), (row, col), copy.deepcopy(self.board[row][col + 1])))

        # get down-left move
        if row < self.board_height - 1 and col > 0 and self.board[row + 1][col - 1] and \
           self.board[row][col].color != self.board[row + 1][col - 1].color:
            moves.append(Move((row + 1, col - 1), (row, col), copy.deepcopy(self.board[row + 1][col - 1])))

        # get down move
        if row < self.board_height - 1 and self.board[row + 1][col] and self.board[row][col].color != self.board[row + 1][col].color:
            moves.append(Move((row + 1, col), (row, col), copy.deepcopy(self.board[row + 1][col])))

        # get down-right move
        if row < self.board_height - 1 and col < self.board_width - 1 and self.board[row + 1][col + 1] and \
           self.board[row][col].color != self.board[row + 1][col + 1].color:
            moves.append(Move((row + 1, col + 1), (row, col), copy.deepcopy(self.board[row + 1][col + 1])))

        return moves

    def __find_legal_castle_moves(self, row, col):
        """
        Find every legal castle move the piece at the given row and column can make, assuming it's a king.

        Parameters
        ----------
        row : int
            The row the piece is located on, must be less than `board_height`.
        col : int
            The column the piece is located on, must be less than `board_width`.

        Returns
        -------
        list
            A list of Moves defining the total legal castle moves available for the king, assuming it's the controller's turn.
        """

        moves = []

        # get king-side castle
        if col == 4 and (row == 0 or row == self.board_height - 1) and self.board[row][col + 1].piece == Piece.EMPTY and \
           self.board[row][col + 2].piece == Piece.EMPTY and not self.board[row][col + 3].has_moved and not self.board[row][col].has_moved:
            moves.append(Move((row, col + 2), (row, col), special_tag='castle'))

        # get queen-side castle
        if col == 4 and (row == 0 or row == self.board_height - 1) and self.board[row][col - 1].piece == Piece.EMPTY and self.board[row][col - 2].piece == Piece.EMPTY and \
           self.board[row][col - 3].piece == Piece.EMPTY and not self.board[row][col - 4].has_moved and not self.board[row][col].has_moved:
            moves.append(Move((row, col - 2), (row, col), special_tag='castle'))

        return moves
    
    def make_move(self, move: Move):
        """
        Implement the changes specified in move onto the board and increment `curr_player`.

        Parameters
        ----------
        move : Move
            The move to be implemented onto the board.

        Notes
        -----
        This function changes `self.board`, adds the move to `self.move_list`, sets `last_move` to be equal to the move, 
        adds any captured pieces to `self.captured_pieces`, and sets `has_moved` to True for the piece that moved. 
        It does not change or care whose turn it is and will make the move regardless.
        """

        if move.special_tag == 'castle':

            # move the king to its new spot
            self.board[move.from_location[0]][move.from_location[1]].has_moved = True
            self.board[move.to_location[0]][move.to_location[1]] = self.board[move.from_location[0]][move.from_location[1]]
            self.board[move.from_location[0]][move.from_location[1]] = ChessPiece()
            
            # move the left rook if this is a queen-side castle
            if move.to_location[1] < move.from_location[1]:
                self.board[move.to_location[0]][move.to_location[1] - 2].has_moved = True
                self.board[move.to_location[0]][move.to_location[1] + 1] = self.board[move.to_location[0]][move.to_location[1] - 2]
                self.board[move.to_location[0]][move.to_location[1] - 2] = ChessPiece()

            # move the right rook if this is a king-side castle
            else:
                self.board[move.to_location[0]][move.to_location[1] + 1].has_moved = True
                self.board[move.to_location[0]][move.to_location[1] - 1] = self.board[move.to_location[0]][move.to_location[1] + 1]
                self.board[move.to_location[0]][move.to_location[1] + 1] = ChessPiece()

        else:

            # if a piece was captured, add it to the captured pieces list and set its spot to empty
            if move.captured_piece.piece != Piece.EMPTY:
                move.captured_piece.captured_by = self.board[move.from_location[0]][move.from_location[1]]
                self.captured_pieces.append(copy.deepcopy(move.captured_piece))
                self.board[move.capture_location[0]][move.capture_location[1]] = ChessPiece()
    
            # move the piece to its new spot
            self.board[move.from_location[0]][move.from_location[1]].has_moved = True
            self.board[move.to_location[0]][move.to_location[1]] = self.board[move.from_location[0]][move.from_location[1]]
            self.board[move.from_location[0]][move.from_location[1]] = ChessPiece()

            # if the piece was a pawn, and it just reached the end, transform it into a queen
            if self.board[move.to_location[0]][move.to_location[1]].piece == Piece.PAWN and \
               move.to_location[0] == 0 or move.to_location[0] == self.board_height - 1:
                self.board[move.to_location[0]][move.to_location[1]] = ChessPiece(Piece.QUEEN, self.board[move.to_location[0]][move.to_location[1]].color)
        
        # add the move to the moves list, set the last move equal to it, and increment curr_player
        self.move_list.append(copy.deepcopy(move))
        self.last_move = copy.deepcopy(move)
        if self.curr_player < self.num_players:
            self.curr_player += 1
        else:
            self.curr_player = 1

    def do_turn(self):
        print()
    
    def print_board(self):
        """
        Print a string representation of the chess board to the terminal, with a newline after each row.
        """

        for row in self.board:
            for piece in row:
                if piece.piece == Piece.EMPTY:
                        print(" . ", end="")
                elif piece.color == Color.WHITE:
                    if piece.piece == Piece.PAWN:
                        print(" ♙ ", end="")
                    elif piece.piece == Piece.KNIGHT:
                        print(" ♘ ", end="")
                    elif piece.piece == Piece.BISHOP:
                        print(" ♗ ", end="")
                    elif piece.piece == Piece.ROOK:
                        print(" ♖ ", end="")
                    elif piece.piece == Piece.QUEEN:
                        print(" ♕ ", end="")
                    elif piece.piece == Piece.KING:
                        print(" ♔ ", end="")
                elif piece.color == Color.BLACK:
                    if piece.piece == Piece.PAWN:
                        print(" ♙ ", end="")
                    elif piece.piece == Piece.KNIGHT:
                        print(" ♘ ", end="")
                    elif piece.piece == Piece.BISHOP:
                        print(" ♝ ", end="")
                    elif piece.piece == Piece.ROOK:
                        print(" ♖ ", end="")
                    elif piece.piece == Piece.QUEEN:
                        print(" ♛ ", end="")
                    elif piece.piece == Piece.KING:
                        print(" ♚ ", end="")
            print()