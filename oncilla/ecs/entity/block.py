import pygame
from lib.vec2d import Vec2d

from lib.ecs.component.shape import RectShapeComponent, DefinedShapeComponent
from lib.ecs.component.render import ShapeRenderComponent, PolygonRenderComponent, SpriteRenderComponent
from lib.ecs.system_manager import SystemManager
from lib.ecs.entity.entity import Entity
from lib.ecs.component.physics import PhysicsComponent, SkipGravityComponent, ImmovableComponent

from oncilla.ecs.message_types import MESSAGE_TYPE
from oncilla.collision_types import COLLISION_TYPE

class Block(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, width, height):
        super(Block, self).__init__(x, y, COLLISION_TYPE.COL_BLOCK)

        self.set_components(self.create_components(width, height))

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'block',
            'entity': self
        })

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        render_component = ShapeRenderComponent(shape_component)
        physics_component = PhysicsComponent(self)

        return [shape_component, render_component, physics_component]

class PinnedBlock(Block):
    system_manager = SystemManager.get_instance()

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        render_component = ShapeRenderComponent(shape_component)
        physics_component = PhysicsComponent(self)
        skip_gravity_component = SkipGravityComponent()
        immovable_component = ImmovableComponent()

        return [shape_component, render_component, physics_component, skip_gravity_component, immovable_component]

class WackBlock(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, points):
        super(WackBlock, self).__init__(x, y)
        self.points = points

        self.set_components(self.create_components())

        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'block',
            'entity': self
        })

    def create_components(self):
        shape_component = DefinedShapeComponent(self, self.points)
        render_component = PolygonRenderComponent(self)

        return [shape_component, render_component]

