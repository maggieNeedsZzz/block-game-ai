import numpy as np

from game.commands.action import ActionCommand
from game.board import BlockBoard, BoardLogic 

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
