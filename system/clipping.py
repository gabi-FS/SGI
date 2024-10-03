from math import inf

from globals import LineClippingType
from system.basics import Point


class Clipping:
    line_type: LineClippingType

    def __init__(self, line_type) -> None:
        self.line_type = line_type

    @staticmethod
    def clip_point(max_p: Point, min_p: Point, point: Point):
        return (min_p.x <= point.x <= max_p.x) and (min_p.y <= point.y <= max_p.y)

    def clip_line(self, max_p: Point, min_p: Point, point1: Point, point2: Point) -> tuple[Point, Point]:
        if LineClippingType.LIANG_BARSKY == self.line_type:
            return Clipping.liam_barsky(max_p, min_p, point1, point2)
        else:
            return Clipping.cohen_sutherland(max_p, min_p, point1, point2)

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
    def compute_cs_code(max_p: Point, min_p: Point, point1: Point):
        # atribuição de códigos
        region_code = 0b0000

        if point1.x < min_p.x:
            region_code |= 0b0001  # RC[4] <- 1
        elif point1.x > max_p.x:
            region_code |= 0b0010  # RC[3] <- 1
        if point1.y < min_p.y:
            region_code |= 0b0100  # RC[2] <- 1
        elif point1.y > max_p.y:
            region_code |= 0b1000  # RC[1] <- 1

        return region_code

    @staticmethod
    def cohen_sutherland(
            max_p: Point, min_p: Point, point1: Point, point2: Point
    ) -> tuple[Point, Point]:

        # verificações
        region_code1 = Clipping.compute_cs_code(max_p, min_p, point1)
        region_code2 = Clipping.compute_cs_code(max_p, min_p, point2)

        result = None
        while True:
            if (
                    region_code1 | region_code2
            ) == 0b0000:  # completamente contida na janela
                result = (point1, point2)
                break

            elif (region_code1 & region_code2) != 0b0000:  # completamente fora da janela
                result = None
                break

            else:
                region_out_code = region_code2 if region_code2 > region_code1 else region_code1

                if region_out_code & 0b1000:  # point is above the clip window
                    x = point1.x + (point2.x - point1.x) * (max_p.y - point1.y) / (
                        point2.y - point1.y
                    )
                    y = max_p.y
                elif region_out_code & 0b0100:  # point is below the clip window
                    x = point1.x + (point2.x - point1.x) * (min_p.y - point1.y) / (
                        point2.y - point1.y
                    )
                    y = min_p.y
                elif region_out_code & 0b0010:  # point is to the right of clip window
                    y = point1.y + (point2.y - point1.y) * (max_p.x - point1.x) / (
                        point2.x - point1.x
                    )
                    x = max_p.x
                elif region_out_code & 0b0001:  # point is to the left of clip window
                    y = point1.y + (point2.y - point1.y) * (min_p.x - point1.x) / (
                        point2.x - point1.x
                    )
                    x = min_p.x

                if region_out_code == region_code1:
                    point1 = Point(x, y)
                    region_code1 = Clipping.compute_cs_code(max_p, min_p, point1)
                else:
                    point2 = Point(x, y)
                    region_code2 = Clipping.compute_cs_code(max_p, min_p, point2)

        return result

    # Sutherland-Hodgeman
    @staticmethod
    def clip_polygon(points: list[Point], max_p: Point, min_p: Point):
        # Deve transformar os pontos em linhas da face
        n_points = len(points)
        clipped_lines = [(points[i], points[(i + 1) % n_points]) for i in range(n_points)]
        clipped_lines_temp = []
        # Fazer para cada borda
        for edge in ["l", "r", "t", "b"]:
            for line in clipped_lines:
                first_inside = Clipping.is_inside(line[0], max_p, min_p, edge)
                second_inside = Clipping.is_inside(line[1], max_p, min_p, edge)

                if first_inside and second_inside:
                    clipped_lines_temp.append(line)
                elif first_inside:
                    intersection = Clipping.intersection(line, max_p, min_p, "first", edge)
                    clipped_lines_temp.append(intersection)
                elif second_inside:
                    intersection = Clipping.intersection(line, max_p, min_p, "second", edge)
                    clipped_lines_temp.append(intersection)

            # Fazer o "patch de linhas"
            n_temp_lines = len(clipped_lines_temp)
            for i in range(n_temp_lines):
                if i < len(clipped_lines_temp) - 1:
                    if clipped_lines_temp[i][1] != clipped_lines_temp[i + 1][0]:
                        clipped_lines_temp.insert(i + 1,
                                                  [clipped_lines_temp[i][1], clipped_lines_temp[i + 1][0]])
                else:
                    if clipped_lines_temp[i][1] != clipped_lines_temp[0][0]:
                        clipped_lines_temp.append([clipped_lines_temp[i][1], clipped_lines_temp[0][0]])

            clipped_lines = clipped_lines_temp.copy()
            clipped_lines_temp.clear()

        return clipped_lines

    @staticmethod
    def is_inside(point: Point, max_p: Point, min_p: Point, edge: str):
        # print(point)
        # print(min_p)
        match edge:
            case "l":
                return point.x > min_p.x
            case "r":
                return point.x < max_p.x
            case "t":
                return point.y < max_p.y
            case "b":
                return point.y > min_p.y

    @staticmethod
    def intersection(line: tuple[Point], max_p: Point, min_p: Point, which_inside: str, edge: str):
        """ which point: first | second """

        angular_coeff = inf
        if (line[1].x - line[0].x) != 0:
            angular_coeff = (line[1].y - line[0].y) / (line[1].x - line[0].x)

        if which_inside == "first":
            point = line[0]
        else:
            point = line[1]

        match edge:
            case "l":
                new_x = min_p.x
                new_y = angular_coeff * (min_p.x - point.x) + point.y
            case "r":
                new_x = max_p.x
                new_y = angular_coeff * (max_p.x - point.x) + point.y
            case "t":
                new_x = point.x + (1.0 / angular_coeff) * (max_p.y - point.y)
                new_y = max_p.y
            case "b":
                new_x = point.x + (1.0 / angular_coeff) * (min_p.y - point.y)
                new_y = min_p.y

        new_point = Point(new_x, new_y)

        if which_inside == "first":
            return (line[0], new_point)
        else:
            return (new_point, line[1])
