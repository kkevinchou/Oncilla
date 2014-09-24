import os
import pygame
import json

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
            file_path = os.path.join(self.spritesheets_folder, f)
            filename, extension = os.path.splitext(f)

            if os.path.isfile(file_path) and extension == '.png':
                sheet = pygame.image.load(file_path)
                json_file_path = os.path.join(self.spritesheets_folder, filename + '.json')

                if os.path.isfile(json_file_path):
                    with open(json_file_path, 'r') as json_file:
                        metadata = json.loads(json_file.read())
                else:
                    raise Exception('Exception in ResourceManager: json file for {} not found'.format(filename + extension))

                self.spritesheets[filename] = sheet, metadata

                print ' *** Loaded {}'.format(file_path)


    def get_sprite(self, name):
        return self.sprites.get(name)

    def get_spritesheet(self, name):
        return self.spritesheets.get(name)
