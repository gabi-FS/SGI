from gi.repository import Gtk


class DrawingArea():

    """ Basicamente, a viewport """

    def __init__(self, grid):
        drawing_area = Gtk.DrawingArea()
        drawing_area.set_size_request(-1, -1)

        grid.attach(drawing_area, 1, 0, 2, 2)

        drawing_area.set_hexpand(True)
        drawing_area.set_vexpand(True)
