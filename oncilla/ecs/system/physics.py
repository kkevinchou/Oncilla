import itertools

from lib.vec2d import Vec2d
from lib.ecs.system.system import System
from lib.ecs.component.shape import ShapeComponent
from lib.ecs.component.physics import PhysicsComponent, SkipGravityComponent, ImmovableComponent
from lib.geometry import calculate_separating_vectors
from lib.physics.force import Force

from oncilla.ecs.message_types import MESSAGE_TYPE, ENTITY_MESSAGE_TYPE

class PhysicsSystem(System):
    def __init__(self):
        self.entities = []

        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
        }

        self.gravity_acceleration = Vec2d(0, 1200)
        self.coefficient_of_friction = 1.5

        super(PhysicsSystem, self).__init__(message_handlers)

    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(ShapeComponent) and entity.get(PhysicsComponent):
            self.entities.append(message['entity'])
            if not entity.get(SkipGravityComponent):
                entity[PhysicsComponent].forces['Gravity'] = Force(entity[PhysicsComponent].mass * self.gravity_acceleration)

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
            physics_component.update_forces(delta)

            # TODO: There's bobbing when we update position, then velocity, then acceleration
            # (which is the right order to do it, i think? do more research on that, then
            # fix the bobbing if necessary)

            if 'Friction' in physics_component.forces:
                friction_force = physics_component.forces['Friction']
                velocity_due_to_friction = delta * friction_force.vector / physics_component.mass

                non_friction_forces = physics_component.get_net_force(exclude_forces=['Friction'])
                non_friction_accel = non_friction_forces / physics_component.mass
                non_friction_velocity_delta = delta * non_friction_accel
                total_delta_velocity = non_friction_velocity_delta + velocity_due_to_friction

                # friction was overly aggressive, time to undo some friction
                if ((total_delta_velocity[0] < 0 and non_friction_velocity_delta[0] >= 0) or
                  (total_delta_velocity[0] > 0 and non_friction_velocity_delta[0] <= 0)):
                    physics_component.velocity += non_friction_velocity_delta + velocity_due_to_friction
                    physics_component.velocity = Vec2d(0, physics_component.velocity[1])
                    physics_component.forces.pop('Friction')
                elif ((total_delta_velocity[0] < 0 and non_friction_velocity_delta[0] < 0) or
                  (total_delta_velocity[0] > 0 and non_friction_velocity_delta[0] > 0)):
                    physics_component.velocity += non_friction_velocity_delta
                    physics_component.forces.pop('Friction')
                else:                
                    physics_component.velocity += non_friction_velocity_delta + velocity_due_to_friction
            else:
                net_force = physics_component.get_net_force()
                physics_component.acceleration = net_force / physics_component.mass
                physics_component.velocity += delta * physics_component.acceleration
            
            entity.position += delta * physics_component.get_total_velocity()

        for (entity_a, entity_b) in itertools.product(self.entities, repeat=2):
            if entity_a == entity_b:
                continue

            if entity_a.get(ImmovableComponent):
                continue

            shape_a = entity_a[ShapeComponent]
            shape_b = entity_b[ShapeComponent]

            separating_vectors, overlap = calculate_separating_vectors(shape_a.get_points(), shape_b.get_points())

            # TODO: this should only be sent after we check against ALL entities
            if not overlap:
                entity_a.send_message({
                    'message_type': ENTITY_MESSAGE_TYPE.AIRBORNE,
                })

            entity_a_total_velocity = entity_a[PhysicsComponent].get_total_velocity()

            if overlap:
                resolution_vector = self.find_resolution_vector(separating_vectors, -1 * entity_a_total_velocity)
                resolution_vector_normalized = resolution_vector.normalized()

                if resolution_vector_normalized == Vec2d(0, -1):
                    entity_a.send_message({
                        'message_type': ENTITY_MESSAGE_TYPE.LANDED,
                    })

                    entity_a[PhysicsComponent].velocity = Vec2d(entity_a[PhysicsComponent].velocity[0], 0)
                    entity_a_total_velocity = entity_a[PhysicsComponent].get_total_velocity()

                    if entity_a[PhysicsComponent].velocity[0] > 0:
                        direction_multiplier = -1
                    elif entity_a[PhysicsComponent].velocity[0] < 0:
                        direction_multiplier = 1
                    else:
                        direction_multiplier = 0

                    if direction_multiplier != 0:
                        entity_a[PhysicsComponent].forces['Friction'] = Force(
                            self.coefficient_of_friction *
                            entity_a[PhysicsComponent].mass *
                            Vec2d(direction_multiplier * entity_a[PhysicsComponent].get_net_force()[1], 0)
                        )
                    elif 'Friction' in entity_a[PhysicsComponent].forces:
                        entity_a[PhysicsComponent].forces.pop('Friction')

                elif resolution_vector_normalized == Vec2d(0, 1):
                    entity_a_total_velocity = Vec2d(entity_a_total_velocity[0], 0)

                entity_a.position += resolution_vector
            elif not overlap:
                if 'Friction' in entity_a[PhysicsComponent].forces:
                    entity_a[PhysicsComponent].velocity -= delta * entity_a[PhysicsComponent].forces['Friction'].vector
                    entity_a.position -= delta * delta * entity_a[PhysicsComponent].velocity
                    entity_a[PhysicsComponent].forces.pop('Friction')
