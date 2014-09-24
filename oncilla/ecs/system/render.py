import pygame

from lib.ecs.system.system import System
from lib.vec2d import Vec2d
from lib.ecs.component.render import RenderComponent

from oncilla.ecs.message_types import MESSAGE_TYPE

class RenderSystem(System):
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()

        self.width, self.height = width, height
        size = width, height
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.entities = []

        pygame.display.set_caption('Oncilla')

        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
        }

        super(RenderSystem, self).__init__(message_handlers)

    def clear(self, color=(255, 255, 255)):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(RenderComponent):
            self.entities.append(entity)

    def update(self, delta):
        self.handle_messages()
        self.clear((171, 218, 237))

        for entity in self.entities:
            render_component = entity[RenderComponent]
            render_component.update(delta)
            render_component.draw(self.screen)

        self.flip()
