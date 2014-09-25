import unittest
import sys, pygame

from oncilla import settings
from lib.vec2d import Vec2d
from lib.geometry.util import generate_random_polygon, create_polygons
from lib.pathfinding.astar.astarplanner import AStarPlanner
from lib.geometry.polygon import Polygon
from lib.ecs.system_manager import SystemManager
from lib.resource_manager import ResourceManager

from oncilla.ecs.system.render import RenderSystem
from oncilla.ecs.system.physics import PhysicsSystem
from lib.ecs.system.input import InputSystem
from oncilla.ecs.entity.block import Block, PinnedBlock, WackBlock
from oncilla.ecs.entity.player import PlayerBlock

def set_up_systems():
    system_manager = SystemManager.get_instance()

    input_system = InputSystem()
    render_system = RenderSystem(800, 600)
    physics_system = PhysicsSystem()

    system_manager.init([
        render_system,
        physics_system,
        input_system,
    ])

    return system_manager

def run():
    resource_manager = ResourceManager.get_instance()
    system_manager = set_up_systems()

    PinnedBlock(0, 300, 600, 50)
    PlayerBlock(100, 0, 64, 64)

    # WackBlock(100, 100, [20 * Vec2d(0.5, -0.5), 20 * Vec2d(-0.5, 0.5), 20 * Vec2d(0.5, 1.5), 20 * Vec2d(1.5, 0.5)])
    # WackBlock(100, 100, [20 * Vec2d(1, 0), 20 * Vec2d(0, 1), 20 * Vec2d(1, 2), 20 * Vec2d(2, 1)])

    clock = pygame.time.Clock()
    quit = False

    while True:
        if system_manager.update(1 / float(settings.FRAMES_PER_SECOND)) is False:
            sys.exit()

        clock.tick(settings.FRAMES_PER_SECOND)

if __name__ == '__main__':
    run()
