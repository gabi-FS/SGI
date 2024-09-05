from gi.repository import Gtk

# Descobrir onde consts deveriam ir
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Sistema Gráfico Interativo")
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)
