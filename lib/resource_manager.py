import os
import pygame
import json
from collections import defaultdict

from oncilla import settings

class ResourceManager(object):
    instance = None

    def __init__(self):
        self.sprites_folder = None
        self.sprites = {}
        self.cached_animations = defaultdict(lambda: defaultdict(dict))
        self.animation_sheets = {}
        self.sprites_folder = settings.SPRITES_FOLDER
        self.animation_sheets_folder = settings.ANIMATION_SHEETS_FOLDER

        self.load_animation_sheets()
        self.load_sprites()

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

    def load_animation_sheets(self):
        print ' *** [ResourceManager :: Loading Animations]'
        for f in os.listdir(self.animation_sheets_folder):
            file_path = os.path.join(self.animation_sheets_folder, f)
            filename, extension = os.path.splitext(f)

            if os.path.isfile(file_path) and extension == '.png':
                sheet = pygame.image.load(file_path)
                json_file_path = os.path.join(self.animation_sheets_folder, filename + '.json')

                if os.path.isfile(json_file_path):
                    with open(json_file_path, 'r') as json_file:
                        metadata = json.loads(json_file.read())
                else:
                    raise Exception('Exception in ResourceManager: json file for {} not found'.format(filename + extension))

                self.animation_sheets[filename] = sheet, metadata
                self.setup_animation(filename, sheet, metadata)

                print ' *** Loaded {}'.format(file_path)

    def get_sprite(self, name):
        return self.sprites.get(name)

    def setup_animation(self, animation_sheet, sheet, metadata):
        for animation, animation_data in metadata.iteritems():
            width = animation_data['width']
            height = animation_data['height']

            animation_frames = []
            for frame_number in range(animation_data['num_frames']):
                animation_frame = pygame.Surface((width, height))
                animation_frame.blit(sheet, (0, 0), pygame.Rect(animation_data['x'] + frame_number * width, animation_data['y'], width, height))
                animation_frames.append(animation_frame)

            self.cached_animations[animation_sheet][animation]['{}x{}'.format(width, height)] = animation_frames, metadata[animation]['seconds_per_frame']

    def get_animations(self, animation_sheet, animation, width, height):
        if not self.cached_animations[animation_sheet][animation].get('{}x{}'.format(width, height)):
            _, metadata = self.animation_sheets[animation_sheet]
            default_width = metadata[animation]["width"]
            default_height = metadata[animation]["height"]
            default_animation_frames, _ = self.cached_animations[animation_sheet][animation]['{}x{}'.format(default_width, default_height)]

            scaled_animation_frames = []
            for default_animation_frame in default_animation_frames:
                scaled_animation_frame = pygame.Surface((width, height))
                scaled_animation_frame.blit(pygame.transform.scale(default_animation_frame, (width, height)), (0, 0))
                scaled_animation_frames.append(scaled_animation_frame)

            self.cached_animations[animation_sheet][animation]['{}x{}'.format(width, height)] = (
                scaled_animation_frames,
                metadata[animation]['seconds_per_frame']
            )

        return self.cached_animations[animation_sheet][animation]['{}x{}'.format(width, height)]
