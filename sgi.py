from typing import Any, Dict, List, Tuple

from gi.repository import Gtk

from globals import WINDOW_WIDTH, WINDOW_HEIGHT, VIEWPORT_SIZE, ObjectType, TransformationType
from gui.main_window import MainWindow
from system.objects import Point
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
        self.display_file = DisplayFile(viewport)
        self.connect()

    def run(self):
        print("GTK+ version:", Gtk.get_major_version(), Gtk.get_minor_version())
        self.main_window.show_all()
        Gtk.main()

    def connect(self):
        """Faz as conexões entre elementos e ações da tela e funções de suas classes específicas"""
        drawing_area = self.main_window.drawing_area
        object_form = self.main_window.menu_box.object_form
        window_form = self.main_window.menu_box.window_form
        object_list = self.main_window.menu_box.object_list

        drawing_area.connect_on_draw(self.display_file.on_draw)
        drawing_area.connect_scroll_up_down(self.zoom_in, self.zoom_out)

        object_list.set_on_apply_transform(self.transform_object)
        object_form.set_on_submit(self.add_object)
        window_form.connect_zoom_buttons(self.zoom_in, self.zoom_out)
        window_form.connect_panning_buttons(self.go_up, self.go_left, self.go_right, self.go_down)

    def add_object(self, object_type: ObjectType, name: str, input_str: str):
        """Função executada ao clicar em 'Adicionar objeto'"""
        try:
            parsed_input: List[Tuple[float, float]] = parse_input(input_str)
            Validation.object_coordinates_input(parsed_input, object_type)

            name = name if name else object_type.name.title()
            object_id = self.display_file.create_object(
                object_type,
                name,
                parsed_input,
                self.main_window.menu_box.object_form.get_color(),
            )
            self.main_window.menu_box.object_list.add_item(f"{object_type.name}[{name}]", object_id)
            self.main_window.drawing_area.queue_draw()
        except (ValueError, SyntaxError, AttributeError) as e:
            print(f"Erro ao processar a string: {e}")
        except ValidationError as e:
            print(f"Erro ao validar entradas: {e}")

    def transform_object(self, object_id: int, object_input: Dict[TransformationType, Any]) -> int:
        """
        object_input:
            TRANSLATION, SCALING: ['x': str, 'y': str]
            ROTATION: ['type': RotationType, 'angle': str, 'point': str]
        """
        try:
            Validation.object_transform_input(object_input)
            graphic_object = self.display_file.get_object(object_id)
            new_points = Transformation.get_transformed_points(graphic_object, object_input)
            graphic_object.update_points(new_points)
            self.main_window.drawing_area.queue_draw()
            return 1
        except ValidationError as e:
            print(f"Erro ao validar entradas: {e}")
            return -1  # Para manter a modal aberta no caso de problemas

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
