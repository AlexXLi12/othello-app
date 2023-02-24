import pygame
from .constants import BLACK, GREEN, WHITE

class Square(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        """_summary_

        Args:
            pos (_type_): _description_
            size (_type_): _description_
        """
        super().__init__()
        self.pos = pos
        self.color = GREEN
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)
        pygame.draw.rect(self.image, BLACK, (0, 0, size, size), width=2)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.player = 0 # -1 = black, 0 = empty, 1 = white
    
    def update(self):
        pass
    
    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        if x >= self.rect.left and x <= self.rect.right and y >= self.rect.top and y <= self.rect.bottom:
            return True
        return False

    def setColor(self, color):
        #make square the color
        self.color = color
        self.image.fill(color)
        #redraw border
        pygame.draw.rect(self.image, BLACK, (0, 0, self.size, self.size), width=2)
    
    """
    Place player's colored piece on square, update square's player status
    """
    def placePiece(self, playerNum):
        color = BLACK if playerNum == -1 else WHITE
        self.player = playerNum
        pygame.draw.circle(self.image, color, (self.size//2, self.size//2), self.size//3)
