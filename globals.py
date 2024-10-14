from enum import Enum

WINDOW_WIDTH = 1125  # 1/3 Menu, 2/3 DrawingArea
WINDOW_HEIGHT = 750
VIEWPORT_SIZE = 750


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME_POLYGON = 3
    FILLED_POLYGON = 4
    POLYGON = 5
    BEZIER_CURVE = 6
    BSPLINE_CURVE = 7


class TransformationType(Enum):
    TRANSLATION = (1,)
    ROTATION = (2,)
    SCALING = 3


class RotationType(Enum):
    WORLD_CENTER = (1,)
    OBJECT_CENTER = (2,)
    AROUND_POINT = 3


class TranslationType(Enum):
    WORLD_AXIS = 1
    SCREEN_AXIS = 2


class LineClippingType(Enum):
    LIANG_BARSKY = 1
    COHEN_SUTHERLAND = 2
