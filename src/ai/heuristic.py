from abc import abstractmethod
from ai.gameTree import GameTree
from game.piece import Pieces
from game.gameHelpers import ScoreCalculator

class Heuristic:
    # Its gonna be the score achieved by clearing the whole board
    MAX_SCORE_PER_PIECE_PLACEMENT = ScoreCalculator.LINE_POINTS * 6 * 2 # SCore * size * both directions
    # TODO: Needs to be turned to a instantiable class so that the board size can be defined on init
    MAX_EXPECTED_COMBO_MULTIPLIER = 50 
    # TODO: actually implement a combo cap
    @abstractmethod
    def calculateScore(self, gameTreeNode : GameTree) -> float:
        pass


# TODO: Is Frequency scaling applicable?

#TODO: Dynamic heuristics:
# for example prioritize the multiplier in earlier rounds, 
# meaning, adjust the weighting of the multiplier and other heuristics accordingly

class MaximizeScoreAndComboHeuristic(Heuristic):
    scoreWeight = 0.6
        
    @classmethod
    def calculateScore(cls, gameTreeNode : GameTree) -> float:
        normalizedScore = gameTreeNode.score / cls.MAX_SCORE_PER_PIECE_PLACEMENT
        normalizedCombo = gameTreeNode.runningCombo / cls.MAX_EXPECTED_COMBO_MULTIPLIER
        return cls.scoreWeight*normalizedScore + (1- cls.scoreWeight )*normalizedCombo 

class FitsBigPiecesHeuristic(Heuristic):
    scoreWeight = 0.5
        
    @classmethod
    def calculateScore(cls, gameTreeNode : GameTree) -> float:
        return cls.scoreWeight*gameTreeNode.score + (1- cls.scoreWeight) * sum([gameTreeNode.board.isPositionAvailable(Pieces.pieces["Five_H_Line"]),
                                                           gameTreeNode.board.isPositionAvailable(Pieces.pieces["Five_V_Line"]),
                                                             gameTreeNode.board.isPositionAvailable(Pieces.pieces["ThreeBlock"])] )
    
    
class EmptySquaresHeuristic(MaximizeScoreAndComboHeuristic):
    scoreWeight = 0.3
        
    @classmethod
    def calculateScore(cls, gameTreeNode : GameTree) -> float:
        score = super().calculateScore(gameTreeNode)
        normalizedNbrOfEmptySquares = gameTreeNode.board.getNumberOfEmptySquares() / (gameTreeNode.board.board.shape[0] * gameTreeNode.board.board.shape[1])
        return cls.scoreWeight*score + (1- cls.scoreWeight) * normalizedNbrOfEmptySquares
    

import numpy as np
class InteruptionsHeuristic(MaximizeScoreAndComboHeuristic):
    scoreWeight = 0.1
    # TODO
    MAX_DISPERSION = 2*  (6 - 1)*(6 - 1) # Its gonna be a checker pattern ´
    
        
    @classmethod
    def calculateScore(cls, gameTreeNode : GameTree) -> float:
        # score = super().calculateScore(gameTreeNode)
        normalizedInteruptionValue = (cls.MAX_DISPERSION - InteruptionsHeuristic.cal(gameTreeNode.board.board)) / cls.MAX_DISPERSION
        # print(score)
        # print(normalizedInteruptionValue)
        # print(cls.scoreWeight*score + (1- cls.scoreWeight) * normalizedInteruptionValue)

        return normalizedInteruptionValue

    # @classmethod
    # def calculateScore(cls, gameTreeNode : GameTree) -> float:
    #     return gameTreeNode.score + 10 * -InteruptionsHeuristic.calculate_runs(gameTreeNode.board.board)


    def calculate_runs(board):
        runs = 0
        kernel = np.asarray([[True, False], [False, True]], dtype=bool)

        for i in range(board.shape[0] - kernel.shape[0] + 1):
            for j in range(board.shape[1] - kernel.shape[1] + 1):
                sum = False
                for k in range(kernel.shape[0]):
                    for l in range(kernel.shape[1]):
                        if kernel[k, l]:
                            if k < kernel.shape[0] - 1 and l < kernel.shape[1] - 1:
                                sum = sum or (board[i+k, j+l] != board[i+k+1, j+l+1])
                if sum:
                    runs += 1

        print("runs: " + str(runs))
        return runs
    def cal(board):
        diffCount = 0
        for i in range(board.shape[0] - 1):
            for j in range(board.shape[1] - 1):
                if board[i][j] != board[i][j+1]:
                    diffCount += 1
                if board[i][j] != board[i+1][j]:
                    diffCount += 1
        # print("diffCount: " + str(diffCount))
        return diffCount

    # def _interuptions(self, board : BlockBoard) -> int:
