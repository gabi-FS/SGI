from gi.repository import Gtk

from .drawing_area import DrawingArea
from .menu_box import MenuBox


class MainWindow(Gtk.Window):

    menu_box: MenuBox
    drawing_area: DrawingArea

    def __init__(self, width: int, height: int, viewport_size: int):
        Gtk.Window.__init__(self, title="Sistema Gráfico Interativo")
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)

        self.add(grid)
        self.menu_box = MenuBox(grid)
        self.drawing_area = DrawingArea(grid, viewport_size)

        self.connect("destroy", Gtk.main_quit)
