import pygame

from lib.ecs.component.component import Component
from lib.ecs.component.shape import ShapeComponent
from lib.resource_manager import ResourceManager
from lib.geometry.polygon import Polygon
from lib.vec2d import Vec2d

class RenderComponent(Component):
    component_id = 'RenderComponent'

    def update(self, delta):
        pass

    def draw(self, screen, color=(0, 0, 0)):
        raise NotImplementedError()

class SpriteRenderComponent(RenderComponent):
    resource_manager = ResourceManager.get_instance()

    def __init__(self, entity, sprite_file, width, height):
        self.entity = entity
        self.width, self.height = width, height
        self.sprite = SpriteRenderComponent.resource_manager.get_sprite(sprite_file)

    def draw(self, screen):
        screen.blit(self.sprite, self.entity.position)

class AnimationRenderComponent(RenderComponent):
    def __init__(self, entity, spritesheet):
        self.entity = entity
        self.animation = 'idle'
        self.frame = 0
        self.elapsed_time = 0
        self.sprite, self.metadata = SpriteRenderComponent.resource_manager.get_spritesheet(spritesheet)

    def set_animation(self, animation):
        self.animation = animation
        self.frame = 0
        self.elapsed_time = 0

    def update(self, delta):
        self.elapsed_time += delta
        num_frames = self.metadata[self.animation]['num_frames']
        seconds_per_frame = self.metadata[self.animation]['seconds_per_frame']

        while self.elapsed_time > seconds_per_frame:
            self.frame += 1
            self.frame = self.frame % num_frames
            self.elapsed_time -= seconds_per_frame

    def draw(self, screen):
        width = self.metadata[self.animation]['width']
        height = self.metadata[self.animation]['height']

        entity_width = self.entity[ShapeComponent].width
        entity_height = self.entity[ShapeComponent].height
        y = self.metadata[self.animation]['y']

        x_scale = entity_width / 1.0 / width
        y_scale = entity_height / 1.0 / height

        # these frame images should be cached (either at run time, or during init)
        frame_image = pygame.Surface((width, height))
        frame_image.blit(self.sprite, (0, 0), pygame.Rect(self.frame * width, y, width, height))

        screen.blit(pygame.transform.scale(frame_image, (entity_width, entity_height)), self.entity.position)

class ShapeRenderComponent(RenderComponent):
    def __init__(self, shape_component):
        self.shape_component = shape_component
        self.font = pygame.font.Font(None, 15)
        self.agent_prototype = Polygon.rectangular_polygon(64, 64)

    def draw_edges(self, screen, points, color=(155, 155, 10)):
        for point in points:
            pygame.draw.circle(screen, color, (int(point.x), int(point.y)), 3, 3)

            text = self.font.render('[{}, {}]'.format(int(point.x), int(point.y)), 1, (37, 4, 52))
            # screen.blit(text, text.get_rect(centerx=point.x + 30, centery=point.y))

        for i in range(len(points)):
            point_a = points[(i + 1) % len(points)]
            point_b = points[i]
            pygame.draw.line(screen, color, point_a, point_b)

    def draw_c_polygon(self, screen):
        c_polygon_points = self.shape_component.compute_c_polygon(self.agent_prototype).get_points()
        self.draw_edges(screen, c_polygon_points, (98, 200, 156))

    def draw(self, screen):
        color=(0, 115, 115)

        self.draw_edges(screen, self.shape_component.get_points())
        # self.draw_c_polygon(screen)

class PolygonRenderComponent(RenderComponent):
    def __init__(self, entity):
        self.entity = entity

    def draw_lines(self, screen, points, color=(0, 0, 0)):
        for i in range(len(points)):
            point_a = points[(i + 1) % len(points)]
            point_b = points[i]
            pygame.draw.line(screen, color, point_a, point_b)

    def draw(self, screen):
        color=(65, 15, 25)
        self.draw_lines(screen, self.entity[ShapeComponent].get_points())
        # pygame.draw.circle(screen, color, (int(self.entity.position[0]), int(self.entity.position[1])), 3, 3)
    
