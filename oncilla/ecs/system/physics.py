import itertools

from lib.vec2d import Vec2d
from lib.ecs.system.system import System
from lib.ecs.component.shape import ShapeComponent
from lib.ecs.component.physics import PhysicsComponent, SkipGravityComponent

from oncilla.ecs.message_types import MESSAGE_TYPE

class PhysicsSystem(System):
    def __init__(self):
        self.entities = []

        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
        }

        super(PhysicsSystem, self).__init__(message_handlers)

    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(ShapeComponent) and entity.get(PhysicsComponent):
            self.entities.append(message['entity'])

    def update(self, delta):
        self.handle_messages()
        self.collisions = []

        for entity in self.entities:
            physics_component = entity[PhysicsComponent]

            if entity.get(SkipGravityComponent):
                if 'Gravity' in physics_component.forces:
                    physics_component.forces.pop('Gravity')
            else:
                physics_component.forces['Gravity'] = Vec2d(0, 100)

            sum_forces = sum([force for force in physics_component.forces.itervalues()])
            if sum_forces == 0:
                sum_forces = Vec2d(0, 0)

            physics_component.acceleration = sum_forces / physics_component.mass
            physics_component.velocity += delta * physics_component.acceleration
            entity.position += delta * physics_component.velocity

        for (entity_a, entity_b) in itertools.product(self.entities, repeat=2):
            if entity_a == entity_b:
                continue

            shape_a = entity_a[ShapeComponent]
            shape_b = entity_b[ShapeComponent]
            print shape_a
