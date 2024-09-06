from gi.repository import Gtk

from .drawing_area import DrawingArea
from .menu_box import MenuBox

# Descobrir onde consts deveriam ir
WINDOW_WIDTH = 1125  # 1/3 Menu, 2/3 DrawingArea
WINDOW_HEIGHT = 750


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Sistema Gráfico Interativo")
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        grid = Gtk.Grid()
        self.add(grid)
        self.menu_box = MenuBox(grid)
        self.drawing_area = DrawingArea(grid)

        self.config_grid(grid)

        self.connect("destroy", Gtk.main_quit)

    def config_grid(self, grid):
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)

    # Ideia: fazer getters de classes ou elementos específicos dentro da main_window pra parte que realmente faz ações da SGI utilizar...
    # Tipo a lista de objetos, os botões... ir pensando quando for fazendo
