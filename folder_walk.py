from os import walk
import pygame
from pygame import mixer

def get_sprites_as_surface(path):
    surfaces = []

    for a, b, images in walk(path):
        for img in images:
            full_path = path + "/" + img
            img_file = pygame.image.load(full_path)
            surfaces.append(img_file)
    
    return surfaces
    # Walk through the folder for images and turn them into surfaces. Then return them.

def get_sfx(path):
    sounds = []

    for a, b, images in walk(path):
        for img in images:
            full_path = path + "/" + img
            song_file = pygame.mixer.Sound(full_path)
            sounds.append(song_file)
    
    return sounds
    # Walk through the folder for sounds and turn them into pygame sounds. Then return them.