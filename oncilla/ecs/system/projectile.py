from oncilla import settings
from lib.ecs.system.system import System
from oncilla.ecs.message_types import MESSAGE_TYPE
from oncilla.ecs.component.projectile import ProjectileComponent
from oncilla.ecs.system.reaper import ReaperSystem
from lib.ecs.system_manager import SystemManager
from lib.ecs.component.shape import RectShapeComponent

class ProjectileSystem(System):
    reaper_system = ReaperSystem.get_instance()
    system_manager = SystemManager.get_instance()

    def __init__(self):
        self.entities = []
        message_handlers = {
            MESSAGE_TYPE.CREATE_ENTITY: self.handle_create_entity,
            MESSAGE_TYPE.DESTROY_ENTITY: self.handle_destroy_entity,
            MESSAGE_TYPE.COLLISION: self.handle_collision,
        }

        super(ProjectileSystem, self).__init__(message_handlers)

    def handle_destroy_entity(self, message):
        entity = message['entity']
        self.reaper_system.queue_reap(self.entities, entity)
    
    def handle_create_entity(self, message):
        entity = message['entity']
        if entity.get(ProjectileComponent):
            self.entities.append(message['entity'])

    def handle_collision(self, message):
        entity = message['collider']
        if entity in self.entities:
            self.destroy_projectile(entity)

    def destroy_projectile(self, projectile):
        self.system_manager.send_message({
            'message_type': MESSAGE_TYPE.DESTROY_ENTITY,
            'entity': projectile,
        }, immediate=True)

    def update(self, delta):
        self.handle_messages()

        for entity in self.entities:
            rect_shape_component = entity.get(RectShapeComponent)
            if rect_shape_component:
                if (entity.position[0] > settings.SCREEN_WIDTH or entity.position[1] > settings.SCREEN_HEIGHT or
                  entity.position[0] + rect_shape_component.width < 0 or
                  entity.position[1] + rect_shape_component.height < 0):
                    self.destroy_projectile(entity)
            else:
                if (entity.position[0] < 0 or entity.position[0] > setings.SCREEN_WIDTH or
                  entity.position[1] < 0 or entity.position[1] > settings.SCREEN_HEIGHT):
                    self.destroy_projectile(entity)

