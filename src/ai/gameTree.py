
import numpy as np
import copy
from game.board import BlockBoard
from game.commands.placePiece import PlacePiece


class GameTree():
    def __init__(self, board, playablePieces, score, runningCombo, parent=None):
        self.parent = parent
        self.children = []
        self.board : BlockBoard = board
        self.playablePieces = playablePieces
        self.score = score
        self.runningCombo = runningCombo
        self.isGameOver = False ## DO THIS????

    # No blocks left to place
    def isLeaf(self):
        # return len(self.children) == 0# or len(self.getAvailablePositions()) == 0
        return len(self.playablePieces) == 0  # or len(self.getAvailablePositions()) == 0

    def isTerminal(self):
        return self.isGameOver

    def __eq__(self, value):
        if value == None:
            return False
        return self.board == value.board

    def generateChildren(self):
        # Generate all possible states from the current state by placing a block
        if self.isLeaf():
            return
        
        for piece in self.playablePieces:
            availablePos = self.getAvailablePositions(piece)
            if len(availablePos) == 0:
                self.isGameOver = True
                self.score = -100 # penalty
                return
            for position in availablePos:
                newBoard : BlockBoard = copy.deepcopy(self.board)      #works, but maybe look into manual copy
                
                placeAction = PlacePiece(piece, position, newBoard, self.score, self.runningCombo)
                newBoard, newScore, newRunningCombo = placeAction.execute()
                # new_board = self.place_block(self.board, piece, position, newScore, newRunningCombo)~
                # print("Type " +str( (piece.all())) )
                # print(self.playablePieces)
                # print("wow")
                # print([p for p in self.playablePieces])
                newPlayableBlocks = copy.deepcopy([p for p in self.playablePieces if not np.array_equal(p, piece)])
                # print("Blcks left", newPlayableBlocks)
                childState = GameTree(newBoard, newPlayableBlocks, newScore, newRunningCombo, self)
                childState.generateChildren()   # Recursively generate children
                self.children.append(childState)




    # finds the positions where the @piece can fit in the current board
    # returns a list of 2D coordinates
    def getAvailablePositions(self, piece):
        availablePositions = []
        for i in range(self.board.getBoard().shape[0] - piece.shape[0]+1):
            for j in range(self.board.getBoard().shape[1] - piece.shape[1]+1):
                if self.board.canPieceFit(piece,[i,j]):
                    availablePositions.append([i,j])
        return availablePositions



    def getSequenceOfBoardsToRoot(self):
        sequence = []
        currentState = self
        while currentState.parent != None:
            sequence.append(currentState)
            currentState = currentState.parent
        sequence = sequence[::-1]   # Inverts the sequence
        return sequence
    


class GameTreeWithPlacements(GameTree):
    def __init__(self, board, playablePieces, score, runningCombo, parent=None, positionSequence=[], pieceSequence=[]):
        super().__init__(board, playablePieces, score, runningCombo, parent)
        self.positionSequence = positionSequence
        self.pieceSequence = pieceSequence

    def generateChildren(self):
        # Generate all possible states from the current state by placing a block
        if self.isLeaf():
            return
        
        for piece in self.playablePieces:
            availablePos = self.getAvailablePositions(piece)
            if len(availablePos) == 0:
                self.isGameOver = True
                self.score = -100 # penalty
                return
            for position in availablePos:
                newBoard : BlockBoard = copy.deepcopy(self.board)      #works, but maybe look into manual copy
                newPositionSequence : [] = copy.deepcopy(self.positionSequence)     
                newPositionSequence.append(position)
                newPieceSequence : [] = copy.deepcopy(self.pieceSequence)     
                newPieceSequence.append(piece)
                placeAction = PlacePiece(piece, position, newBoard, self.score, self.runningCombo)
                newBoard, newScore, newRunningCombo = placeAction.execute()
                # new_board = self.place_block(self.board, piece, position, newScore, newRunningCombo)~
                # print("Type " +str( (piece.all())) )
                # print(self.playablePieces)
                # print("wow")
                # print([p for p in self.playablePieces])
                newPlayableBlocks = copy.deepcopy([p for p in self.playablePieces if not np.array_equal(p, piece)])
                # print("Blcks left", newPlayableBlocks)
                childState = GameTreeWithPlacements(newBoard, newPlayableBlocks, newScore, newRunningCombo, self, newPositionSequence, newPieceSequence)
                childState.generateChildren()   # Recursively generate children
                self.children.append(childState)




    def getSequenceOfPlaysToRoot(self):
        return list(zip(self.pieceSequence,self.positionSequence) )
    


