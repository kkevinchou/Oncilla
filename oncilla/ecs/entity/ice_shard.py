import pygame

from lib.ecs.component.physics import PhysicsComponent
from lib.ecs.component.input import KeyboardInputComponent
from lib.ecs.component.shape import RectShapeComponent
from lib.ecs.component.render import AnimationRenderComponent
from lib.ecs.system_manager import SystemManager

from lib.ecs.entity.entity import Entity

from oncilla.ecs.message_types import MESSAGE_TYPE, MESSAGE_TYPE

class IceShard(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, owner, x, y, width, height):
        super(IceShard, self).__init__(x, y)
        self.owner = owner
        self.set_components(self.create_components(width, height))

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'ice_shard',
            'entity': self
        })

    def send_message(self, message):
        if message['message_type'] == MESSAGE_TYPE.COLLISION:
            print message
            other = message['second'] if message['first'] == self else message['first']
            if self.owner == other:
                print 'HIT SELF!'

    def create_components(self, width, height):
        return [
            # RectShapeComponent(self, width, height),
            AnimationRenderComponent(self, 'testsheet', width, height),
            PhysicsComponent(self),
        ]
