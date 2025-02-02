
from enum import Enum
import pygame 
from abc import ABC, abstractmethod



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
        self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS = 200 #1500
        self.isGameOver = False

        self.timer = Timer()

    def onEnter(self, game ):
        
        if game.isAI:
            if game.ai.isDone():
                print("Playing last move.")
                self.completed = True
            else:
                self.piece, self.position = game.ai.getNextMove()
        self.isGameOver = game.isGameOver
        self.timer.start(self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS)
        
    

    def update(self, game ):
        if self.isGameOver:
            self.completed = True
        if game.isAI:
            if self.timer.isDone():
                # print("Playing piece: " + str(self.piece) + " At: " + str(self.position))
                game.playPiece(self.piece, self.position)
                self.completed = True



    def onExit(self, game):
        return BoardLogicState()




class GeneratingPiecesState(State):
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.WAIT_TIME = 600 #1000

    def onEnter(self, game ):
        print("New Round!")
        game.newRound()
        self.timer.start(self.WAIT_TIME) 

    def update(self, game ):
        if self.timer.isDone():
            self.completed = True

    def onExit(self, game):
        if game.isAI:
            game.ai.reset(game)
            game.ai.think(game)
        # return DecideGamePlan()
        return GameLogicChecks()
    

class BoardLogicState(State):
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.WAIT_TIME = 500

    def onEnter(self, game ):
        # print("Cleaning Board!")
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
            


