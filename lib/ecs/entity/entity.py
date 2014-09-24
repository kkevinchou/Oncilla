from collections import defaultdict
from lib.vec2d import Vec2d

class Entity(object):
    def __init__(self, x, y):
        self._components = {}
        self._position = Vec2d(x, y)
        self._message_handlers = defaultdict(list)

    def __getitem__(self, component_class):
        return self._components[component_class.component_id]

    def set_components(self, components):
        for component in components:
            for message_type in component.get_message_subscriptions():
                self._message_handlers[message_type].append(component)

            self._components[component.component_id] = component

    def get(self, component_class):
        return self._components.get(component_class.component_id)

    def send_message(self, message):
        for component in self._message_handlers[message['message_type']]:
            component.send_message(message)

    @property
    def position(self):
        return self._position.copy()

    @position.setter
    def position(self, val):
        if not isinstance(val, Vec2d):
            raise ValueError('Assigning non-Vec2d value to position')
        self._position = val.copy()
