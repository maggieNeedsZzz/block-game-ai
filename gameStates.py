from gameLogic import Game
from gameTree import GameState, GameStateWithPlacements


class GameTreeAnalyser:
    leafList = []
    bestLeafScore = -1023
    bestLeaf = None

    @classmethod
    def reset(cls):
        GameTreeAnalyser.leafList = []
        GameTreeAnalyser.bestLeafScore = -1023
        GameTreeAnalyser.bestLeaf = None
        
    @classmethod
    def getLeafStates(cls, treeRootNode : GameState) -> (GameState): 
        print("Score is always: " + str(cls.bestLeafScore))
        cls.findLeafStates(treeRootNode)
        return cls.leafList
    
    @classmethod
    def getBestLeafState(cls, treeRootNode : GameState) -> (GameState, int): 
        cls.findBestLeafState(treeRootNode)
        return cls.bestLeaf, cls.bestLeafScore
    
    @classmethod
    def findBestLeafState(cls, node : GameState): 
        if node.isLeaf() or node.isTerminal():
            if node.score > cls.bestLeafScore:
                cls.bestLeafScore = node.score
                cls.bestLeaf = node
        else:
            for child in node.children:
                cls.findBestLeafState(child)

    @classmethod
    def findLeafStates(cls, node : GameState): 
        if node.isLeaf():
            cls.leafList.append(node)    
        else:
            for child in node.children:
                cls.findLeafStates(child)

    @classmethod
    def getLeafStatesWithoutRepetitions(cls, node : GameState, leafList):
        if node.isLeaf():
            for i, listNode in enumerate(leafList):
                if listNode.board == node.board:
                    found = True
                    if listNode.score < node.score:
                        del leafList[i]
                        leafList.append(node)
                    break
            if not found:
                leafList.append(node)    
        else:
            for child in node.children:
                cls.getLeafStatesWithoutRepetitions(child, leafList)




from enum import Enum
import pygame

class StateEnum(Enum):
    PLAYING = 0
    GENERATING_PIECES = 1
    GAMEOVER = 2


class State():
    def __init__(self):
        self.completed = False
    def handleInput(self, event : pygame.event.Event, game : Game):
        pass
    def update(self, game : Game):
        pass
    def onEnter(self, game : Game):
        pass
    def onExit(self, game : Game):
        pass
    def isCompleted(self):
        return self.completed
    


#### TODO: Can these be class methods???

class GeneratingPiecesState(State):
    def update(self, game : Game):
        game.newRound()
        self.completed = True

    def onExit(self, game):
        return PlayingState()

        
class PlayingState(State):
    def __init__(self):
        super().__init__()
        self.playSequence = []
        self.WAIT_TIME_BETWEEN_PLAYS_MILISECONDS = 1500
        self.isGameOver = False

        # Timer
        self.initTime = 0
        self.currentTime = 0

    def onExit(self, game):
        if self.isGameOver:
            return GameOverState()
        else:
            return GeneratingPiecesState()
    

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

    def onEnter(self, game : Game):
        root = GameStateWithPlacements(game.getBoard(), game.getPlayablePieces(), 0, 0)
        root.generateChildren()
        print("Game tree calculated.")  
        bestLeaf , bestLeafScore = GameTreeAnalyser.getBestLeafState(root)
        self.playSequence = bestLeaf.getSequenceOfPlaysToRoot()
        self.initTime = pygame.time.get_ticks()
        self.isGameOver = bestLeaf.isGameOver
        


class GameOverState(State):
    def onEnter(self, game : Game):
        game.gameOver()
    def update(self, game : Game):
        pass