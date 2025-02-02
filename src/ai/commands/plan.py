import numpy as np

from game.commands.action import ActionCommand
from game.board import BlockBoard
from game.timer import Timer

from ai.gameTreeAnalyser import GameTreeAnalyser
from ai.gameTree import GameTreeWithPlacements, RandomSequenceGenerator

from ai.heuristic import *

class AIPlan(ActionCommand):
    def __init__(self, board : BlockBoard, playablePieces : np.ndarray, score, runningCombo, heurisitic):
        self.SCORE_FROM_0 = True


        self.playSequence = []
        self.isGameOver = False

        self.board = board
        self.playablePieces = playablePieces
        self.score = score
        self.runningCombo = runningCombo
        self.heuristic = heurisitic

        ### TODO: Implement time limit on thinking
        # self.timer = Timer()

        


    def execute(self):
        if self.board.getNumberOfEmptySquares() > 3*((self.board.board.shape[0]**2)//4):
            print("Random!")
            thing = RandomSequenceGenerator(self.board, self.playablePieces)
            self.playSequence = thing.generateSequence()
            # print(self.playSequence)
            # self.isGameOver = thing.isGameOver
        else: 
            # TODO: might need to be done in parallel?
            print("Thinking!")
            baseScore = 0 if self.SCORE_FROM_0 else self.score
            root = GameTreeWithPlacements(self.board , self.playablePieces, baseScore, self.runningCombo, 0)
            root.generateChildren()
            print("Game Tree calculated.")  
            GameTreeAnalyser.reset()
            bestLeaf, bestLeafScore = GameTreeAnalyser.getBestLeafState(root, self.heuristic)
            # print("Score: " + str(bestLeafScore))
            self.playSequence = bestLeaf.getSequenceOfPlaysToRoot()
            # print("Playing Sequence:")  
            # print(self.playSequence)
            # self.isGameOver = bestLeaf.isGameOver
        return self.playSequence