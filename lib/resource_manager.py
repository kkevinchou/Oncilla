import os
import pygame

from oncilla import settings

class ResourceManager(object):
    instance = None

    def __init__(self):
        self.sprites_folder = None
        self.sprites = {}
        self.spritesheets = {}
        self.sprites_folder = settings.SPRITES_FOLDER
        self.spritesheets_folder = settings.SPRITESHEETS_FOLDER
        self.load_sprites()
        self.load_spritesheets()

    @staticmethod
    def get_instance():
        if ResourceManager.instance is None:
            ResourceManager.instance = ResourceManager()

        return ResourceManager.instance

    def load_sprites(self):
        print ' *** [ResourceManager :: Loading Sprites]'
        for f in os.listdir(self.sprites_folder):
            sprite_path = os.path.join(self.sprites_folder, f)
            if os.path.isfile(sprite_path):
                print ' *** Loaded {}'.format(sprite_path)
                self.sprites[f] = pygame.image.load(sprite_path)

    def load_spritesheets(self):
        print ' *** [ResourceManager :: Loading Sprite Sheets]'
        for f in os.listdir(self.spritesheets_folder):
            spritesheet_path = os.path.join(self.spritesheets_folder, f)
            if os.path.isfile(spritesheet_path):
                self.spritesheets[f] = pygame.image.load(spritesheet_path)
                print ' *** Loaded {}'.format(spritesheet_path)

    def get_sprite(self, sprite):
        return self.sprites.get(sprite)

    def get_spritesheet(self, sprite):
        return self.spritesheets.get(sprite)
