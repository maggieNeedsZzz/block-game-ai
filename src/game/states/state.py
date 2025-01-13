
from enum import Enum
import pygame 
from abc import ABC, abstractmethod

from game.game import Game

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
    def handleInput(self, event : pygame.event.Event, game : Game):
        pass
    @abstractmethod
    def update(self, game : Game):
        pass
    def onEnter(self, game : Game):
        pass
    def onExit(self, game : Game):
        pass
    def isCompleted(self):
        return self.completed
    

class GameOverState(State):
    def onEnter(self, game : Game):
        game.gameOver()
    def update(self, game : Game):
        pass


class PlayingState(State):
    def __init__(self):
        super().__init__()
        self.playSequence = []
        self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS = 1500
        self.isGameOver = False

        # Timer
        self.initTime = 0
        self.currentTime = 0

    def onEnter(self, game : Game):
        print("New Round!")
        root = GameTreeWithPlacements(game.getBoard(), game.getPlayablePieces(), 0, 0)
        root.generateChildren()
        print("Game tree calculated.")  
        bestLeaf , bestLeafScore = GameTreeAnalyser.getBestLeafState(root)
        self.playSequence = bestLeaf.getSequenceOfPlaysToRoot()
        self.initTime = pygame.time.get_ticks()
        self.isGameOver = bestLeaf.isGameOver
        
    

    def update(self, game : Game):
        self.currentTime =  pygame.time.get_ticks() - self.initTime
        if  self.currentTime > self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS:
            self.currentTime = 0
            print("Playing piece: " + str(self.playSequence[0][1]))
            if len(self.playSequence) > 0:
                game.playPiece(self.playSequence[0][0], self.playSequence[0][1])
                self.playSequence.pop(0)
                self.initTime = pygame.time.get_ticks()
                if len(self.playSequence) == 0:
                    self.completed = True
            else:
                self.completed = True


    def onExit(self, game):
        if self.isGameOver:
            return GameOverState()
        else:
            return GeneratingPiecesState()

class GeneratingPiecesState(State):
    def __init__(self):
        super().__init__()
        # Timer
        self.initTime = 0
        self.currentTime = 0

        self.WAIT_TIME = 1000

    def onEnter(self, game : Game):
        print("New Round!")
        self.initTime = pygame.time.get_ticks()

    def update(self, game : Game):
        self.currentTime =  pygame.time.get_ticks() - self.initTime
        if  self.currentTime > self.WAIT_TIME:
            self.initTime = self.currentTime
            self.currentTime = 0
            game.newRound()
            self.completed = True

    def onExit(self, game):
        return PlayingState()