from gi.repository import Gtk


class WindowForm():
    def __init__(self, menu_box):
        title_label = Gtk.Label()
        title_label.set_markup("Janela")
        self.zoom_box = ZoomBox()

        menu_box.add_element(title_label)
        menu_box.add_element(Gtk.HSeparator())
        menu_box.add_element(self.zoom_box.element)
        menu_box.add_element(Gtk.HSeparator())


class ZoomBox():
    def __init__(self):
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        zoom_label = Gtk.Label(label="Zoom:")
        zoom_label.set_xalign(0)

        self.zoom_in_button = Gtk.Button.new_with_label("+")
        self.zoom_in_button.connect("clicked", self.on_zoom_in)

        self.zoom_out_button = Gtk.Button.new_with_label("-")
        self.zoom_out_button.connect("clicked", self.on_zoom_out)

        self.element.pack_start(zoom_label, False, False, 0)
        self.element.pack_start(self.zoom_in_button, False, False, 0)
        self.element.pack_start(self.zoom_out_button, False, False, 0)

    def on_zoom_in(self, button):
        print("Zoom in clicado")

    def on_zoom_out(self, button):
        print("Zoom out clicado")
