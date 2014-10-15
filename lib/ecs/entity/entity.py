from collections import defaultdict
from lib.vec2d import Vec2d

class Entity(object):
    def __init__(self, x, y, collision_type=0, collision_mask=0):
        self._components = {}
        self._position = Vec2d(x, y)
        self._message_handlers = defaultdict(list)
        self._collision_type = collision_type
        self._collision_mask = collision_mask

    def __getitem__(self, component_class):
        return self._components[component_class.component_id]

    def set_components(self, components):
        for component in components:
            self.set_component(component)

    def set_component(self, component):
        self._components[component.component_id] = component

    def get(self, component_class):
        return self._components.get(component_class.component_id)

    def send_message(self, message):
        pass

    @property
    def collision_type(self):
        return self._collision_type

    @collision_type.setter
    def collision_type(self, val):
        self._collision_type = val

    @property
    def collision_mask(self):
        return self._collision_mask

    @collision_mask.setter
    def collision_mask(self, val):
        self._collision_mask = val

    @property
    def position(self):
        return self._position.copy()

    @position.setter
    def position(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value to position')
        self._position = val.copy()
