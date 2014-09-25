from lib.enum import enum

MESSAGE_TYPE = enum(
    'CREATE_ENTITY',
    'MOVE_ENTITY',
    'INIT_MOVEMENT_PLANNER',
)

ENTITY_MESSAGE_TYPE = enum(
    'JUMPED',
    'LANDED',
    'AIRBORNE'
)
