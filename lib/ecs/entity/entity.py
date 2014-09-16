from lib.vec2d import Vec2d

class Entity(object):
    def __init__(self, x, y):
        self.components = {}
        self._position = Vec2d(x, y)

    def __getitem__(self, component_class):
        return self.components[component_class.component_id]

    def set_components(self, components):
        for component in components:
            self.components[component.component_id] = component

    def get(self, component_class):
        return self.components.get(component_class.component_id)

    @property
    def position(self):
        return self._position.copy()

    @position.setter
    def position(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value to position')
        self._position = val.copy()
