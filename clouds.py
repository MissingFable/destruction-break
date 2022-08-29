import pygame
import random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, screen_size, min_height):
        super().__init__()
        self.image = pygame.image.load('graphics/cloud.png')
        self.rect = self.image.get_rect()

        self.screen_size = screen_size
        self.min_height = min_height
        self.image.set_alpha(random.randint(0, 255))

        self.gen_new_pos()
    
    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
           self.gen_new_pos()
    
    def gen_new_pos(self):
        self.height = random.randrange(0, self.min_height)
        self.rect.topleft = pygame.math.Vector2(self.screen_size[0] + random.randrange(20, self.image.get_width() * 3), self.height)
        self.speed = random.randrange(1, 7)
            