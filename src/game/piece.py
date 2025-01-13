 
import numpy as np
# from enum import Enum

# Name of piece _ horizontal/vertical or up/down _ left/right 
class Pieces():
    pieces = {
        "L_H_M": np.asarray([[True,False,False],[True,True,True]]),
        "L_H_N": np.asarray([[False,False,True],[True,True,True]]),
        "L_V_N": np.asarray([[True,False],[True,False],[True,True]]),
        "L_V_M": np.asarray([[False,True],[False,True],[True,True]]),
        "Corner_U_L": np.asarray([[True,True],[True,False]]),
        "Corner_U_R": np.asarray([[True,True],[False,True]]),
        "Corner_D_L": np.asarray([[True,False],[True,True]]),
        "Corner_D_R": np.asarray([[False,True],[True,True]]),
        "ThreeBlock": np.asarray([[True,True,True],[True,True,True],[True,True,True]]),
        "TwoBlock": np.asarray([[True,True],[True,True]]),
        "Five_H_Line": np.asarray([[True,True,True,True,True]]),
        "Five_V_Line": np.asarray([[True],[True],[True],[True],[True]]),
        "TwoDiagonalPositive": np.asarray([[False,True],[True,False]])
    }
    @classmethod
    def getPieces(cls):
        return list(cls.pieces.values())


class PieceEnum:
    L_H_M = np.asarray([[True,False,False],[True,True,True]])
    L_H_N = np.asarray([[False,False,True],[True,True,True]])
    L_V_N = np.asarray([[True,False],[True,False],[True,True]])
    L_V_M = np.asarray([[False,True],[False,True],[True,True]])
    Corner_U_L = np.asarray([[True,True],[True,False]])
    Corner_U_R = np.asarray([[True,True],[False,True]])
    Corner_D_L = np.asarray([[True,False],[True,True]])
    Corner_D_R = np.asarray([[False,True],[True,True]])
    ThreeBlock = np.asarray([[True,True,True],[True,True,True],[True,True,True]])
    TwoBlock = np.asarray([[True,True],[True,True]])
    Five_H_Line = np.asarray([[True,True,True,True,True]])
    Five_V_Line = np.asarray([[True],[True],[True],[True],[True]])
    TwoDiagonalPositive = np.asarray([[False,True],[True,False]])




    



class PaddedPieces():
    def __init__(self, padding = None):
        
        self.pieces = [p.value for p in Pieces]
        if padding != None:
            self.padding = padding
            if padding < 5:
                if(padding != 0): # if zero don't pad
                    print("The minimum pad is 5! Not padding")
                else:
                    paddedPieces = []
                    for p in self.pieces:
                        paddedPieces.append(self.padPiece(p, self.padding))
        

    def __call__(self, *args, **kwds):
        return self.pieces

    # puts original piece at the top 
    def padPiece(self, piece, desiredSize: int) -> np.ndarray:
        if (piece.shape[0] > desiredSize or piece.shape[1] > desiredSize):
            raise Exception("The minimum pad is 5.")
        piece.resize((desiredSize,desiredSize))
        return piece
