from typing import List, Tuple

from globals import ObjectType
from system.basics import Point
from system.objects import PointObject, GraphicObject, LineSegmentObject, WireframeObject


class ObjectDescriptor:
    """ Descritor do objeto: armazena informações necessárias """

    name: str
    vertices: List[Tuple[float, float, float]]
    faces = List[Tuple[int, ...]]  # Utiliza índice iniciado em 1
    type: ObjectType | None  # Preenchido no momento da criação do objeto

    def __init__(self, name: str, vertices: List[Tuple[float, float, float]], faces: List[Tuple[int, ...]]):
        self.name = name
        self.vertices = vertices
        self.faces = faces
        self.color = (1, 0, 0)  # Later, get from file

    def get_2d_object(self) -> GraphicObject | None:
        """ Atualmente, o máximo nível de objeto que nosso sistema desenha são polígonos.
        Então, o desenho só permite uma face.
        """
        face = self.faces[0]
        ordered_points = []
        for i in face:
            vertice = self.vertices[i - 1]
            ordered_points.append(Point(vertice[0], vertice[1]))

        match len(ordered_points):
            case 0:
                return None
            case 1:
                self.type = ObjectType.POINT
                return PointObject(self.name, ordered_points, self.color)
            case 2:
                self.type = ObjectType.LINE
                return LineSegmentObject(self.name, ordered_points, self.color)
            case _:
                self.type = ObjectType.POLYGON
                return WireframeObject(self.name, ordered_points, self.color)


class ObjFileHandler:
    """ Lida com o formato Wavefront.obj para o SGI"""

    @staticmethod
    def read(filename: str) -> List[ObjectDescriptor]:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.readlines()
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            return []

        object_descriptors = []
        name = ''
        vertices = []
        faces = []

        for line in content:
            parts = line.split()

            if not parts or line.startswith('#'):
                continue

            prefix = parts[0]
            match prefix:
                case 'o':
                    if len(vertices) > 0:
                        object_descriptors.append(ObjectDescriptor(name, vertices, faces))
                    name = parts[1]
                    vertices = []
                    faces = []
                case 'v':
                    x, y, z = map(float, parts[1:4])
                    vertices.append((x, y, z))
                case 'f':
                    line_content = line.split('#')[0]
                    vertex_indices = tuple(int(p.split('/')[0]) for p in line_content.split()[1:])
                    faces.append(vertex_indices)

        if len(vertices) > 0:
            object_descriptors.append(ObjectDescriptor(name, vertices, faces))

        return object_descriptors
