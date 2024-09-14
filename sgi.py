import ast
from typing import List, Tuple

from gi.repository import Gtk

from globals import *
from gui.main_window import MainWindow
from system.objects import Point
from system.view import DisplayFile, ViewPort, Window
from utils import parse_input, validate


class SGI:
    """
    Sistema Gráfico Interativo: esta classe possui a criação dos principais elementos do sistemas,
    assim como os métodos do sistema que simbolizam as funcionalidades principais

    main_window: MainWindow(GTK.Window)
    display_file: DisplayFile
    """

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

        drawing_area.connect_on_draw(self.display_file.on_draw)
        drawing_area.connect_scroll_up_down(self.zoom_in, self.zoom_out)

        object_form.set_on_submit(self.add_object)
        window_form.connect_zoom_buttons(self.zoom_in, self.zoom_out)
        window_form.connect_panning_buttons(
            self.go_up, self.go_left, self.go_right, self.go_down
        )

    def add_object(self, object_type, name, input):
        """Função executada ao clicar em 'Adicionar objeto'"""
        try:
            result: List[Tuple[float]] = parse_input(input)
            validate(result, object_type)

            name = name if name else object_type.name.title()
            object_list_name = f"{object_type.name}[{name}]"
            self.display_file.create_object(
                object_type,
                name,
                result,
                self.main_window.menu_box.window_form.color_box.get_color_tuple(),
            )
            self.main_window.menu_box.object_list.add_item(object_list_name)
            self.main_window.drawing_area.queue_draw()
        except (ValueError, SyntaxError, AttributeError) as e:
            print(f"Erro ao processar a string: {e}")

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
