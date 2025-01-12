 
import numpy as np
# import matplotlib.pyplot as plt
from enum import Enum
import sys
from itertools import permutations
import copy
from gymnasium import spaces
# import gymnasium as gym
import random
import typing


# Name of piece _ horizontal/vertical or up/down _ left/right 
class Piece(spaces.Space):
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

    def __init__(self, shape=None, dtype=None, seed = None, padding = 0):# seedz
        super().__init__(shape, dtype, seed)
        self.padding = padding

        if padding < 5:
            if(padding != 0): # if zero don't pad
                print("The minimum pad is 5! Not padding")
            self.pieces = [Piece.L_H_M,Piece.L_H_N,Piece.L_V_N, Piece.L_V_M, Piece.Corner_U_L, Piece.Corner_U_R, Piece.Corner_D_L, Piece.Corner_D_R, 
                        Piece.ThreeBlock, Piece.TwoBlock, Piece.Five_H_Line, Piece.Five_V_Line, Piece.TwoDiagonalPositive]
                
        else:
            self.setPad(padding)
        

    #Can be uniform or non-uniform sampling based on boundedness of space.
    #mask – A mask used for sampling, expected dtype=np.int8 and see sample implementation for expected shape.
    #returns: A sampled actions from the space
    def sample(self): # #Randomly sample an element of this space.
        index = random.randint(0,len(self.pieces)-1)
        return self.pieces[index]



    def contains(self, x): # Return boolean specifying if x is a valid member of this space.
        #TODO: Type&Shape-Check
        for piece in self.pieces:
            if(np.equal(x,piece)):
                return True
        return False

    def setPad(self, desiredSize):
        self.padding = desiredSize
        self.pieces = []
        _pieces = [Piece.L_H_M,Piece.L_H_N,Piece.L_V_N, Piece.L_V_M, Piece.Corner_U_L, Piece.Corner_U_R, Piece.Corner_D_L, Piece.Corner_D_R, 
                Piece.ThreeBlock, Piece.TwoBlock, Piece.Five_H_Line, Piece.Five_V_Line, Piece.TwoDiagonalPositive]
        for p in _pieces:
            self.pieces.append(self.padPiece(p, self.padding))

    def resetPad(self):
        self.pieces = [Piece.L_H_M,Piece.L_H_N,Piece.L_V_N, Piece.L_V_M, Piece.Corner_U_L, Piece.Corner_U_R, Piece.Corner_D_L, Piece.Corner_D_R, 
                       Piece.ThreeBlock, Piece.TwoBlock, Piece.Five_H_Line, Piece.Five_V_Line, Piece.TwoDiagonalPositive]



    # puts original piece at the top 
    def padPiece(self, piece, desiredSize: int) -> np.ndarray:
        if (piece.shape[0] > desiredSize or piece.shape[1] > desiredSize):
            raise Exception("The minimum pad is 5.")
        piece.resize((desiredSize,desiredSize))
        return piece
    

    '''
    def drawPygamePiece(piece, canvas, pix_square_size, locationCoordinates):
        # maybe use env.np_random though it doesn't make a difference
        color = list(np.random.choice(range(256), size=3))
        pygame.draw.rect(
            canvas,
            color,
            pygame.Rect(
                pix_square_size * locationCoordinates,
                (pix_square_size, pix_square_size),
            ),
        )
    '''


