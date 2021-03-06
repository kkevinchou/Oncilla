import itertools

from lib.vec2d import Vec2d
from lib.ecs.system.system import System
from lib.ecs.component.shape import ShapeComponent
from lib.ecs.component.physics import (
    PhysicsComponent,
    SkipGravityComponent,
    ImmovableComponent,
    SkipCollisionResolutionComponent
)
from lib.ecs.component.character import CharacterComponent
from lib.geometry import calculate_separating_vectors
from lib.ecs.system_manager import SystemManager
from lib.physics.force import Force
from lib.ecs.component.state import StateComponent
from lib.quad_tree.quad_tree import QuadTreeNode

from oncilla.ecs.system.reaper import ReaperSystem
from oncilla.ecs.message_types import MESSAGE_TYPE, MESSAGE_TYPE
from oncilla import settings

class PhysicsSystem(System):
    system_manager = SystemManager.get_instance()
    reaper_system = ReaperSystem.get_instance()

    def __init__(self):
        self.entities = []

        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
            MESSAGE_TYPE.DESTROY_ENTITY: self.handle_destroy_entity,
        }

        self.gravity_acceleration = Vec2d(0, 1200)
        self.coefficient_of_friction = 1.5

        super(PhysicsSystem, self).__init__(message_handlers)

    def handle_destroy_entity(self, message):
        entity = message['entity']
        self.reaper_system.queue_reap(self.entities, entity)

    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(PhysicsComponent):
            self.entities.append(message['entity'])
            if not entity.get(SkipGravityComponent):
                entity[PhysicsComponent].forces['Gravity'] = Force(entity[PhysicsComponent].mass * self.gravity_acceleration)

    def find_resolution_vector(self, separating_vectors):
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

        if settings.USE_SPATIAL_PARTITIONING:
            quad_tree = QuadTreeNode(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
            for entity in self.entities:
                quad_tree.add_entity(entity)

            self.system_manager.send_message({
                'message_type': MESSAGE_TYPE.QUAD_TREE,
                'quad_tree': quad_tree,
            })

        for entity in self.entities:
            if entity.get(ImmovableComponent):
                continue

            physics_component = entity[PhysicsComponent]
            physics_component.update_forces(delta)

            if 'Friction' in physics_component.forces:
                friction_force = physics_component.forces['Friction']
                velocity_delta_due_to_friction = delta * friction_force.vector / physics_component.mass

                non_friction_forces = physics_component.get_net_force(exclude_forces=['Friction'])
                non_friction_accel = non_friction_forces / physics_component.mass
                velocity_without_friction = delta * non_friction_accel + physics_component.velocity
                velocity_with_friction = velocity_without_friction + velocity_delta_due_to_friction

                # friction was overly aggressive, time to undo some friction
                if ((velocity_without_friction[0] < 0 and velocity_with_friction[0] >= 0) or
                  (velocity_without_friction[0] > 0 and velocity_with_friction[0] <= 0)):
                    physics_component.velocity = velocity_with_friction
                    physics_component.velocity = Vec2d(0, physics_component.velocity[1])
                    physics_component.forces.pop('Friction')
                else:
                    physics_component.velocity = velocity_with_friction
            else:
                net_force = physics_component.get_net_force()
                physics_component.acceleration = net_force / physics_component.mass
                physics_component.velocity += delta * physics_component.acceleration
            
            entity.position += delta * physics_component.get_total_velocity()

        for entity_a in self.entities:
            overlapping_entities = []

            if entity_a.get(ImmovableComponent):
                continue

            collision_candidates = quad_tree.get_intersections(entity_a) if settings.USE_SPATIAL_PARTITIONING else self.entities
            for entity_b in collision_candidates:
                if entity_a == entity_b:
                    continue

                if entity_a.get(CharacterComponent) and entity_b.get(CharacterComponent):
                    continue

                shape_a = entity_a.get(ShapeComponent)
                shape_b = entity_b.get(ShapeComponent)

                if shape_a is None or shape_b is None:
                    continue

                separating_vectors, overlap = calculate_separating_vectors(shape_a.get_points(), shape_b.get_points())
                entity_a_total_velocity = entity_a[PhysicsComponent].get_total_velocity()

                if overlap and entity_a.collision_mask & entity_b.collision_type:
                    overlapping_entities.append(entity_b)

                    self.system_manager.send_message({
                        'message_type': MESSAGE_TYPE.COLLISION,
                        'collider': entity_a,
                        'collidee': entity_b
                    })

                    if entity_a.get(SkipCollisionResolutionComponent) or entity_b.get(SkipCollisionResolutionComponent):
                        continue

                    resolution_vector = self.find_resolution_vector(separating_vectors)
                    resolution_vector_normalized = resolution_vector.normalized()

                    if resolution_vector_normalized == Vec2d(0, -1):
                        entity_a.send_message({
                            'message_type': MESSAGE_TYPE.LANDED,
                        })

                        entity_a[PhysicsComponent].velocity = Vec2d(entity_a[PhysicsComponent].velocity[0], 0)

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
                                Vec2d(direction_multiplier * entity_a[PhysicsComponent].get_net_force()[1], 0),
                                source=entity_b
                            )
                        elif 'Friction' in entity_a[PhysicsComponent].forces:
                            entity_a[PhysicsComponent].forces.pop('Friction')

                    elif resolution_vector_normalized == Vec2d(0, 1):
                        entity_a[PhysicsComponent].velocity = Vec2d(entity_a[PhysicsComponent].velocity[0], 0)

                    entity_a.position += resolution_vector

            if 'Friction' in entity_a[PhysicsComponent].forces:
                friction_force = entity_a[PhysicsComponent].forces['Friction']
                if friction_force.source not in overlapping_entities:
                    entity_a[PhysicsComponent].forces.pop('Friction')

            if len(overlapping_entities) == 0:
                entity_a.send_message({
                    'message_type': MESSAGE_TYPE.AIRBORNE,
                })
