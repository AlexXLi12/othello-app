import pygame
import othello.constants as const
from othello.classes import *

# initialization
WINDOW = pygame.display.set_mode((const.WIDTH,const.HEIGHT))
pygame.display.set_caption('Othello')

# Create a Square object

squares = []
for k in range(0, const.HEIGHT, const.HEIGHT//8):
    for i in range(0, const.WIDTH, const.WIDTH//8):
        print(i, k)
        square = Square((i, k), const.WIDTH//8)
        WINDOW.blit(square.image, square.rect)
        squares.append(square)
# main function
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        pygame.display.update()

if __name__ == '__main__':
    main()