
import random
from game.piece import Pieces

class ScoreCalculator():
    LINE_POINTS = 10
    COMBO_MULTIPLIER = 2

    @classmethod
    def calculateNewScore(cls, currentScore, runningCombo, numberoOfLines):
        points = 0
        points += (cls.LINE_POINTS * numberoOfLines)
        runningCombo = runningCombo + 1 if points > 0 else runningCombo
        combo = cls.COMBO_MULTIPLIER if points/10 > 2 else 1
        return currentScore + (points * combo *  runningCombo), runningCombo

class PieceGenerator():  
    @staticmethod
    def generatePieces() -> list:   
        return random.sample(Pieces.getPieces(), 3) 

