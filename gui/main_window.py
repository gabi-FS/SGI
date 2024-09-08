from gi.repository import Gtk

from .drawing_area import DrawingArea
from .menu_box import MenuBox


class MainWindow(Gtk.Window):
    def __init__(self, width, height, viewport_size):
        Gtk.Window.__init__(self, title="Sistema Gráfico Interativo")
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        grid = Gtk.Grid()
        self.add(grid)
        self.menu_box = MenuBox(grid)
        self.drawing_area = DrawingArea(grid, viewport_size)

        self.config_grid(grid)

        self.connect("destroy", Gtk.main_quit)

    def config_grid(self, grid):
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
