from typing import List, Tuple

import os

from system.basics import Point


class ObjectDescriptor:
    """ Descritor do objeto: armazena informações necessárias """

    name: str
    vertices: List[Tuple[float, float, float]]
    faces = List[Tuple[int, ...]]
    lines = List[Tuple[int, ...]]
    points = List[int]

    def __init__(self, name: str):
        self.name = name
        self.vertices = []
        self.faces = []
        self.lines = []
        self.points = []
        self.color = (1, 0, 0)  # Later, get from file

    @staticmethod
    def vertices_to_points(vertices: List[Tuple[float, float, float]]) -> List[Point]:
        return [Point(v[0], v[1]) for v in vertices]

    def get_wavefront_str(self) -> str:
        wavefront_str = f'o {self.name.replace(" ", "_")}\n'
        for v in self.vertices:
            wavefront_str += f'v {v[0]} {v[1]} {v[2]}\n'

        if self.points:
            p_string = "p " + " ".join(str(p) for p in self.points)
            wavefront_str += p_string + '\n'

        for line in self.lines:
            l_string = "l " + " ".join(str(l) for l in line)
            wavefront_str += l_string + '\n'

        for face in self.faces:
            f_string = "f " + " ".join(str(f) for f in face)
            wavefront_str += f_string + '\n'

        return wavefront_str


class ObjFileHandler:
    """ Lida com o formato Wavefront.obj para o SGI"""

    @staticmethod
    def save(filename: str, object_list: List[ObjectDescriptor]):
        archive_str = ''
        for obj in object_list:
            archive_str += obj.get_wavefront_str() + '\n'

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as file:
            file.write(archive_str)

    @staticmethod
    def read(filename: str) -> List[ObjectDescriptor]:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.readlines()
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            return []

        object_descriptors = []
        vertices = []
        current_object = None

        for line in content:
            split_by_comment = line.split('#')
            before_comment = split_by_comment[0]
            if not before_comment:
                continue
            parts = before_comment.split()
            if not parts:
                continue
            prefix = parts[0]

            match prefix:
                case 'o':
                    object_name = parts[1]
                    current_object = ObjectDescriptor(object_name)
                    object_descriptors.append(current_object)
                case 'v':
                    x, y, z = map(float, parts[1:4])
                    vertices.append((x, y, z))
                case 'f':
                    new_face = ObjFileHandler._add_vertices_and_get_relative_indexes(vertices, parts[1:], current_object)
                    current_object.faces.append(new_face)
                case 'l':
                    new_line = ObjFileHandler._add_vertices_and_get_relative_indexes(vertices, parts[1:], current_object)
                    current_object.lines.append(new_line)
                case 'p':
                    new_points = ObjFileHandler._add_vertices_and_get_relative_indexes(vertices, parts[1:], current_object)
                    current_object.points += new_points

        return object_descriptors

    @staticmethod
    def _add_vertices_and_get_relative_indexes(vertices: List[Tuple[float, float, float]], indexes: List[str], obj: ObjectDescriptor):
        relative_indexes = []
        for i in indexes:
            index = int(i)
            if index > 0:
                index -= 1
            vertice = vertices[index]
            if vertice not in obj.vertices:
                obj.vertices.append(vertice)
            relative_indexes.append(obj.vertices.index(vertice))
        return relative_indexes
