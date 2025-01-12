import numpy as np
from piece import Piece

from helpers import ScoreCalculator

class BlockBoard():
    def __init__(self, size: int = None, boardArray: np.ndarray = None):
        #static
        if size != None:
            self.size = size
            self.board = np.zeros((size,size), dtype=bool)
        elif boardArray != None:
            self.size = boardArray.shape[0]
            self.board = boardArray

        # play state
        # self.clearRowIndexes = []
        # self.clearColIndexes = []
        # self.numberOfLines = 0

    def __eq__(self, value : np.ndarray):
        if self.board.shape != value.shape:
            return False
        return np.array_equal(self.board,value) 
        # return (self.board == value).all()

    def getBoard(self):
        return self.board
    
    #|!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def __call__(self, *args, **kwds):
    #     return self.board

    def addPiece(self, piece : Piece, position):
        if(self.canFit(piece,position)):
            for i in range(piece.shape[0]):
                for j in range(piece.shape[1]):
                    self.board[position[0] + i, position[1] + j] = piece[i][j] | self.board[position[0] + i, position[1] + j]
            
                    


    def canFit(self, piece : Piece, position):
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if (position[0] + i >= self.size or position[1] + j >= self.size) and piece[i,j]:
                    #print("Out of bounds of board")
                    return False
                if self.board[position[0] + i, position[1] + j] & piece[i][j]:
                    #print("Position Occupied")
                    return False

        return True
    

    # def getState(self):
    #     for i, row in enumerate(self.board):
    #         if row.all() == True:
    #             self.clearRowIndexes.append(i)
    #     for j, col in enumerate(self.board.T):
    #         if col.all() == True:
    #             self.clearColIndexes.append(j) 
    #     self.numberOfLines = len(self.clearRowIndexes) + len(self.clearColIndexes)
    #     return self.numberOfLines
        

    # def clearLines(self):
    #     for i in self.clearRowIndexes:
    #         self.board[i].fill(False)
    #     for i in self.clearColIndexes:
    #         self.board.T[i].fill(False)

    # def resetState(self):
    #     self.clearRowIndexes = []
    #     self.clearColIndexes = []
    #     self.numberOfLines = 0



    # for when the piece size equals the dimentions of the piece (meaning the array isnt padded)
    # def canFit_PieceSize(self, piece, position):
    #     position = np.asarray(position)
    #     for i in range(2):
    #         if position[i] + piece.shape[i] -1 >= self.size:
    #             print("Out of bounds of board")
    #             return False

    #     for i in range(piece.shape[0]):
    #         for j in range(piece.shape[1]):
    #             if self.board[position[0] + i, position[1] + j] & piece[i][j]:
    #                 #print("Position Occupied")
    #                 return False

    #     return True


    def getNumberOfEmptySquares(self):
        return np.sum(self.board ^ np.ones(self.board.shape,dtype=bool)) 
    
    
    def getNumberOfOccupiedSquares(self):
        return np.sum(self.board ^ np.zeros(self.board.shape,dtype=bool)) 



class BoardLogic():
    @staticmethod
    def findLines(board : np.ndarray):
        clearRowIndexes = []
        clearColIndexes = []
        for i, row in enumerate(board):
            if row.all() == True:
                clearRowIndexes.append(i)
        for j, col in enumerate(board.T):
            if col.all() == True:
                clearColIndexes.append(j) 
        numberOfLines = len(clearRowIndexes) + len(clearColIndexes)
        return numberOfLines, clearRowIndexes, clearColIndexes  

    @staticmethod
    def execute(board : BlockBoard, runningCombo, score):
        numberOfLines, clearRowIndexes, clearColIndexes = BoardLogic.findLines(board.getBoard())
        newScore, newRunningCombo = ScoreCalculator.calculateNewScore(score, runningCombo, numberOfLines)

        for i in clearRowIndexes:
            board.getBoard()[i].fill(False)
        for i in clearColIndexes:
            board.getBoard().T[i].fill(False)

        return board, newScore, newRunningCombo

