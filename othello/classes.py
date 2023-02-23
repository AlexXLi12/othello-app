import pygame

class Square(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.color = (0,255,0)
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (0,0,0), (0, 0, size, size), width=2)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def update(self):
        pass
    
    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        if x >= self.rect.left and x <= self.rect.right and y >= self.rect.top and y <= self.rect.bottom:
            return True
        return False