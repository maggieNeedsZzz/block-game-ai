import pygame
from ui.boardObject import BoardObject
from ui.pieceObject import PieceObject
from game.observer import Observer

class StaticUI():
    def __init__(self):
        pass
import math

import numpy as np

class UI(Observer):
    def __init__(self, boardCellWidth = 6):
        super().__init__()
        ### Screen
        SCREEN_WIDTH = 360
        SCREEN_HEIGHT = 640 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Test")

        self.boardCellWidth = boardCellWidth



        ### Board
        BOARD_WIDTH_PERCENT = 85 
        self.boardWidthSize = SCREEN_WIDTH * (BOARD_WIDTH_PERCENT / 100)
        self.boardX = (SCREEN_WIDTH - self.boardWidthSize) / 2
        self.BOARD_Y = self.boardX*3

        # print("board corners" + str(boardX), str(BOARD_Y))
        self.board = pygame.Rect((self.boardX, self.BOARD_Y, self.boardWidthSize, self.boardWidthSize))



        ### Piece Showcase
        PIECE_SHOWCASE_HEIGHT_PERCENT = 50
        bottomOfBoard = self.BOARD_Y + self.boardWidthSize
        remainingYSpace = SCREEN_HEIGHT - bottomOfBoard 
        pieceShowcaseHeightSize = remainingYSpace * (PIECE_SHOWCASE_HEIGHT_PERCENT / 100)
        pieceShowcaseY = bottomOfBoard + (remainingYSpace - pieceShowcaseHeightSize)/2
        PIECE_SHOWCASE_X = self.boardX
        
        self.pieceShowcase = pygame.Rect((PIECE_SHOWCASE_X, pieceShowcaseY, self.boardWidthSize, pieceShowcaseHeightSize))



        ### Pieces
        NUMBER_OF_PIECES = 3
        PADDING_BETWEEN_PIECES = 10 # TODO needs to be set dynamically
        pieceShowcaseLength = self.boardWidthSize
        self.pieceSize = (pieceShowcaseLength - 2*PADDING_BETWEEN_PIECES)/NUMBER_OF_PIECES

        self.pieceXPositions = []
        for i in range(NUMBER_OF_PIECES):
            self.pieceXPositions.append((PIECE_SHOWCASE_X + i*(self.pieceSize + PADDING_BETWEEN_PIECES)))

        self.piecesY = pieceShowcaseY + (pieceShowcaseHeightSize - self.pieceSize)/2

        self.pieces = []
        # self.pieceColors = []
        # for i in range(len(self.pieceXPositions)):
        #     self.pieces.append(pygame.Rect((self.pieceXPositions[i], piecesY, pieceSize, pieceSize)))




        # Static UI
        self.UIElements = {
            "Board": self.board,
            "PieceShowcase": self.pieceShowcase,
            "Pieces": self.pieces,
            # "Score": self.score
        }

        
        # Score
        self.textFont = pygame.font.SysFont('Arial', 32)
        self.score = self.textFont.render("0", True, "#000000")  
        ## Board Content
        self.boardSquares = BoardObject(boardCellWidth, self.boardX, self.BOARD_Y, self.boardWidthSize//boardCellWidth)
        ## Pieces to Play
        self.playablePieces = []
            

    def getUIElementByName(self, name) -> pygame.Rect:
        return self.UIElements[name] if name in self.UIElements else None
    
    def getPlayablePieceColor(self, pieceIndex):
        return self.playablePieces[pieceIndex].color


    def onNotify(self, game, event):

        if event == "newRound":
            pieceList = []
            for i, piece in enumerate(game.playablePieces):
                pieceSprite = PieceObject(self.pieceSize, piece, self.pieceXPositions[i], self.piecesY)
                pieceList.append(pieceSprite)
                self.playablePieces = pieceList

        elif event == "piecePlayed":
            colorToAdd, idx = self._findMissingPiece(game)
            self.boardSquares.update(game.board.getBoard(), colorToAdd)
            self.playablePieces.pop(idx)

        elif event == "logicDone":
            self.boardSquares.update(game.board.getBoard())
            self.score = self.textFont.render(str(game.score), True, "#000000")

    def _findMissingPiece(self, game):
        colorToAdd = None
        idx = 0
        for pieceObject in self.playablePieces:
            if not any(np.array_equal(pieceObject.piece, piece) for piece in game.playablePieces):
                colorToAdd = pieceObject.color
                return colorToAdd, idx
            idx += 1
        print("ERROS: Something is ")
        return 


    ### Define UI elements                    
    # def setScore(self, score):
        # self.score = self.textFont.render(str(score), True, "#000000")
        # self.screen.blit(self.score, (self.screen/2 - self.score.get_width()/2, 2))



    # def removePlayablePiece(self, pieceIndex):
    #     self.playablePieces.pop(pieceIndex)
        





    ### Draw calls
    # def drawPieceOnBoard(self, piece, position ):
    #     whole = []
    #     for i in range(piece.shape[0]):
    #         for j in range(piece.shape[1]):
    #             pieceSquareSize = self.boardWidthSize//6
    #             if piece[i][j]:
    #                 blah = pygame.Rect((self.boardX + position[1]*pieceSquareSize + i*pieceSquareSize, self.BOARD_Y + position[0]*pieceSquareSize + j*pieceSquareSize , pieceSquareSize,pieceSquareSize))
    #                 whole.append(blah)
    #     for blah in whole:
    #         pygame.draw.rect(self.screen, (0,0,0), blah)

    def drawPlayablePieces(self):
        for pieceSprite in self.playablePieces:
            pieceSprite.draw(self.screen)

    def drawBoardPieces(self):
        self.boardSquares.draw(self.screen)

    def drawScore(self):
        self.screen.blit(self.score, (self.screen.get_width()/2 - self.score.get_width()/2,self.board.topleft[1]/2 - self.score.get_height()/2 ))
        

    ## TODO grid size has to be set in init
    def drawStaticUI(self):
        self.screen.fill("#cdb4db")
        pygame.draw.rect(self.screen,"#bde0fe", self.board)
        self.drawBoardGrid(self.board, self.boardCellWidth)
        pygame.draw.rect(self.screen,"#ffafcc", self.pieceShowcase)


    def drawBoardGrid(self, board, gridSize=6):
        blockSize = math.ceil( board.width/ gridSize) #board.width // gridSize
        
        # blockSize = 20 #Set the size of the grid block
        for x in range(0, board.width, blockSize):
            for y in range(0, board.height, blockSize):
                rect = pygame.Rect(x + board.x, y + board.y, blockSize, blockSize)
                pygame.draw.rect(self.screen, "#a2d2ff", rect, 1)

    def draw(self):
        self.drawStaticUI()

        self.drawScore()
        self.drawPlayablePieces()
        self.drawBoardPieces()



