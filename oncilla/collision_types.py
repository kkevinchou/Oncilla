from lib.enum import enum

COLLISION_TYPE = enum(
    ('COL_PLAYER', 1 << 0),
    ('COL_BLOCK', 1 << 1),
    ('COL_ENEMY', 1 << 2),
    ('COL_PROJECTILE', 1 << 3),
)
