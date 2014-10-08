import pygame
import time

from lib.ecs.system.system import System
from lib.vec2d import Vec2d
from lib.ecs.component.render import RenderComponent

from oncilla.ecs.message_types import MESSAGE_TYPE
from oncilla.settings import FRAMES_PER_SECOND, PRINT_FPS

SECONDS_PER_FRAME = 1.0 / FRAMES_PER_SECOND
SECONDS_PER_FPS_DISPLAY = 0.2

class RenderSystem(System):
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()

        self.width, self.height = width, height
        size = width, height
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.entities = []
        self.elapsed_time = 0

        # FPS display settings
        self.font = pygame.font.Font(None, 20)
        self.last_render_time = time.time()
        self.last_fps_render_time = time.time()
        self.fps_elapsed_time = 0
        self.actual_fps = 0

        pygame.display.set_caption('Oncilla')

        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
        }

        super(RenderSystem, self).__init__(message_handlers)

    def clear(self, color=(255, 255, 255)):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def display_actual_fps(self, delta):
        if not PRINT_FPS:
            return

        render_time = time.time()
        time_since_last_render = render_time - self.last_render_time
        self.last_render_time = render_time

        self.fps_elapsed_time += delta
        if self.fps_elapsed_time >= SECONDS_PER_FPS_DISPLAY:
            self.fps_elapsed_time %= SECONDS_PER_FPS_DISPLAY
            self.actual_fps = 1.0 / time_since_last_render

        text = self.font.render('FPS: {:1.2f}'.format(self.actual_fps), 1, (37, 4, 52))
        self.screen.blit(text, (0, 0))

    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(RenderComponent):
            self.entities.append(entity)

    def update(self, delta):
        self.handle_messages()
        self.elapsed_time += delta

        if self.elapsed_time >= SECONDS_PER_FRAME:
            self.clear((171, 218, 237))
            for entity in self.entities:
                render_component = entity[RenderComponent]
                render_component.update(delta)
                render_component.draw(self.screen)

            self.display_actual_fps(delta)
            self.flip()
            self.elapsed_time %= SECONDS_PER_FRAME
