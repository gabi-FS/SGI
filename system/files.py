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
        object_name = self.name.replace(" ", "_")
        wavefront_str = f'o {object_name}\n'
        for v in self.vertices:
            wavefront_str += f'v {v[0]} {v[1]} {v[2]}\n'

        wavefront_str += f'usemtl {object_name}_material\n'

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

    def get_mtl_str(self) -> str:
        mtl_str = f'newmtl {self.name.replace(" ", "_")}_material\n'
        r, g, b = [float(i) for i in self.color]
        mtl_str += f'Kd {r} {g} {b}'
        return mtl_str


class ObjFileHandler:
    """ Lida com o formato Wavefront.obj para o SGI"""

    @staticmethod
    def save(filename: str, object_list: List[ObjectDescriptor]):
        obj_filename = os.path.basename(filename)
        mtl_filename = obj_filename.replace(".obj", ".mtl")

        obj_archive_str = f'mtllib {mtl_filename}\n'
        mtl_archive_str = ''
        for obj in object_list:
            obj_archive_str += obj.get_wavefront_str() + '\n'
            mtl_archive_str += obj.get_mtl_str() + '\n'

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as obj_file:
            obj_file.write(obj_archive_str)

        mtl_file_path = os.path.join(os.path.dirname(filename), mtl_filename)
        with open(mtl_file_path, 'w', encoding='utf-8') as mtl_file:
            mtl_file.write(mtl_archive_str)

    @staticmethod
    def read(filename: str) -> List[ObjectDescriptor]:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.readlines()
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            return []

        obj_directory = os.path.dirname(filename)
        materials = {}
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
                case 'mtllib':
                    for filename in parts[1:]:
                        mtl_file_path = os.path.join(obj_directory, filename)
                        new_materials = ObjFileHandler.process_mtllib(mtl_file_path)
                        materials.update(new_materials)
                case 'o':
                    object_name = parts[1]
                    current_object = ObjectDescriptor(object_name)
                    object_descriptors.append(current_object)
                case 'usemtl':
                    material_name = parts[1]
                    material = materials[material_name]
                    if material and material['Kd']:
                        current_object.color = material['Kd']
                case 'v':
                    x, y, z = map(float, parts[1:4])
                    vertices.append((x, y, z))
                case 'f':
                    indexes = [part.split('/')[0] for part in parts[1:]]
                    new_face = ObjFileHandler._add_vertices_and_get_relative_indexes(vertices, indexes, current_object)
                    current_object.faces.append(new_face)
                case 'l':
                    indexes = [part.split('/')[0] for part in parts[1:]]
                    new_line = ObjFileHandler._add_vertices_and_get_relative_indexes(vertices, indexes, current_object)
                    current_object.lines.append(new_line)
                case 'p':
                    new_points = ObjFileHandler._add_vertices_and_get_relative_indexes(vertices, parts[1:], current_object)
                    current_object.points += new_points

        return object_descriptors

    @staticmethod
    def process_mtllib(filename: str) -> dict:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.readlines()
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            return {}

        current_material = None
        materials = {}

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
                case 'newmtl':
                    current_material = {}
                    material_name = parts[1]
                    materials[material_name] = current_material
                case 'Kd':
                    r, g, b = [float(i) for i in parts[1:]]
                    current_material['Kd'] = (r, g, b)

        return materials

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
