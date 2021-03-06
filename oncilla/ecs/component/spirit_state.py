from lib.ecs.component.state import StateComponent
from lib.ecs.component.physics import PhysicsComponent
from lib.ecs.component.render import AnimationRenderComponent
from lib.vec2d import Vec2d
from lib.command import Command
from lib.physics.force import TimedForce
from lib.audio.audio_manager import AudioManager

from lib.enum import enum

from oncilla.ecs.message_types import MESSAGE_TYPE

audio_manager = AudioManager.get_instance()

STATE_ID = enum(
    'IDLE',
    'JUMPING',
    'AIRBORNE',
)

class MoveLeftCommand(Command):
    def execute(self, entity):
        entity[SpiritStateComponent].move_left()

    def undo(self, entity):
        entity[SpiritStateComponent].move_left_stop()

class MoveRightCommand(Command):
    def execute(self, entity):
        entity[SpiritStateComponent].move_right()

    def undo(self, entity):
        entity[SpiritStateComponent].move_right_stop()
        
class JumpCommand(Command):
    def execute(self, entity):
        entity[SpiritStateComponent].jump()

class SpiritStateComponent(StateComponent):
    def __init__(self, entity):
        self.entity = entity

    def jump(self):
        pass

    def apply_move_left_momemtum(self):
        pass

    def apply_move_right_momemtum(self):
        pass

    def move_left(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(-200, 0)

    def move_left_stop(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(200, 0)
        self.apply_move_left_momemtum()

    def move_right(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(200, 0)

    def move_right_stop(self):
        self.entity[PhysicsComponent].movement_velocity += Vec2d(-200, 0)
        self.apply_move_right_momemtum()

    # message_handlers

    def handle_airborne(self, message):
        pass

    def handle_landed(self, message):
        pass

    def send_message(self, message):
        if message['message_type'] == MESSAGE_TYPE.LANDED:
            self.handle_landed(message)
        elif message['message_type'] == MESSAGE_TYPE.AIRBORNE:
            self.handle_airborne(message)

class IdleSpiritStateComponent(SpiritStateComponent):
    state_id = STATE_ID.IDLE

    def apply_move_left_momemtum(self):
        if self.entity[PhysicsComponent].velocity[0] > -200:
            self.entity[PhysicsComponent].velocity = Vec2d(-200, 0)

    def apply_move_right_momemtum(self):
        if self.entity[PhysicsComponent].velocity[0] < 200:
            self.entity[PhysicsComponent].velocity = Vec2d(200, 0)

    def jump(self):
        # audio_manager.play('jump')
        self.entity[PhysicsComponent].velocity = Vec2d(0, -450)
        self.entity[AnimationRenderComponent].set_animation('jump')
        self.entity.set_component(AirborneSpiritStateComponent(self.entity))

    def handle_airborne(self, message):
        self.entity[AnimationRenderComponent].set_animation('jump')
        self.entity.set_component(AirborneSpiritStateComponent(self.entity))

class AirborneSpiritStateComponent(SpiritStateComponent):
    state_id = STATE_ID.AIRBORNE

    def handle_landed(self, message):
        self.entity.set_component(IdleSpiritStateComponent(self.entity))
        self.entity[AnimationRenderComponent].set_animation('idle')
