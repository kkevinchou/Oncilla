import pygame

from lib.ecs.component.physics import PhysicsComponent
from lib.ecs.component.input import KeyboardInputComponent
from lib.ecs.component.shape import RectShapeComponent
from lib.ecs.component.render import AnimationRenderComponent
from lib.ecs.system_manager import SystemManager
from lib.ecs.component.character import CharacterComponent

from lib.ecs.entity.entity import Entity

from oncilla.ecs.message_types import MESSAGE_TYPE
from oncilla.ecs.component.player_state import (
    PlayerStateComponent,
    IdlePlayerStateComponent,
    JumpCommand,
    MoveLeftCommand,
    MoveRightCommand,
    IceShardCommand
)

from oncilla.collision_types import COLLISION_TYPE

class PlayerBlock(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, width, height):
        super(PlayerBlock, self).__init__(x, y, COLLISION_TYPE.COL_PLAYER, COLLISION_TYPE.COL_BLOCK)
        self.set_components(self.create_components(width, height))

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'block',
            'entity': self
        })

    def send_message(self, message):
        self[PlayerStateComponent].send_message(message)

    def create_components(self, width, height):
        keyboard_input_component = KeyboardInputComponent(self)
        keyboard_input_component.bind(pygame.K_w, JumpCommand())
        keyboard_input_component.bind(pygame.K_a, MoveLeftCommand())
        keyboard_input_component.bind(pygame.K_d, MoveRightCommand())
        keyboard_input_component.bind(pygame.K_j, IceShardCommand())

        return [
            RectShapeComponent(self, width, height),
            AnimationRenderComponent(self, 'testsheet', width, height),
            PhysicsComponent(self),
            IdlePlayerStateComponent(self),
            keyboard_input_component,
            CharacterComponent(),
        ]
