import pygame
import math
# import neccessary libraries

class Floor_tile(pygame.sprite.Sprite):
    tile_img = pygame.image.load('graphics/floor tile.png')
    # define the image used for the floor

    def __init__(self, position):
        super().__init__()
        self.image = Floor_tile.tile_img
        # define the image used for the floor
        self.rect = self.image.get_rect()
        # define the rect used for the image

        self.rect.topleft = position
        # move the rect to the floor's position
    
    @staticmethod
    def generate_tiles(screen_width, group, floor_pos):
        tile_width = Floor_tile.tile_img.get_width()
        for i in range(math.ceil(screen_width/tile_width)):
            # add enough floor tile so that it covers the entire screen and is not cut short
            group.add(Floor_tile(pygame.math.Vector2(tile_width * i, floor_pos)))
            # add floor to the floor group as long as there is space
