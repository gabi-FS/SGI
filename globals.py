from enum import Enum

WINDOW_WIDTH = 1125  # 1/3 Menu, 2/3 DrawingArea
WINDOW_HEIGHT = 750
VIEWPORT_SIZE = 750


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3


class TransformationType(Enum):
    TRANSLATION = 1,
    ROTATION = 2,
    SCALING = 3


class RotationType(Enum):
    WORLD_CENTER = 1,
    OBJECT_CENTER = 2,
    AROUND_POINT = 3
