import pygame
import random
import math
import particle
# import necessary libraries

class Enemy(pygame.sprite.Sprite):
    avaiable_positions = []
    total_positions = []
    sprites = []
    sprite_width = None
    refill_amt = None
    closest_positions = []
    # define class objects for positions, sprites, how many positions are able to be refilled, and the closest positions

    def __init__(self, floor_pos, x_pos, pos_index):
        super().__init__()
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # Choose one of the sprites for the enemy. Then, create a rect and collision mask for it.

        self.rect.x = x_pos * self.image.get_width()
        self.rect.centery = floor_pos  - self.image.get_width()/2
        self.pos_index = pos_index
        # place the sprite onto the floor

    def update(self, player_group, enemy_group, enemy_death_particles):
        Enemy.closest_positions = Enemy.get_closestpositions(player_group)
        # update the closest positions by recalculating the closest positions

        for e in enemy_group:
            if pygame.sprite.spritecollide(e, player_group, False, pygame.sprite.collide_mask):
                for i in range(0, 361):
                    angle_vector = pygame.math.Vector2(math.cos(i), math.sin(i)).normalize()
                    if player_group.sprite.key_input != 0:
                        if i % 20 == 0 and angle_vector.y < 0:
                            enemy_death_particles.add_particle(particle.PhysicsParticle(pygame.math.Vector2(e.rect.center), 2, i, [0.05, 0.1], angle_vector, 10, (255, 255, 255)))

                            # Loop through all enemies to see if they are colliding. If so, spawn particles that will rise up first before falling

                enemy_group.remove(e)
                temp_group = pygame.sprite.GroupSingle()
                temp_group.add(e)
                Enemy.avaiable_positions.append(temp_group.sprite.pos_index)
                # once particles are spawned, remove the enemy from the enemy group and add its position to possible positions

    @classmethod
    def get_closestpositions(cls, player_group):
        positions = {}

        for index, pos in enumerate(cls.total_positions):
            distance = abs(pos * cls.sprites[0].get_width() - player_group.sprite.position.x)
            positions.update({distance:index})
            # get closest positions by using subtraction to determine the distance between 2 x values
        
        player_room = math.ceil(player_group.sprite.image.get_width() / cls.sprites[0].get_width())
        # define the room that player occupies (how many cells it occupies)

        positions = {k:v for k, v in sorted(positions.items())}
        return list(positions.values())[:player_room]
        # sort the list from closest to farthest, and add only return those cells that are the closest and are being covered by the tile

    @classmethod
    def spawn_enemy(cls, enemy_group, floor_pos):
        if len(cls.avaiable_positions) > 0 or cls.avaiable_positions is not cls.closest_positions:
            # check if there are any positions that are avaiable that aren't being occupied by the player
            pos = random.choice(cls.avaiable_positions)
            # choose a random position out of the positions that are avaiable

            cls.avaiable_positions.remove(pos)
            enemy_group.add(Enemy(floor_pos, pos, pos))
            # add an enemy to the enemy group and remove its position from the avaiable positions

    @classmethod
    def generate_positions(cls, screen_width):
        cls.refill_amt = math.floor(screen_width/cls.sprites[0].get_width())
        # definte how many positions there are
        cls.avaiable_positions, cls.total_positions = [i for i in range(cls.refill_amt)], [i for i in range(cls.refill_amt)]
        # define how many positions are available and exist in total