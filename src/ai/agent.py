
from game.observer import Observer
from game.states.state import State


from abc import ABC, abstractmethod

from ai.gameTreeAnalyser import GameTreeAnalyser
from ai.gameTree import GameTreeWithPlacements

from game.timer import Timer


class AIState(ABC):
    def __init__(self):
        self.completed = False
    @abstractmethod
    def update(self, game, ai):
        pass
    def onEnter(self, game, ai ):
        pass
    def onExit(self, game , ai):
        pass
    def isCompleted(self):
        return self.completed
    


class AI():
    def __init__(self):
        self.plan = []
        self._state = AIWaitingState()


    ## Setter
    def setPlan(self, plan):
        # TODO: check if plan is valid
        self.plan = plan

    
    def isDone(self):
        return len(self.plan) == 0


    def update(self, game):
        self._state.update(game, self)


    ##### Action calls ?? Commands ??
    def think(self, game):
        self._state.onExit(game, self)
        self._state = AIThinkingState()
        self._state.onEnter(game, self)

    def play(self, game):
        self._state.onExit(game, self)
        self._state = AIPlayingState()
        self._state.onEnter(game, self)

        
    def reset(self,game):
        self._state.onExit(game, self)
        self._state = AIPlayingState()
        self._state.onEnter(game, self)


    def getNextMove(self):
        return self.plan.pop(0)
    # def getMove(self):
    #     return self.plan[self._move]



    # def onNotify(self, game):
    #     print("Got notifies of state change")




class AIWaitingState(AIState):
    def update(self, game):
        pass
    def onEnter(self, game, ai):
        self.plan = []
        self.completed = True
    

from ai.heuristic import *

### THis is a command not a state
class AIThinkingState(AIState):
    def __init__(self):
        super().__init__()
        self.playSequence = []
        self.isGameOver = False

        ### TODO: Implement time limit on thinking
        self.timer = Timer()

        # self.heurisistic = None
        self.heurisistic = None #InteruptionsHeuristic # MaximizeScoreAndComboHeuristicEmptySquaresHeuristic # FitsBigPiecesHeuristic

    def onEnter(self, game, ai):
        # TODO: might need to be done in parallel?
        print("Thinking!")
        # root = GameTreeWithPlacements(game.getBoard(), game.getPlayablePieces(), game.score, game.runningCombo)
        root = GameTreeWithPlacements(game.getBoard(), game.getPlayablePieces(), 0, game.runningCombo)
        root.generateChildren()
        print("Game Tree calculated.")  
        GameTreeAnalyser.reset()
        bestLeaf, bestLeafScore = GameTreeAnalyser.getBestLeafState(root, self.heurisistic)
        print("Score: " + str(bestLeafScore))
        self.playSequence = bestLeaf.getSequenceOfPlaysToRoot()
        print("Playing Sequence:")  
        print(self.playSequence)
        self.isGameOver = bestLeaf.isGameOver
        self.completed = True

    def update(self, game, ai):
        pass
    
    def onExit(self, game, ai):
        if not self.completed:
            ai.setPlan([])
        ai.setPlan(self.playSequence)


    
class AIPlayingState(AIState):
    def update(self, game, ai):
        if ai.isDone():
            self.completed = True
