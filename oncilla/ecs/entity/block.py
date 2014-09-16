from lib.ecs.component.shape import RectShapeComponent
from lib.ecs.component.render import ShapeRenderComponent, SimpleRenderComponent
from lib.ecs.system_manager import SystemManager
from lib.ecs.entity.entity import Entity
from lib.ecs.component.physics import PhysicsComponent, SkipGravityComponent

from oncilla.ecs.message_types import MESSAGE_TYPE

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

class PinnedBlock(Block):
    system_manager = SystemManager.get_instance()

    def __init__(self, x, y, width, height):
        super(PinnedBlock, self).__init__(x, y, width, height)

    def create_components(self, width, height):
        shape_component = RectShapeComponent(self, width, height)
        render_component = ShapeRenderComponent(shape_component)
        physics_component = PhysicsComponent(self)
        skip_gravity_component = SkipGravityComponent()

        return [shape_component, render_component, physics_component, skip_gravity_component]
