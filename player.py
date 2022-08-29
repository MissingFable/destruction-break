import pygame
import folder_walk
import random
# import necessary libraries

class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, floor_pos):
        super().__init__()
        self.sprite = pygame.image.load('graphics/player.png')
        # get the sprite for the player
        self.image = self.sprite
        # set the player image to the sprite
        self.rect = self.image.get_rect()
        # get rect from image
        self.mask = pygame.mask.from_surface(self.image)
        # get mask from image
        self.position = pygame.math.Vector2(x_pos, floor_pos - self.image.get_width()/2)
        # get the position for the image to be at so it touches the floor

        self.rect.center = self.position
        # move the image to the positoin

        self.speed = 10
        self.angle = 0
        # define speed and angle for the image

        self.input_val = 0
        self.lerp_speed = 0.1
        # define the input value and the lerp speed

        self.sfx = random.choice(folder_walk.get_sfx('sound'))
        # get a random sfx from the sound folder

    def update(self, screen_size, enemy_group, player_group):
        keys = pygame.key.get_pressed()
        self.key_input = keys[pygame.K_d]-keys[pygame.K_a] or keys[pygame.K_RIGHT]-keys[pygame.K_LEFT]
        # check for key input
        self.input_val = self.lerp(self.input_val, self.key_input, self.lerp_speed)
        # lerp from current input to key input

        condition = not (self.rect.left <= 0 and self.input_val < 0) and not (self.rect.right >= screen_size[0] and self.input_val > 0)
        # check if player is trying to exit bounds of screen

        self.position.x += self.input_val * self.speed * condition
        # move the player if the condition is true by the player's input and the speed of the player
        
        self.angle -= (self.input_val * self.speed * condition) % 360
        # change the angle as well.

        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.rect = self.image.get_rect()
        # rotate the image and get a new rectangle

        self.rect.center = self.position
        # move the rectangle to the player's position

        self.mask = pygame.mask.from_surface(self.image)
        # get a new mask for the rotated image

        destroyed_amt = 0
        # define how many items have been destroyed (will indicated proper value soon)

        if pygame.sprite.spritecollide(player_group.sprite, enemy_group, False, pygame.sprite.collide_mask):
            # check for collision with enemy
            self.sfx.play()
            # play sound effect
            with open('destroyed_amt.txt', 'r') as f:
                destroyed_amt = int(f.read())

            with open('destroyed_amt.txt', 'w') as a:
                a.seek(0)
                a.write(str(destroyed_amt + 1))
            
            # change the destroyed amt in the file
    
    def lerp(self, start, end, amt):
        return start + (end - start) * amt
        # lerp formula