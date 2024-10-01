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

    @staticmethod
    def cs_intersection(
        max_p: Point, min_p: Point, point1: Point, point2: Point, point_code: "bin"
    ):
        if point_code & 0b1000:  # point is above the clip window
            x = point1.x + (point2.x - point1.x) * (max_p.y - point1.y) / (
                point2.y - point1.y
            )
            y = max_p.y
        elif point_code & 0b0100:  # point is below the clip window
            x = point1.x + (point2.x - point1.x) * (min_p.y - point1.y) / (
                point2.y - point1.y
            )
            y = min_p.y
        elif point_code & 0b0010:  # point is to the right of clip window
            y = point1.y + (point2.y - point1.y) * (max_p.x - point1.x) / (
                point2.x - point1.x
            )
            x = max_p.x
        elif point_code & 0b0001:  # point is to the left of clip window
            y = point1.y + (point2.y - point1.y) * (min_p.x - point1.x) / (
                point2.x - point1.x
            )
            x = min_p.x
        return Point(x, y)

    @staticmethod
    def cohen_sutherland(
        max_p: Point, min_p: Point, point1: Point, point2: Point
    ) -> tuple[Point, Point]:

        # atribuição de códigos
        region_code = [0b0000, 0b0000]

        for i, p in enumerate([point1, point2]):
            if p.x < min_p.x:
                region_code[i] |= 0b0001  # RC[4] <- 1

            if p.x > max_p.x:
                region_code[i] |= 0b0010  # RC[3] <- 1

            if p.y < min_p.y:
                region_code[i] |= 0b0100  # RC[2] <- 1

            if p.y > max_p.y:
                region_code[i] |= 0b1000  # RC[1] <- 1

        # verificações

        if (
            region_code[0] | region_code[1]
        ) == 0b0000:  # completamente contida na janela
            return (point1, point2)

        if (region_code[0] & region_code[1]) != 0b0000:  # completamente fora da janela
            return None

        if region_code[0] != 0b0000:
            out1 = Clipping.cs_intersection(
                max_p, min_p, point1, point2, region_code[0]
            )
        else:
            out1 = point1

        if region_code[1] != 0b0000:
            out2 = Clipping.cs_intersection(max_p, min_p, out1, point2, region_code[1])
        else:
            out2 = point2

        return (out1, out2)
