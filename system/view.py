from objects import GraphicObject, Coordinate


class Window(GraphicObject):
    _size: tuple[int, int]

    def __init__(self, initial_coord: Coordinate, size: tuple[int, int]) -> None:
        self._coords = [initial_coord]
        coord_max = (initial_coord[0] + size[0], initial_coord[1] + size[1])
        self._coords.append(coord_max)
        # coordenadas da window vão ser sempre [(Xmin, Ymin), (Xmax, Ymax)]


class ViewPort:
    _size: tuple[int, int]
    _window: (
        Window  # talvez não seja o ideal, mas a viewport precisa ter acesso à window
    )

    # também dá pra passar como parâmetro
    def __init__(self, initial_coord: Coordinate, size: tuple[int, int]) -> None:
        self._window = Window(initial_coord, size)
        self._size = size

    def transform(self, coord: Coordinate):
        return Coordinate


class DisplayFile:
    _objects: list[GraphicObject]
    _view_port: ViewPort

    def __init__(self, window: Window) -> None:
        self._window = window
