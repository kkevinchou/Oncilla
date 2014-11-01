from lib.ecs.system.system import System
from oncilla.ecs.message_types import MESSAGE_TYPE

class ReaperSystem(System):
    instance = None

    def __init__(self):
        super(ReaperSystem, self).__init__({})
        self.to_reap = []

    @staticmethod
    def get_instance():
        if ReaperSystem.instance is None:
            ReaperSystem.instance = ReaperSystem()

        return ReaperSystem.instance

    def queue_reap(self, container, entity):
        self.to_reap.append((container, entity))

    def update(self, delta):
        if len(self.to_reap) > 0:
            for container, entity in self.to_reap:
                if entity in container:
                    container.remove(entity)

            self.to_reap = []
