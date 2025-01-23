import numpy as np
import random

from game.board import BlockBoard
from game.commands.placePiece import PlacePiece
from ui.ui import UI
from game.gameHelpers import PieceGenerator

from game.board import BoardLogic

from ai.agent import AI
from ui.ui import Observer

from game.observer import Publisher



gameVariables = None

from game.states.state import  GeneratingPiecesState
# Notifies subscribers when the game variables change
class Game(Publisher):
    def __init__(self, seed, isAI = True):
        super().__init__()
        random.seed(seed)

        boardSize = 8
        #static
        self.board = BlockBoard(boardSize)
        # self.LINE_POINTS = 10
        # self.COMBO_MULTIPLIER = 2

        self.ui = UI(boardSize)

        self.isAI = isAI
        self.ai = AI()
        
        #runtime
        self.playablePieces = None
        self.score = 0
        self.runningCombo = 0
        self.roundCombo = False

        self.isGameOver = False

        self.addObserver(self.ui)

        
        self.state = GeneratingPiecesState()     
        self.state.onEnter(self)
        



    def newRound(self):
        self.playablePieces = PieceGenerator.generatePieces()
        self.notify(self, "newRound")
        # self.ui.cleanPlayablePieces()
        # self.ai.reset()
        # self.ui.setPlayablePieces(self.playablePieces)

    def gameOver(self):
        self.isGameOver = True


    def getPlayablePieces(self):
        return self.playablePieces
    
    def getBoard(self):
        return self.board
    
    def playPiece(self, piece, position):
        # placeAction = PlacePiece(piece, position, self.board, self.score, self.runningCombo)
        # newBoard, newScore, newRunningCombo = placeAction.execute()
        
        self.board.addPiece(piece, position)
        for i, p in enumerate(self.playablePieces):
            if np.array_equal(p, piece):
                self.playablePieces.pop(i)
                break
        # self.playablePieces = [ p for p in self.playablePieces if not np.array_equal(p, piece) ]

        # self.ai.completeMove()
        # self.ui.updateCombo(self.runningCombo)
        # self.ui.updateBoardPiecesWithColor(self.board.getBoard(), self.ui.getPlayablePieceColor(pieceIndex))
        # self.ui.removePlayablePiece(pieceIndex)

        self.notify(self, "piecePlayed")
        
    def activateBoardLogic(self):
        newBoard, newScore, newRunningCombo = BoardLogic.execute(self.board, self.runningCombo, self.score)
        self.board = newBoard
        self.score = newScore
        self.runningCombo = newRunningCombo
        self.notify(self, "logicDone")
        # self.ui.setScore(self.score)
        

    def update(self):

        # Game state update 
        self.state.update(self)
        self.ai.update(self)
        if self.state.isCompleted():      
            self.state = self.state.onExit(self)      
            self.state.onEnter(self)
