import itertools

from lib.vec2d import Vec2d
from lib.ecs.system.system import System
from lib.ecs.component.shape import ShapeComponent
from lib.ecs.component.physics import PhysicsComponent, SkipGravityComponent
from lib.geometry import calculate_separating_vectors

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

    def find_resolution_vector(self, separating_vectors, correction_vector):
        # minimum_correction = 99999
        # min_vec = None
        #
        # correction_vector = correction_vector.normalized()
        #
        # for separating_vector in separating_vectors:
        #     scalar_projection = separating_vector.scalar_projection(correction_vector)
        #     if scalar_projection < minimum_correction and scalar_projection > 0:
        #         minimum_correction = scalar_projection
        #         min_vec = separating_vector
        #
        # return minimum_correction * correction_vector
        # return min_vec

        min_vec = separating_vectors[0]
        min_length =separating_vectors[0].get_length()

        for separating_vector in separating_vectors:
            length = separating_vector.get_length()
            if length < min_length:
                min_vec = separating_vector
                min_length = length

        return min_vec

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

            separating_vectors, overlap = calculate_separating_vectors(shape_a.get_points(), shape_b.get_points())

            if overlap and entity_a[PhysicsComponent].velocity.get_length() > 0:
                resolution_vector = self.find_resolution_vector(separating_vectors, -1 * entity_a[PhysicsComponent].velocity)
                entity_a.position += resolution_vector
                entity_a[PhysicsComponent].velocity = Vec2d(entity_a[PhysicsComponent].velocity[0], 0)
