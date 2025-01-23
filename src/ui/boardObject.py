
import numpy as np
import pygame
from ui.pieceObject import PieceObject, ColoredRect

class BoardObject():
    def __init__(self, boardSize, boardX, boardY ,rectSize = 100):
        self.rectArray = np.empty((boardSize, boardSize), dtype=pygame.Rect)
        self.occupancy = np.zeros((boardSize, boardSize), dtype=bool)

        self.boardX = boardX
        self.boardY = boardY
        self.rectSize = rectSize


    def setSquare(self, x, y, color):
        self.rectArray[x][y] = ColoredRect(self.boardX +y*self.rectSize, self.boardY +x*self.rectSize, self.rectSize, self.rectSize, color)
        self.occupancy[x][y] = True

        # [i = None if i is None else i for i in self.rectArray[x]]

    # Removes rects and adds new ones (if applicable)
    # Color can be set to None in the case where it is obvious no pieces are being added, just removed
    def update(self, board : np.ndarray, color = None):
        difference = np.logical_xor(self.occupancy, board)
        for i in range(difference.shape[0]):
            for j in range(difference.shape[1]):
                if difference[i][j]:
                    if self.occupancy[i][j]: 
                        self.rectArray[i][j] = None
                    else:
                        if color is None: 
                            print("ERROR: Color is set to None")
                            continue
                        self.setSquare(i,j, color)
        self.occupancy = board.copy()







    def draw(self, screen):
        for line in self.rectArray:
            for rect in line:
                if rect is None: continue
                pygame.draw.rect(screen, rect.color, rect)

