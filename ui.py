import pygame
import random
import numpy as np



class ColoredRect(pygame.Rect):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color

class BoardSprite():
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

    def update(self, board, color):
        print(self.occupancy)
        print(board)
        difference = np.logical_xor(self.occupancy, board)
        print(difference)
        for i in range(difference.shape[0]):
            for j in range(difference.shape[1]):
                if difference[i][j]:
                    if self.occupancy[i][j]: 
                        self.rectArray[i][j] = None
                    else:
                        print("Im here")
                        self.setSquare(i,j, color)
        self.occupancy = board.copy()

    def draw(self, screen):
        # for i in range(self.occupancy.shape[0]):
        #     for j in range(self.occupancy.shape[1]):
        #         if self.occupancy[i][j]:
        #             pygame.draw.rect(screen, self.rectArray[i][j].color, self.rectArray[i][j])
        for line in self.rectArray:
            for rect in line:
                if rect is None: continue
                pygame.draw.rect(screen, rect.color, rect)


class PieceSprite():
    def __init__(self, pieceSize):
        self.rectArray = []
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.pieceSquareSize = pieceSize//5 # because

    def createPiece(self, piece : np.ndarray):
        # pieceSquareSizeY = self.pieceSize//piece.shape[0]
        # pieceSquareSizeX = self.pieceSize//piece.shape[1]
        
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if piece[i][j]:
                    rect = pygame.Rect((j*self.pieceSquareSize,  i*self.pieceSquareSize, self.pieceSquareSize, self.pieceSquareSize))
                    self.rectArray.append(rect)


    def placePiece(self, x, y):
        for rect in self.rectArray:
            rect.x += x
            rect.y += y

    def draw(self, screen):
        for rect in self.rectArray:
            pygame.draw.rect(screen, self.color, rect)


class UI():
    def __init__(self):
        ### Screen
        SCREEN_WIDTH = 360
        SCREEN_HEIGHT = 640 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Test")


        ### Board
        BOARD_WIDTH_PERCENT = 85 
        self.boardWidthSize = SCREEN_WIDTH * (BOARD_WIDTH_PERCENT / 100)
        self.boardX = (SCREEN_WIDTH - self.boardWidthSize) / 2
        self.BOARD_Y = self.boardX*3

        # print("board corners" + str(boardX), str(BOARD_Y))
        self.board = pygame.Rect((self.boardX, self.BOARD_Y, self.boardWidthSize, self.boardWidthSize))
        self.boardSquares = BoardSprite(6, self.boardX, self.BOARD_Y, self.boardWidthSize//6)

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
        self.pieceColors = []
        # for i in range(len(self.pieceXPositions)):
        #     self.pieces.append(pygame.Rect((self.pieceXPositions[i], piecesY, pieceSize, pieceSize)))


        ## Score
        self.textFont = pygame.font.SysFont('Arial', 32)
        self.score = self.textFont.render("0", True, "#000000")  



        self.UIElements = {
            "Board": self.board,
            "PieceShowcase": self.pieceShowcase,
            "Pieces": self.pieces,
            "Score": self.score
        }
        self.playablePieces = []
            

    def getUIElementByName(self, name) -> pygame.Rect:
        return self.UIElements[name] if name in self.UIElements else None
    
    def getPlayablePieceColor(self, pieceIndex):
        return self.playablePieces[pieceIndex].color




    ### Define UI elements                    
    def setScore(self, score):
        self.score = self.textFont.render(str(score), True, "#000000")
        # self.screen.blit(self.score, (self.screen/2 - self.score.get_width()/2, 2))


    def setPlayablePieces(self, pieces):
        pieceList = []
        for i, piece in enumerate(pieces):
            pieceSprite = PieceSprite(self.pieceSize)
            pieceSprite.createPiece(piece)
            pieceSprite.placePiece(self.pieceXPositions[i], self.piecesY)
            pieceList.append(pieceSprite)
        self.playablePieces = pieceList

    def removePlayablePiece(self, pieceIndex):
        self.playablePieces.pop(pieceIndex)
    # def setBoardSquares(self, board):
    #     rectArray = []
    #     for i in range(board.shape[0]):
    #         for j in range(board.shape[1]):
    #             if board[i][j]:
    #                 rect = ColoredRect((self.boardX + j*self.boardWidthSize/6, self.BOARD_Y + i*self.boardWidthSize/6, self.boardWidthSize/6, self.boardWidthSize/6), "#000000")
    #                 rectArray.append(rect)
    #     self.boardSquares = board
        

    def updateBoardPiecesWithColor(self, board, color):
        self.boardSquares.update(board, color)



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

    def drawRoundPlayablePieces(self):
        for pieceSprite in self.playablePieces:
            pieceSprite.draw(self.screen)


    def drawPiecesInBoard(self):
        self.boardSquares.draw(self.screen)
        # for rect in self.board:
        #     pygame.draw.rect(self.screen, rect.color, rect)

    def drawScore(self):
        self.screen.blit(self.score, (self.screen.get_width()/2 - self.score.get_width()/2,self.board.topleft[1]/2 - self.score.get_height()/2 ))
        

    ## TODO grid size has to be set in init
    def drawStaticUI(self):
        self.screen.fill("#cdb4db")
        pygame.draw.rect(self.screen,"#bde0fe", self.board)
        self.drawBoardGrid(self.board, 6)
        pygame.draw.rect(self.screen,"#ffafcc", self.pieceShowcase)


    def drawBoardGrid(self, board, gridSize=6):
        blockSize = board.width // gridSize
        # blockSize = 20 #Set the size of the grid block
        for x in range(0, board.width, blockSize):
            for y in range(0, board.height, blockSize):
                rect = pygame.Rect(x + board.x, y + board.y, blockSize, blockSize)
                pygame.draw.rect(self.screen, "#a2d2ff", rect, 1)




