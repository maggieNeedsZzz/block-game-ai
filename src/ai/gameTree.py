
import numpy as np
import copy
from game.board import BlockBoard
from game.commands.placePiece import PlacePiece

import random
class RandomSequenceGenerator:
    def __init__(self, board, playablePieces):
        self.board : BlockBoard = copy.deepcopy(board)
        self.playablePieces =  copy.deepcopy(playablePieces)
        self.isGameOver = False 
        
        self.positionSequence = []
        self.pieceSequence = []

    def getAvailablePositions(self, piece):
        availablePositions = []
        for i in range(self.board.getBoard().shape[0] - piece.shape[0]+1):
            for j in range(self.board.getBoard().shape[1] - piece.shape[1]+1):
                if self.board.canPieceFit(piece,[i,j]):
                    availablePositions.append([i,j])
        return availablePositions



    def generateSequence(self):

        # Can run into issues if piece chosen to be played does not fit in the current board, 
        # but some  other piece does fit, 
        # this function gives up when it encounter the first piece that does not fit
        # however, the game loop will wait for a play
        # TODO: fix that
        for _ in  range(len(self.playablePieces)):# > 0:
            random.shuffle(self.playablePieces)
            piece = self.playablePieces.pop(0)
            availablePos = self.getAvailablePositions(piece)
            if len(availablePos) != 0:
                # position = random.choice(availablePos)
                position = availablePos[0]
                placeAction = PlacePiece(piece, position, self.board, 0, 0)
                board, _ , _, _ = placeAction.execute()
                self.board = board
                self.positionSequence.append(position)
                self.pieceSequence.append(piece)
            else:
                self.isGameOver = True
                self.score = -100 # penalty

        return list(zip(self.pieceSequence,self.positionSequence) )
                    


class GameTree():
    def __init__(self, board, playablePieces, score, runningCombo, numberOfLines, parent=None):
        self.parent = parent
        self.children = []
        self.board : BlockBoard = board
        self.playablePieces = playablePieces
        self.score = score
        self.runningCombo = runningCombo
        self.numberOfLines = numberOfLines
        self.isGameOver = False 

    # No blocks left to place
    def isDone(self):
        # return len(self.children) == 0# or len(self.getAvailablePositions()) == 0
        return len(self.playablePieces) == 0  # or len(self.getAvailablePositions()) == 0

    def isLeaf(self):
        return len(self.children) == 0

    def isTerminal(self):
        return self.isGameOver

    def __eq__(self, value):
        if value == None:
            return False
        return self.board == value.board

    # Generate all possible states from the current state by placing a block
    def generateChildren(self):
        if self.isDone():
            return
        
        foundFit = False
        for piece in self.playablePieces:
            availablePos = self.getAvailablePositions(piece)
            if len(availablePos) == 0:
                continue
            for position in availablePos:
                foundFit = True
                childState = self._createNewNode(piece, position)
                childState.generateChildren()   # Recursively generate children
                self.children.append(childState)

        if not foundFit:
            self.isGameOver = True
            self.score = -100 # penalty


    def _createNewNode(self, piece, position) -> 'GameTree':
        newBoard : BlockBoard = copy.deepcopy(self.board)     
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
        return childState


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
    def __init__(self, board, playablePieces, score, runningCombo, numberOfLines, parent=None, positionSequence=[], pieceSequence=[]):
        super().__init__(board, playablePieces, score, runningCombo,numberOfLines, parent)
        self.positionSequence = positionSequence
        self.pieceSequence = pieceSequence
        


    def _createNewNode(self, piece : np.ndarray, position) -> 'GameTree':
        newBoard : BlockBoard = copy.deepcopy(self.board)     
        newScore = copy.deepcopy(self.score)
        newRunningCombo = copy.deepcopy(self.runningCombo)

        newPositionSequence : [] = copy.deepcopy(self.positionSequence)     
        newPositionSequence.append(position)

        newPieceSequence : [] = copy.deepcopy(self.pieceSequence)     
        newPieceSequence.append(piece)

        placeAction = PlacePiece(piece, position, newBoard, newScore, newRunningCombo)
        newBoard, newScore, newRunningCombo, numberOfLines = placeAction.execute()
        newPlayableBlocks = copy.deepcopy([p for p in self.playablePieces if not np.array_equal(p, piece)])
        # if len(newPlayableBlocks) == 0:
        #     currentNode = self
        #     while currentNode.parent != None:
        #         currentNode = currentNode.parent
        #     startNode = currentNode
        #     if  self.runningCombo == startNode.runningCombo:
        #         self.runningCombo == 1

        return GameTreeWithPlacements(newBoard, newPlayableBlocks, newScore, newRunningCombo, numberOfLines, self, newPositionSequence, newPieceSequence)
        



    def getSequenceOfPlaysToRoot(self):
        return list(zip(self.pieceSequence,self.positionSequence) )
    


