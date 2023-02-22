import pygame
import othello.constants as const

# initialization
WINDOW = pygame.display.set_mode((const.WIDTH,const.HEIGHT))
pygame.display.set_caption('Othello')


# main function
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

if __name__ == '__main__':
    main()