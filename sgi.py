import ast
from typing import List, Tuple

from gi.repository import Gtk

from globals import *
from gui.main_window import MainWindow
from system.objects import Point
from system.view import DisplayFile, ViewPort, Window


class SGI:
    def __init__(self):
        self.main_window = MainWindow(
            WINDOW_WIDTH, WINDOW_HEIGHT, VIEWPORT_SIZE)
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

        self.main_window.drawing_area.connect_on_draw(
            self.display_file.on_draw)
        self.main_window.menu_box.object_form.set_on_submit(self.add_object)
        self.main_window.menu_box.window_form.connect_zoom_buttons(
            self.zoom_in, self.zoom_out)
        self.main_window.menu_box.window_form.connect_panning_buttons(
            self.go_up, self.go_left, self.go_right, self.go_down)

    def add_object(self, object_type, name, input):
        """Função executada ao apertar Adicionar objeto"""
        if not name:  # Rever depois
            name = object_type

        # Tratar Input -> Por aqui, se necessário separar a lógica..
        try:
            result: List[Tuple[float]] = ast.literal_eval(input)
            if all(
                isinstance(t, tuple) and all(isinstance(x, float) for x in t)
                for t in result
            ):
                self.display_file.create_object(object_type, name, result)
                self.main_window.menu_box.object_list.add_item(name)
                self.main_window.drawing_area.queue_draw()
            else:
                print("Formato inválido")

        except (ValueError, SyntaxError):
            print("Erro ao avaliar a string")

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
