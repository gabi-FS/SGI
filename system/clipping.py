from system.basics import Point


class Clipping:

    @staticmethod
    def clip_point(max_p: Point, min_p: Point, point: Point):
        return (min_p.x <= point.x <= max_p.x) and (min_p.y <= point.y <= max_p.y)

    # line clipping
    @staticmethod
    def liam_barsky(
        max_p: Point, min_p: Point, point1: Point, point2: Point
    ) -> tuple[Point, Point]:
        dx = point2.x - point1.x
        dy = point2.y - point1.y

        p = [-dx, dx, -dy, dy]
        q = [
            point1.x - min_p.x,
            max_p.x - point1.x,
            point1.y - min_p.y,
            max_p.y - point1.y,
        ]

        u1, u2 = 0.0, 1.0

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None  # Line is parallel and outside the window, reject it
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u, u1)
                else:
                    u2 = min(u, u2)

        if u1 > u2:
            return None  # Line is completely outside the window, reject it
        else:
            x0_clip = point1.x + u1 * dx
            y0_clip = point1.y + u1 * dy
            x1_clip = point1.x + u2 * dx
            y1_clip = point1.y + u2 * dy

            return (Point(x0_clip, y0_clip), Point(x1_clip, y1_clip))
