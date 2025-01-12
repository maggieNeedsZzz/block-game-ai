import numpy as np
from board import BlockBoard, BoardLogic 
# from piece import Piece

class ActionCommand():
    def execute():
        pass

class PlacePiece(ActionCommand):
    def __init__(self, piece : np.ndarray, position : np.ndarray, board : BlockBoard, score : int, runningCombo : int):
        self.piece = piece
        self.position = position
        self.board = board
        self.score = score
        self.runningCombo = runningCombo

    def execute(self):
        self.board.addPiece(self.piece, self.position)
        return BoardLogic.execute(self.board, self.runningCombo, self.score)


# ActionCommand placePiece(piece, position)
# ActionCommand removePieceFromShowcase()
# ActionCommand startNewRound()