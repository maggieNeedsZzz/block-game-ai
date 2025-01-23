import pygame
from game.game import Game
from ui.ui import UI
import numpy as np

def handleInput(ui : UI, event):
    # piece.move_ip(0, 10)
    draggingPiece = False
    pieceShowcase = ui.getUIElementByName("PieceShowcase")
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        # pos = pygame.mouse.get_pos() 
        if pieceShowcase.collidepoint(event.pos):
            offset_x = pieceShowcase.x - mouse_x
            offset_y = pieceShowcase.y - mouse_y
            print("clicked on piece showcase")
            draggingPiece = True
            
    elif event.type == pygame.MOUSEBUTTONUP:
        # pos = pygame.mouse.get_pos()
        print("board corners" + str(pieceShowcase.x), str(pieceShowcase.y))
        
        draggingPiece = False

    elif event.type == pygame.MOUSEMOTION:
        if draggingPiece:
            mouse_x, mouse_y = event.pos
            # print(mouse_x, mouse_y)
            pieceShowcase.x = mouse_x + offset_x
            pieceShowcase.y = mouse_y + offset_y

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True
        elif event.key == pygame.K_1:
            print("pressed 1")







pygame.init()
clock = pygame.time.Clock()

seed = 2
np.random.seed(seed)


game = Game(seed)

running = True
while running:
    game.ui.draw()
    game.update()

    for event in pygame.event.get():        
        exit = handleInput(game.ui, event)
        if exit or event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()