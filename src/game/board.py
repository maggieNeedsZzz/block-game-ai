import numpy as np

from game.piece import Pieces
from game.gameHelpers import ScoreCalculator

class BlockBoard():
    def __init__(self, size: int = None, boardArray: np.ndarray = None):
        if size != None:
            self.size = size
            self.board = np.zeros((size,size), dtype=bool)
        elif boardArray != None:
            self.size = boardArray.shape[0]
            self.board = boardArray

    def __eq__(self, value : np.ndarray):
        if self.board.shape != value.shape:
            return False
        return np.array_equal(self.board,value) 

    def getBoard(self):
        return self.board
    

    def addPiece(self, piece : np.ndarray, position):
        if(self.canPieceFit(piece,position)):
            for i in range(piece.shape[0]):
                for j in range(piece.shape[1]):
                    self.board[position[0] + i, position[1] + j] = piece[i][j] | self.board[position[0] + i, position[1] + j]
            

    def isPositionAvailable(self, piece):
        for i in range(self.board.shape[0] - piece.shape[0]+1):
            for j in range(self.board.shape[1] - piece.shape[1]+1):
                if self.canPieceFit(piece,[i,j]):
                    return True
        return False                    

    
    def isPositionAvailableForPieces(self, pieces):
        for piece in pieces:
            if self.isPositionAvailable(piece):
                return True 
        return False


    def canPieceFit(self, piece : np.ndarray, position):
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if (position[0] + i >= self.size or position[1] + j >= self.size) and piece[i,j]:
                    #print("Out of bounds of board")
                    return False
                if self.board[position[0] + i, position[1] + j] & piece[i][j]:
                    #print("Position Occupied")
                    return False

        return True
    

    # def canPieceFit(self, piece : np.ndarray, position, board : np.ndarray):
    #     for i in range(piece.shape[0]):
    #         for j in range(piece.shape[1]):
    #             if (position[0] + i >= board.shape[0] or position[1] + j >= board.shape[1]) and piece[i,j]:
    #                 return False
    #             if board[position[0] + i, position[1] + j] and piece[i][j]:
    #                 return False

    # return True
    

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

        return board, newScore, newRunningCombo, numberOfLines

