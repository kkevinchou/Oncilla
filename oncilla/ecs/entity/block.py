import pygame
from lib.vec2d import Vec2d

from lib.ecs.component.shape import RectShapeComponent, DefinedShapeComponent
from lib.ecs.component.render import ShapeRenderComponent, PolygonRenderComponent, SpriteRenderComponent, AnimationRenderComponent
from lib.ecs.system_manager import SystemManager
from lib.ecs.entity.entity import Entity
from lib.ecs.component.physics import PhysicsComponent, SkipGravityComponent
from lib.ecs.component.input import KeyboardInputComponent

from oncilla.ecs.message_types import MESSAGE_TYPE
from oncilla.commands import JumpCommand, MoveLeftCommand, MoveRightCommand

class Block(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, width, height):
        super(Block, self).__init__(x, y)

        self.set_components(self.create_components(width, height))

        Block.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'block',
            'entity': self
        })

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        render_component = ShapeRenderComponent(shape_component)
        physics_component = PhysicsComponent(self)

        return [shape_component, render_component, physics_component]

class PlayerBlock(Block):
    def jump(self):
        self[PhysicsComponent].velocity += Vec2d(0, -450)
        self[AnimationRenderComponent].set_animation('jump')

    def move_left(self):
        self[PhysicsComponent].velocity += Vec2d(-200, 0)

    def move_right(self):
        self[PhysicsComponent].velocity += Vec2d(200, 0)

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        # render_component = ShapeRenderComponent(shape_component)
        # render_component = SpriteRenderComponent(self, 'mite', width, height)
        render_component = AnimationRenderComponent(self, 'testsheet')
        physics_component = PhysicsComponent(self)

        keyboard_input_component = KeyboardInputComponent(self)
        keyboard_input_component.bind(pygame.K_w, JumpCommand())
        keyboard_input_component.bind(pygame.K_a, MoveLeftCommand())
        keyboard_input_component.bind(pygame.K_d, MoveRightCommand())

        return [
            shape_component,
            render_component,
            physics_component,
            keyboard_input_component
        ]

class PinnedBlock(Block):
    system_manager = SystemManager.get_instance()

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        render_component = ShapeRenderComponent(shape_component)
        physics_component = PhysicsComponent(self)
        skip_gravity_component = SkipGravityComponent()

        return [shape_component, render_component, physics_component, skip_gravity_component]

class WackBlock(Entity):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, points):
        super(WackBlock, self).__init__(x, y)
        self.points = points

        self.set_components(self.create_components())

        Block.system_manager.send_message({
            'message_type': MESSAGE_TYPE.CREATE_ENTITY,
            'entity_type': 'block',
            'entity': self
        })

    def create_components(self):
        shape_component = DefinedShapeComponent(self, self.points)
        render_component = PolygonRenderComponent(self)

        return [shape_component, render_component]

