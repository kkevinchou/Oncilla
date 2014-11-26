import time
import unittest
import sys, pygame
import cProfile, pstats, StringIO

from oncilla import settings
from lib.vec2d import Vec2d
from lib.geometry.util import generate_random_polygon, create_polygons
from lib.pathfinding.astar.astarplanner import AStarPlanner
from lib.geometry.polygon import Polygon
from lib.ecs.system_manager import SystemManager
from lib.resource_manager import ResourceManager

from oncilla.ecs.system.render import RenderSystem
from oncilla.ecs.system.physics import PhysicsSystem
from oncilla.ecs.system.projectile import ProjectileSystem
from oncilla.ecs.system.reaper import ReaperSystem
from lib.ecs.system.input import InputSystem
from oncilla.ecs.entity.block import Block, PinnedBlock, WackBlock
from oncilla.ecs.entity.player import PlayerBlock
from oncilla.ecs.entity.spirit import Spirit

def set_up_systems():
    system_manager = SystemManager.get_instance()

    system_manager.init([
        InputSystem(),
        PhysicsSystem(),
        ProjectileSystem(),
        ReaperSystem.get_instance(),
        RenderSystem(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
    ])

    return system_manager

def run():
    resource_manager = ResourceManager.get_instance()
    system_manager = set_up_systems()

    from lib.ecs.component.physics import PhysicsComponent
    # PinnedBlock(100, 230, 100, 25)
    # PinnedBlock(400, 230, 100, 25)
    PinnedBlock(150, 300, 500, 25)
    PlayerBlock(200, 200, 64, 64)
    # Spirit(500, 0, 64, 64)
    # PinnedBlock(503, 230, 100, 25)
    # PlayerBlock(503, 0, 200, 200)

    # p2 = PlayerBlock(301, 31, 200, 200)
    # p2.set_components([ImmovableComponent()])

    # WackBlock(100, 100, [20 * Vec2d(0.5, -0.5), 20 * Vec2d(-0.5, 0.5), 20 * Vec2d(0.5, 1.5), 20 * Vec2d(1.5, 0.5)])
    # WackBlock(100, 100, [20 * Vec2d(1, 0), 20 * Vec2d(0, 1), 20 * Vec2d(1, 2), 20 * Vec2d(2, 1)])

    if settings.ENABLE_PROFILING:
        pr = cProfile.Profile()
        pr.enable()

    max_frame_time = 0.25
    fixed_update_dt = 0.01
    accumulated_time = 0
    current_time = time.time()
    last_render_time = 0
    game_over = False

    while not game_over:
        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time

        if frame_time >= max_frame_time:
            frame_time = max_frame_time

        accumulated_time += frame_time

        while accumulated_time >= fixed_update_dt:
            accumulated_time -= fixed_update_dt
            if system_manager.update(fixed_update_dt) is False:
                game_over = True

    if settings.ENABLE_PROFILING:
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()

if __name__ == '__main__':
    run()
