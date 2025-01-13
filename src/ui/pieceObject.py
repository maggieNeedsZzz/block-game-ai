import pygame
import random
import numpy as np

class ColoredRect(pygame.Rect):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color


class PieceObject():
    """
    A class used to represent a piece. To be shown to the player.
    
    Attributes:
        pieceSize (int): The max length the piece can occupy
        piece (np.ndarray): A 2D array representing the shape of the piece
        x (int): The top-left x position of the piece
        y (int): The top-left y position of the piece
        color (tuple, string, optional): The color of the piece
    """
    def __init__(self, pieceSize, piece, x, y, color=None):
        self.rectArray = []
        if color is not None:
            self.color = color
        else:
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.pieceSquareSize = pieceSize//5 
        self.createPiece(piece)
        self.placePiece(x, y)

    def createPiece(self, piece : np.ndarray):
        # pieceSquareSizeY = self.pieceSize//piece.shape[0]
        # pieceSquareSizeX = self.pieceSize//piece.shape[1]
        pieceArray = []
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if piece[i][j]:
                    rect = pygame.Rect((j*self.pieceSquareSize,  i*self.pieceSquareSize, self.pieceSquareSize, self.pieceSquareSize))
                    pieceArray.append(rect)
        self.rectArray = pieceArray



    def placePiece(self, x, y):
        for rect in self.rectArray:
            rect.x += x
            rect.y += y

    def draw(self, screen):
        for rect in self.rectArray:
            pygame.draw.rect(screen, self.color, rect)
