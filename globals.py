from enum import Enum

WINDOW_WIDTH = 1125  # 1/3 Menu, 2/3 DrawingArea
WINDOW_HEIGHT = 750
VIEWPORT_SIZE = 750


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3
