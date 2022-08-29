import pygame
import random

class PhysicsParticle():
    def __init__(self, start_position, speed, angle, gravity_range, direction, opacity_decrease_amt, color = None):
        self.sprite = pygame.image.load('graphics/particle.png')
        self.image = self.sprite
        # get the particle sprite

        if color != None:
            self.image.fill(color)
        # fill the particle with a certain color if started

        self.rect = self.image.get_rect()
        self.rect.topleft = start_position
        # create a rectangle and set the position to the topleft

        self.speed = speed
        self.angle = angle
        self.gravity = random.uniform(gravity_range[0], gravity_range[1])
        # define the particle's speed, angle and gravity

        self.direction = direction
        # define the particle's direction calculated when adding particle to particle list

        self.opacity = 255
        self.opacity_decrease_amt = opacity_decrease_amt
        # define the particle's opacity and the amount to decrease it by each frame
    
    def update(self):
        self.save_pos = self.rect.center
        # save the position of the particle
        
        self.angle -= 5
        self.image = pygame.transform.rotate(self.sprite, self.angle)
        # rotate particle

        self.rect = self.image.get_rect()
        self.rect.center = self.save_pos
        # recenter the particle

        self.direction.y += self.gravity
        self.rect.topleft += self.direction * self.speed
        # move the particle using direction

        self.opacity -= self.opacity_decrease_amt
        self.image.set_alpha(self.opacity)
        # change opacity

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)
        # draw the particle

class Particles:
    def __init__(self, particles = None):
        if particles == None:
            self.particles = []
        else:
            self.particles = particles
        
        # store the particles
    
    def add_particle(self, particle):
        self.particles.append(particle)
        # add particles to stored particles

    def update_and_draw(self, display):
        for p in self.particles:
            p.update()
            p.draw(display)
            # draw and update the particles
    
    def __len__(self):
        return len(self.particles)
        # return length of number of particles