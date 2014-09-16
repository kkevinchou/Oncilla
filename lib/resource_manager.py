import os
import pygame

class ResourceManager(object):
    instance = None

    def __init__(self):
        self.sprites_folder = None
        self.sprites = {}

    @staticmethod
    def get_instance():
        if ResourceManager.instance is None:
            ResourceManager.instance = ResourceManager()

        return ResourceManager.instance

    def setup(self, sprites_folder):
        self.sprites_folder = sprites_folder
        self.load_sprites()

    def load_sprites(self):
        print ' *** [ResourceManager :: Loading Sprites]'
        for f in os.listdir(self.sprites_folder):
            sprite_path = os.path.join(self.sprites_folder, f)
            if os.path.isfile(sprite_path):
                print ' *** Loaded {}'.format(sprite_path)
                self.sprites[f] = pygame.image.load(sprite_path)

    def get_sprite(self, sprite):
        return self.sprites.get(sprite)

