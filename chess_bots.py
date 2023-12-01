from abc import abstractmethod
from chess import *
import random

class ChessBot():
    """
    An abstract class representing a base chess bot with no behavior.

    Attributes
    ----------
    chess_board : ChessBoard
        The board the bot is playing on.

    color : Color
        The color that the bot is controlling/playing for.
    """

    def __init__(self, chess_board: ChessBoard, color: Color):
        self.chess_board = chess_board
        self.color = color

    @abstractmethod
    def get_move(self) -> Move:
        """
        Generates a move based on the current board state, depending on the bot's behavior.
        """
        pass

class RandomMoveBot(ChessBot):
    """
    A chess bot that selects what move to make randomly.

    Attributes
    ----------
    chess_board : ChessBoard
        The board the bot is playing on.

    color : Color
        The color that the bot is controlling/playing for.
    """

    def __init__(self, chess_board: ChessBoard, color: Color):
        super().__init__(chess_board, color)

    def get_move(self) -> Move:
        """
        Select a random move from a list of all possible moves the bot could make.

        Returns
        -------
        Move
            The move the chess bot selected.

        Notes
        -----
        This function assumes it is currently the bot's turn.
        """

        # create a list of all possible moves the bot could make
        moves = []
        for i in range(len(self.chess_board.board)):
            for j in range(len(self.chess_board.board[i])):

                # only add the moves if the piece belongs to the bot
                if self.chess_board.board[i][j].color == Color(self.chess_board.curr_player):
                    moves += self.chess_board.find_legal_moves(i, j)

        return moves[random.randint(0, len(moves) - 1)]
    
class RandomPieceBot(ChessBot):
    """
    A chess bot that selects which piece to move randomly.

    Attributes
    ----------
    chess_board : ChessBoard
        The board the bot is playing on.
        
    color : Color
        The color that the bot is controlling/playing for.
    """

    def __init__(self, chess_board: ChessBoard, color: Color):
        super().__init__(chess_board, color)

    def get_move(self) -> Move:
        """
        Select a random piece from the bot's side, then select a random move for that piece.

        Returns
        -------
        Move
            The move the chess bot selected.

        Notes
        -----
        This function assumes it is currently the bot's turn.
        """

        # create a list of (row, col) tuples for every piece the bot owns
        pieces = []
        for i in range(len(self.chess_board.board)):
            for j in range(len(self.chess_board.board[i])):

                # only add the piece if it belongs to the bot
                if self.chess_board.board[i][j].color == Color(self.chess_board.curr_player):
                    pieces.append((i, j))

        # select a piece at random
        random_piece = pieces[random.randint(0, len(pieces) - 1)]

        # return a random legal move the piece can make
        moves = self.chess_board.find_legal_moves(random_piece[0], random_piece[1])
        return moves[random.randint(0, len(moves) - 1)]