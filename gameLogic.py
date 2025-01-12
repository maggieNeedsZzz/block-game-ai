import numpy as np
# import matplotlib.pyplot as plt
# from enum import Enum
# import sys
from itertools import permutations
# import copy
import random
# import typing

from board import BlockBoard
from action import PlacePiece
from ui import UI
from helpers import PieceGenerator

class Game():
    def __init__(self, seed, ui : UI):
        random.seed(seed)
        #static
        self.board = BlockBoard(6)
        self.LINE_POINTS = 10
        self.COMBO_MULTIPLIER = 2

        self.ui = ui
        #runtime
        self.playablePieces = None
        self.score = 0
        self.runningCombo = 0
        self.roundCombo = False

        self.isGameOver = False

    def newRound(self):
        self.playablePieces = PieceGenerator.generatePieces()
        # self.ui.cleanPlayablePieces()
        self.ui.setPlayablePieces(self.playablePieces)

    def gameOver(self):
        self.isGameOver = True


    def getPlayablePieces(self):
        return self.playablePieces
    
    def getBoard(self):
        return self.board
    
    def playPiece(self, piece, position):
        placeAction = PlacePiece(piece, position, self.board, self.score, self.runningCombo)
        newBoard, newScore, newRunningCombo = placeAction.execute()
        self.board = newBoard
        self.score = newScore
        self.runningCombo = newRunningCombo 

        pieceIndex = 0
        for i, p in enumerate(self.playablePieces):
            if np.array_equal(p, piece):
                pieceIndex = i
                self.playablePieces.pop(i)
                break
        # self.playablePieces = [ p for p in self.playablePieces if not np.array_equal(p, piece) ]

        self.ui.setScore(self.score)
        # self.ui.updateCombo(self.runningCombo)
        self.ui.updateBoardPiecesWithColor(newBoard.getBoard(), self.ui.getPlayablePieceColor(pieceIndex))
        self.ui.removePlayablePiece(pieceIndex)
        
