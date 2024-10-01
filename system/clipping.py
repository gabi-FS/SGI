from system.basics import Point


class Clipping:

    @staticmethod
    def clip_point(max_p: Point, min_p: Point, point: Point):
        return (min_p.x <= point.x <= max_p.x) and (min_p.y <= point.y <= max_p.y)
