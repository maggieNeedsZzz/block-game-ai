
from enum import Enum
import pygame 
from abc import ABC, abstractmethod

from ai.gameTreeAnalyser import GameTreeAnalyser
from ai.gameTree import GameTreeWithPlacements


class StateEnum(Enum):
    PLAYING = 0
    GENERATING_PIECES = 1
    GAMEOVER = 2


#### TODO: Can these be class methods???
# TODO: Consider game object in init
class State(ABC):
    def __init__(self):
        self.completed = False
    def handleInput(self, event : pygame.event.Event, game ):
        pass
    @abstractmethod
    def update(self, game ):
        pass
    def onEnter(self, game ):
        pass
    def onExit(self, game ):
        pass
    def isCompleted(self):
        return self.completed
    


from game.timer import Timer

class GameOverState(State):
    def onEnter(self, game):
        print("Oops, GAME OVER.")
        game.gameOver()
    def update(self, game ):
        pass


class PlayingState(State):
    def __init__(self):
        super().__init__()
        self.piece, self.position = None, None
        self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS = 100 #1500
        self.isGameOver = False

        self.timer = Timer()

    def onEnter(self, game ):
        if game.isAI:
            game.ai.play(game)
        self.isGameOver = game.isGameOver
        self.timer.start(self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS)
        
    

    def update(self, game ):
        if self.isGameOver:
            self.completed = True
        if game.isAI:
            if self.timer.isDone():
                if game.ai.isDone():
                    print("No more moves.")
                    self.completed = True
                    return
                self.piece, self.position = game.ai.getNextMove()
                print("Playing piece: " + str(self.piece) + " At: " + str(self.position))
                game.playPiece(self.piece, self.position)
                # self.timer.start(self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS)
                
                self.completed = True



    def onExit(self, game):
        return BoardLogicState()




class GeneratingPiecesState(State):
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.WAIT_TIME = 400#1000

    def onEnter(self, game ):
        print("New Round!")
        game.newRound()
        if game.isAI:
            game.ai.reset(game)
            game.ai.think(game)
        self.timer.start(self.WAIT_TIME) 

    def update(self, game ):
        if self.timer.isDone():
            self.completed = True

    def onExit(self, game):
        # return DecideGamePlan()
        return GameLogicChecks()
    

class BoardLogicState(State):
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.WAIT_TIME = 500

    def onEnter(self, game ):
        print("Cleaning Board!")
        self.timer.start(self.WAIT_TIME)

    def update(self, game ):
        if self.timer.isDone():
            game.activateBoardLogic()
            self.completed = True

    def onExit(self, game):
        return GameLogicChecks()
            



class GameLogicChecks(State):
    def __init__(self):
        self.roundEnd = False
        super().__init__()



    def onEnter(self, game):
        self.roundEnd = True if len(game.playablePieces) == 0 else False
        if not self.roundEnd:
            game.isGameOver = not game.getBoard().isPositionAvailableForPieces(game.getPlayablePieces())
            # GameLogicChecks.isPositionAvailable(game.getBoard(), game.getPlayablePieces())

    def update(self, game):
        self.completed = True

    def onExit(self, game):
        if game.isGameOver:
            return GameOverState()
        else:
            if self.roundEnd:
                return GeneratingPiecesState()
            else:
                return PlayingState()
            



# class PlayingStateNoWait(State):
#     def __init__(self):
#         super().__init__()
#         self.playSequence = []
#         self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS = 1500
#         self.isGameOver = False

#         # Timer
#         self.initTime = 0
#         self.currentTime = 0

#     def onEnter(self, game : ):
#         print("Playing!")
#         root = GameTreeWithPlacements(game.getBoard(), game.getPlayablePieces(), game.score, game.runningCombo)
#         root.generateChildren()
#         print(" tree calculated.")  
#         bestLeaf , bestLeafScore = GameTreeAnalyser.getBestLeafState(root)
#         self.playSequence = bestLeaf.getSequenceOfPlaysToRoot()
#         print(self.playSequence)
#         self.initTime = pygame.time.get_ticks()
#         self.isGameOver = bestLeaf.isGameOver
        
    

#     def update(self, game : ):
#         self.currentTime =  pygame.time.get_ticks() - self.initTime
#         if  self.currentTime > self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS:
#             self.currentTime = 0
#             print("Playing piece: " + str(self.playSequence[0][1]))
#             if len(self.playSequence) > 0:
#                 game.playPiece(self.playSequence[0][0], self.playSequence[0][1])
#                 self.playSequence.pop(0)
#                 self.initTime = pygame.time.get_ticks()
#                 if len(self.playSequence) == 0:
#                     self.completed = True
#             else:
#                 self.completed = True


#     def onExit(self, game):
#         if self.isGameOver:
#             return GameOverState()
#         else:
#             return GeneratingPiecesState()