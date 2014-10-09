import pygame

from lib.ecs.component.physics import PhysicsComponent
from lib.ecs.component.input import KeyboardInputComponent
from lib.ecs.component.shape import RectShapeComponent
from lib.ecs.component.render import AnimationRenderComponent
from lib.ecs.system_manager import SystemManager

from lib.ecs.entity.entity import Entity

from oncilla.ecs.message_types import MESSAGE_TYPE
from oncilla.ecs.component.spirit_state import (
    SpiritStateComponent,
)

class Spirit(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, width, height):
        super(Spirit, self).__init__(x, y)
        self.set_components(self.create_components(width, height))

        Spirit.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'spirit',
            'entity': self
        })

    def send_message(self, message):
        self[SpiritStateComponent].send_message(message)

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        render_component = AnimationRenderComponent(self, 'testsheet', width, height)
        physics_component = PhysicsComponent(self)
        state_component = SpiritStateComponent(self)

        # keyboard_input_component = KeyboardInputComponent(self)
        # keyboard_input_component.bind(pygame.K_w, JumpCommand())
        # keyboard_input_component.bind(pygame.K_a, MoveLeftCommand())
        # keyboard_input_component.bind(pygame.K_d, MoveRightCommand())

        return [
            shape_component,
            render_component,
            physics_component,
            state_component,
            # keyboard_input_component
        ]
