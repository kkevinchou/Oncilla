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
from lib.ecs.system.input import InputSystem
from oncilla.ecs.entity.block import Block, PinnedBlock, WackBlock
from oncilla.ecs.entity.player import PlayerBlock

ENABLE_PROFILING = False

def set_up_systems():
    system_manager = SystemManager.get_instance()

    input_system = InputSystem()
    render_system = RenderSystem(800, 600)
    physics_system = PhysicsSystem()

    system_manager.init([
        input_system,
        physics_system,
        render_system,
    ])

    return system_manager

def run():
    resource_manager = ResourceManager.get_instance()
    system_manager = set_up_systems()

    from lib.ecs.component.physics import PhysicsComponent
    # PinnedBlock(100, 300, 325, 50)
    # PinnedBlock(450, 300, 300, 50)
    PinnedBlock(100, 230, 100, 25)
    # block = Block(0, 200, 50, 50)
    # block[PhysicsComponent].velocity = Vec2d(100, 0)
    PlayerBlock(100, 0, 200, 200)

    # WackBlock(100, 100, [20 * Vec2d(0.5, -0.5), 20 * Vec2d(-0.5, 0.5), 20 * Vec2d(0.5, 1.5), 20 * Vec2d(1.5, 0.5)])
    # WackBlock(100, 100, [20 * Vec2d(1, 0), 20 * Vec2d(0, 1), 20 * Vec2d(1, 2), 20 * Vec2d(2, 1)])

    if ENABLE_PROFILING:
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

    if ENABLE_PROFILING:
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()

if __name__ == '__main__':
    run()
