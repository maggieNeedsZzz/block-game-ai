
from ai.heuristic import *

from game.timer import Timer

from ai.commands.plan import AIPlan


class AI():
    def __init__(self):
        self.plan = []
        # self.heuristic = None 
        self.heuristic = InteruptionsHeuristic
        # self.heuristic = EmptySquaresHeuristic 
        # self.heuristic = FitsBigPiecesHeuristic
        # self.heuristic = MaximizeScoreAndComboHeuristic


    ## Setter
    def setPlan(self, plan):
        # TODO: check if plan is valid
        self.plan = plan

    
    def isDone(self):
        return len(self.plan) == 0


    def update(self, game):
        pass


    def think(self, game):
        planner = AIPlan(game.getBoard(), game.getPlayablePieces(), game.score, game.runningCombo, self.heuristic)
        self.plan = planner.execute()

        
    def reset(self,game):
        self.plan = []

    def getNextMove(self):
        return self.plan.pop(0)