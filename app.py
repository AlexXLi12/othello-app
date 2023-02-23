import pygame
import othello.constants as const
from othello.classes import *

# initialization
WINDOW = pygame.display.set_mode((const.WIDTH,const.HEIGHT))
pygame.display.set_caption('Othello')

#initialize 8x8 board with 64 Square sprites
squares = []
for k in range(0, const.HEIGHT, const.HEIGHT//8):
    for i in range(0, const.WIDTH, const.WIDTH//8):
        print(i, k)
        square = Square((i, k), const.WIDTH//8)
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
                run = False
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
                        square.setColor(colorwheel[playerTurn])
                        square.player = playerTurn
                        playerTurn *= -1
                    #otherwise, color yellow
                    else:
                        square.setColor(const.YELLOW)
                #update square onto window
                WINDOW.blit(square.image, square.rect)
        pygame.display.update()

if __name__ == '__main__':
    main()