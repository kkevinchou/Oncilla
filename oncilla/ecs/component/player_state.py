from lib.ecs.component.state import StateComponent
from lib.ecs.component.physics import PhysicsComponent
from lib.ecs.component.render import AnimationRenderComponent
from lib.vec2d import Vec2d
from lib.command import Command
from lib.physics.force import TimedForce
from lib.audio.audio_manager import AudioManager

from lib.enum import enum

from oncilla.ecs.message_types import ENTITY_MESSAGE_TYPE

audio_manager = AudioManager.get_instance()

STATE_ID = enum(
    'IDLE',
    'JUMPING',
    'AIRBORNE',
)

class MoveLeftCommand(Command):
    def execute(self, entity):
        entity[PlayerStateComponent].move_left()

    def undo(self, entity):
        entity[PlayerStateComponent].move_left_stop()

class MoveRightCommand(Command):
    def execute(self, entity):
        entity[PlayerStateComponent].move_right()

    def undo(self, entity):
        entity[PlayerStateComponent].move_right_stop()
        
class JumpCommand(Command):
    def execute(self, entity):
        entity[PlayerStateComponent].jump()

class PlayerStateComponent(StateComponent):
    component_id = 'StateComponent'

    def __init__(self, entity):
        self.entity = entity

    def jump(self):
        pass

    def move_left(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(-200, 0)
        # self.entity[PhysicsComponent].velocity += Vec2d(-200, 0)

    def move_left_stop(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(200, 0)
        if self.state_id != STATE_ID.AIRBORNE:
            if self.entity[PhysicsComponent].velocity[0] > -200:
                self.entity[PhysicsComponent].velocity = Vec2d(-200, 0)
        # self.entity[PhysicsComponent].forces['DriftForce'] = TimedForce(Vec2d(-500, 0), 0.1)

    def move_right(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(200, 0)
        # self.entity[PhysicsComponent].velocity += Vec2d(200, 0)

    def move_right_stop(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(-200, 0)
        if self.state_id != STATE_ID.AIRBORNE:
            if self.entity[PhysicsComponent].velocity[0] < 200:
                self.entity[PhysicsComponent].velocity = Vec2d(200, 0)
        # self.entity[PhysicsComponent].forces['DriftForce'] = TimedForce(Vec2d(500, 0), 0.1)

    def send_message(self, message):
        if message['message_type'] == ENTITY_MESSAGE_TYPE.LANDED:
            if self.state_id == STATE_ID.AIRBORNE:
                self.entity.set_component(IdlePlayerStateComponent(self.entity))
                self.entity[AnimationRenderComponent].set_animation('idle')
        elif message['message_type'] == ENTITY_MESSAGE_TYPE.AIRBORNE:
            if self.state_id != STATE_ID.AIRBORNE:
                self.entity[AnimationRenderComponent].set_animation('jump')
                self.entity.set_component(AirbornePlayerStateComponent(self.entity))

    # def move_left(self):
    #     pass

    # def move_right(self):
    #     pass

    # def jump(self):
    #     pass

class IdlePlayerStateComponent(PlayerStateComponent):
    state_id = STATE_ID.IDLE

    def jump(self):
        audio_manager.play('jump')
        self.entity[PhysicsComponent].velocity = Vec2d(0, -450)
        self.entity[AnimationRenderComponent].set_animation('jump')
        self.entity.set_component(AirbornePlayerStateComponent(self.entity))

# class JumpingPlayerStateComponent(PlayerStateComponent):
#     state_id = STATE_ID.JUMPING

class AirbornePlayerStateComponent(PlayerStateComponent):
    state_id = STATE_ID.AIRBORNE
