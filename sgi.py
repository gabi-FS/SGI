from gi.repository import Gtk

from gui.main_window import MainWindow


class SGI:
    def __init__(self): pass

    def run(self):
        print("GTK+ version:", Gtk.get_major_version(), Gtk.get_minor_version())

        main_window = MainWindow()
        main_window.show_all()
        Gtk.main()
