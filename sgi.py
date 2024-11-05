from typing import Any, Dict, List, Tuple

from gi.repository import Gtk

from globals import (
    VIEWPORT_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    LineClippingType,
    ObjectType,
    TransformationType,
)
from gui.main_window import MainWindow
from system.files import ObjFileHandler
from system.objects import GraphicObject, Point
from system.transform import Transformation
from system.view import DisplayFile, ViewPort, Window
from utils import parse_input
from validation import Validation, ValidationError


class SGI:
    """
    Sistema Gráfico Interativo: esta classe possui a criação dos principais elementos do sistema,
    assim como os métodos do sistema que simbolizam as funcionalidades principais
    """

    main_window: MainWindow
    display_file: DisplayFile

    def __init__(self):
        self.main_window = MainWindow(WINDOW_WIDTH, WINDOW_HEIGHT, VIEWPORT_SIZE)
        window = Window(Point(0, 0), (VIEWPORT_SIZE, VIEWPORT_SIZE))
        viewport = ViewPort((VIEWPORT_SIZE, VIEWPORT_SIZE), window)
        transformation = Transformation()
        self.display_file = DisplayFile(viewport, transformation)
        self.connect()

    def run(self):
        print("GTK+ version:", Gtk.get_major_version(), Gtk.get_minor_version())
        self.main_window.show_all()
        Gtk.main()

    def connect(self):
        """Faz as conexões entre elementos e ações da tela e funções de suas classes específicas"""
        drawing_area = self.main_window.drawing_area
        window_form = self.main_window.menu_box.window_form
        object_list = self.main_window.menu_box.object_list

        self.main_window.menu_bar.connect_on_import(self.import_objects)
        self.main_window.menu_bar.connect_on_export(self.export_objects)

        drawing_area.connect_on_draw(self.display_file.on_draw)
        drawing_area.connect_scroll_up_down(self.zoom_in, self.zoom_out)

        object_list.set_on_apply_transform(self.transform_object)
        self.main_window.menu_box.set_on_create_object(self.add_object)
        window_form.connect_zoom_buttons(self.zoom_in, self.zoom_out)
        window_form.connect_panning_buttons(
            self.go_up,
            self.go_left,
            self.go_right,
            self.go_down,
            self.go_front,
            self.go_back,
        )
        window_form.connect_rotate_window(self.rotate)
        window_form.connect_change_clipping(self.change_clipping_type)

    def add_object(
            self, object_type: ObjectType, name: str, input_str: str, color: tuple[float]
    ) -> int:
        """Função executada ao clicar em 'Adicionar objeto'"""
        try:
            if ObjectType.BEZIER_SURFACE == object_type:
                parsed_input = []  # Matriz de inputs (lista de pontos)
                lines = input_str.split(";")
                for line in lines:
                    parsed_line = parse_input(line)
                    parsed_input.append(parsed_line)
            else:
                parsed_input: (
                        List[Tuple[float, float]] | List[Tuple[float, float, float]]
                ) = parse_input(input_str)
                Validation.object_coordinates_input(parsed_input, object_type)

            name = name if name else object_type.name.title()
            object_id = self.display_file.create_object(
                object_type, name, parsed_input, color
            )
            self.main_window.menu_box.object_list.add_item(
                f"{object_type.name}[{name}]", object_id
            )
            self.main_window.drawing_area.queue_draw()
            return 1
        except (ValueError, SyntaxError, AttributeError) as e:
            print(f"Erro ao processar a string: {e}")
            return -1
        except ValidationError as e:
            print(f"Erro ao validar entradas: {e}")
            return -1

    def transform_object(
            self, object_id: int, object_input: Dict[TransformationType, Any]
    ) -> int:
        """
        object_input:
            TRANSLATION, SCALING: ['x': str, 'y': str]
            ROTATION: ['type': RotationType, 'angle': str, 'point': str]
        """
        try:
            Validation.object_transform_input(object_input)
            self.display_file.transform_object(object_id, object_input)
            self.main_window.drawing_area.queue_draw()
            return 1
        except ValidationError as e:
            print(f"Erro ao validar entradas: {e}")
            return -1  # Para manter a modal aberta no caso de problemas

    def import_objects(self, filename: str):
        try:
            object_descriptors = ObjFileHandler.read(filename)
            for obj in object_descriptors:
                graphic_obj = GraphicObject.get_2d_object(obj)
                if graphic_obj:
                    self.display_file.add_object(graphic_obj)
                    item_text = f"{graphic_obj.type.name}[{obj.name}]"
                    self.main_window.menu_box.object_list.add_item(
                        item_text, graphic_obj.id
                    )
            self.main_window.drawing_area.queue_draw()
        except:
            print("Erro ao importar objetos, arquivo possívelmente inválido.")

    def export_objects(self, filename: str):
        ObjFileHandler.save(filename, self.display_file.get_object_descriptors())

    def change_clipping_type(self, new_type: LineClippingType):
        self.display_file.change_clipping_type(new_type)
        self.main_window.drawing_area.queue_draw()

    def zoom_in(self):
        self.display_file.on_zoom_in()
        self.main_window.drawing_area.queue_draw()

    def zoom_out(self):
        self.display_file.on_zoom_out()
        self.main_window.drawing_area.queue_draw()

    def go_up(self):
        self.display_file.on_up()
        self.main_window.drawing_area.queue_draw()

    def go_left(self):
        self.display_file.on_left()
        self.main_window.drawing_area.queue_draw()

    def go_right(self):
        self.display_file.on_right()
        self.main_window.drawing_area.queue_draw()

    def go_down(self):
        self.display_file.on_down()
        self.main_window.drawing_area.queue_draw()

    def go_front(self):
        self.display_file.on_front()
        self.main_window.drawing_area.queue_draw()

    def go_back(self):
        self.display_file.on_back()
        self.main_window.drawing_area.queue_draw()

    def rotate(
            self,
            angle_x: str,
            angle_y: str,
            angle_z: str,
    ):
        try:
            # TODO: do nothing if all empty

            a_x = float(angle_x) if angle_x.strip() else 0.0
            a_y = float(angle_y) if angle_y.strip() else 0.0
            a_z = float(angle_z) if angle_z.strip() else 0.0

            self.display_file.on_rotate(a_x, a_y, a_z)
            self.main_window.drawing_area.queue_draw()
        except ValueError:
            print("Não foi possível converter entrada para numérico.")
