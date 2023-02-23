import pygame, sys
import othello.constants as const
from othello.classes import *

# initialization
WINDOW = pygame.display.set_mode((const.WIDTH,const.HEIGHT))
pygame.display.set_caption('Othello')

#initialize 8x8 board with 64 Square sprites
squares = []
for k in range(0, const.HEIGHT, const.HEIGHT//8):
    for i in range(0, const.WIDTH, const.WIDTH//8):
        square = Square((i, k), const.WIDTH//8)
        #starting position
        if k//(const.HEIGHT//8) == 3:
            if i//(const.WIDTH//8) == 3:
                square.placePiece(1)
            elif i//(const.WIDTH//8) == 4:
                square.placePiece(-1)
        if k//(const.HEIGHT//8) == 4:
            if i//(const.WIDTH//8) == 3:
                square.placePiece(-1)
            if i//(const.WIDTH//8) == 4:
                square.placePiece(1)
        WINDOW.blit(square.image, square.rect)
        squares.append(square)

"""
if playerTurn =-1, color = colorwheel[-1] = const.BLACK;
if playerTurn = 1, color = colorwheel[1] = const.WHITE;
"""
colorwheel = [0,const.WHITE, const.BLACK] 

# main function
def main():
    clock = pygame.time.Clock()
    run = True
    mouseDown = False
    playerTurn = -1
    while run:
        mouseDown = False
        clock.tick(30)
        #process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
        #loop over squares and check for mouse actions
        for square in squares:
            if square.player == 0:
                square.setColor(const.GREEN)
                #if mouse is hovered over square
                if square.rect.collidepoint(pygame.mouse.get_pos()):
                    #if mouse is hovered over square AND mouseDown, place a piece
                    if mouseDown:
                        square.placePiece(playerTurn)
                        playerTurn *= -1
                    #otherwise, color yellow
                    else:
                        square.setColor(const.YELLOW)
                #update square onto window
                WINDOW.blit(square.image, square.rect)
        pygame.display.update()

if __name__ == '__main__':
    main()