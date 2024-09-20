from gi.repository import Gtk

from gui.drawing_area import DrawingArea
from gui.menu_bar import MenuBar
from gui.menu_box import MenuBox


class MainWindow(Gtk.Window):
    menu_box: MenuBox
    drawing_area: DrawingArea

    def __init__(self, width: int, height: int, viewport_size: int):
        Gtk.Window.__init__(self, title="Sistema Gráfico Interativo")
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        self.menu_bar = MenuBar()

        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        self.menu_box = MenuBox(grid)
        self.drawing_area = DrawingArea(grid, viewport_size)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(self.menu_bar.element, False, False, 0)
        vbox.pack_start(grid, False, False, 0)
        self.add(vbox)

        self.connect("destroy", Gtk.main_quit)
