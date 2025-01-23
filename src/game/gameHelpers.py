
import random
from game.piece import Pieces

class ScoreCalculator():
    LINE_POINTS = 10
    COMBO_MULTIPLIER = 2

    @classmethod
    def calculateNewScore(cls, currentScore, runningCombo, numberOfLines):
        points = 0
        points += (cls.LINE_POINTS * numberOfLines)
        runningCombo = runningCombo + 1 if points > 0 else runningCombo
        # combo = cls.COMBO_MULTIPLIER if points/10 > 2 else 1 # Dont remember what this is
        return currentScore + (points *  runningCombo), runningCombo
        # return currentScore + (points * combo *  runningCombo), runningCombo


    def calculateNewScoreWithPiece(cls,piece, currentScore, runningCombo, numberOfLines):
        points = 0
        points += (cls.LINE_POINTS * numberOfLines)
        runningCombo = runningCombo + 1 if points > 0 else runningCombo
        points += piece.sum()
        combo = cls.COMBO_MULTIPLIER if points/10 > 2 else 1
        return currentScore + (points * combo *  runningCombo), runningCombo

class PieceGenerator():  
    @staticmethod
    def generatePieces() -> list:   
        return random.sample(Pieces.getPieces(), 3) 

