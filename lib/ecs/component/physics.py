from lib.ecs.component.component import Component
from lib.vec2d import Vec2d

class PhysicsComponent(Component):
    component_id = 'PhysicsComponent'

    def __init__(self, entity):
        self.entity = entity
        self._velocity = Vec2d(0, 0)
        self._acceleration = Vec2d(0, 0)
        self.mass = 1
        self.forces = {}

    @property
    def velocity(self):
        return self._velocity.copy()

    @velocity.setter
    def velocity(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value to position')
        self._velocity = val.copy()

    @property
    def acceleration(self):
        return self._acceleration.copy()

    @acceleration.setter
    def acceleration(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value to position')
        self._acceleration = val.copy()

class SkipGravityComponent(Component):
    component_id = 'SkipGravity'
