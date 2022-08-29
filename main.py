import pygame
import sys
# needed for pygame to function

from player import Player
from floor import Floor_tile
from enemy import Enemy
from clouds import Cloud
import folder_walk
from timer import Timer
import particle
# scripts and classes part of game

import ui
# import ui script

pygame.init()
# initialize pygame

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Destruction Break")
# creating and titling screen

clock = pygame.time.Clock()
# pygame clock
frame_rate = 60
# pygame frame rate

# Floor:
floor_group = pygame.sprite.Group()
floor_pos = 600

Floor_tile.generate_tiles(screen_size[0], floor_group, floor_pos)

# Player:
player_group = pygame.sprite.GroupSingle()
player_group.add(Player(400, floor_pos))

# Enemy:
enemy_group = pygame.sprite.Group()
Enemy.sprites = folder_walk.get_sprites_as_surface('./graphics/score_obj')
Enemy.generate_positions(screen_size[0])

enemy_death_particles = particle.Particles()
# particles group created for particle strage, updating, drawing

spawn_time = 0.25
enemy_spawn_timer = Timer(spawn_time)
# create spawn timer for enemy

# Clouds:
cloud_group = pygame.sprite.Group()
cloud_amt = 4
for i in range(cloud_amt):
    cloud_group.add(Cloud(screen_size, player_group.sprite.rect.y - player_group.sprite.image.get_width()))

# add as many clouds as specified and ensure they are off screen and won't ever cross the same path as the player

font_name = 'graphics/dogicapixel.ttf'

# Start Menu:
title_text = ui.Text("DESTRUCTION BREAK", pygame.math.Vector2(screen_size[0]/2, 200), (255, 255, 255), font_name, 50, 255, True, (100, 100, 100), pygame.math.Vector2(3, 3))
credits = ui.Text("Made by Setu Marathe in Pygame", pygame.math.Vector2(screen_size[0]/2, 250), (255, 255, 255), font_name, 15)
instructions_text = ui.Text("[Press any key to start. A/D or LEFT/RIGHT to move.]", pygame.math.Vector2(screen_size[0]/2, 625), (255, 255, 255), font_name, 20, 255)
# text for title screen defined using custom text classes

game_has_started = False
# boolean dictates if game has started

destroyed_amt = 0
with open('destroyed_amt.txt', 'r') as f:
    destroyed_amt = int(f.read())
# figure out how many items have been destroyed so far (read txt file)

destroyed_caption = ui.Text("DESTROYED:", pygame.math.Vector2(screen_size[0]/2, 180), (255, 255, 255), font_name, 50, 100)
destroyed_amt_text = ui.Text(str(destroyed_amt), pygame.math.Vector2(screen_size[0]/2, 270), (255, 255, 255), font_name, 100, 100)
# visual for the counter

while True:
    screen.fill((0, 0, 0))
    # fill screen with black

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            sys.exit()
            # check for pygame events

        if event.type == pygame.KEYDOWN:
            game_has_started = True
            # start game once input is received

    if game_has_started:
        # check if game has started. If has, execute code below.
        if enemy_spawn_timer.time_check(frame_rate) == True:
            Enemy.spawn_enemy(enemy_group, floor_pos)
            # spawn enemies using custom Timer object. Check if this returns True and if does, then spawn an enemy

        enemy_group.update(player_group, enemy_group, enemy_death_particles)
        enemy_group.draw(screen)
        # draw and update all enemies
        enemy_death_particles.update_and_draw(screen)
        # draw and update all enemy particles

        title_text.opacity_change(0, 0.3)
        credits.opacity_change(0, 0.3)
        instructions_text.opacity_change(0, 0.3)
        # make title screen UI invisible

        destroyed_amt_text.draw(screen)
        # draw how many items have been destroyed.
        
        destroyed_amt = 0
        
        with open('destroyed_amt.txt', 'r') as f:
            destroyed_amt = f.read()
            destroyed_amt_text.update_text(destroyed_amt)
        
        # continute to update this number each frame

        destroyed_caption.draw(screen)
        # draw the caption which adds context to the destruction counter.

        player_group.update(screen_size, enemy_group, player_group)
        # update the player
        
    player_group.draw(screen)
    # draw the player regardless of if the game has started or not

    floor_group.draw(screen)
    # draw the floor

    if game_has_started == False:
        title_text.draw(screen)
        credits.draw(screen)
        instructions_text.draw(screen)
    # draw everything on the start screen if the game has not started

    cloud_group.update()
    cloud_group.draw(screen)
    # update and draw the clouds

    pygame.display.update()
    clock.tick(frame_rate)
    # update display at frame rate