from typing import Callable

from gi.repository import Gtk


class WindowForm:
    def __init__(self, menu_box):
        title_label = Gtk.Label()
        title_label.set_markup("Janela")
        self.zoom_box = ZoomBox()
        self.panning_box = PanningBox()

        menu_box.add_element(title_label)
        menu_box.add_element(Gtk.HSeparator())
        menu_box.add_element(self.zoom_box.element)
        menu_box.add_element(self.panning_box.element)
        menu_box.add_element(Gtk.HSeparator())

    def connect_panning_buttons(self,
                                on_up: Callable[[], None], on_left: Callable[[], None],
                                on_right: Callable[[], None], on_down: Callable[[], None]):
        self.panning_box.external_on_button_up = on_up
        self.panning_box.external_on_button_left = on_left
        self.panning_box.external_on_button_right = on_right
        self.panning_box.external_on_button_down = on_down

    def connect_zoom_buttons(self, zoom_in: Callable[[], None], zoom_out: Callable[[], None]):
        self.zoom_box.connect_on_zoom_in(zoom_in)
        self.zoom_box.connect_on_zoom_out(zoom_out)


class ZoomBox:
    _external_zoom_in: Callable[[], None]
    _external_zoom_out: Callable[[], None]

    def __init__(self):
        self.element = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        zoom_label = Gtk.Label(label="Zoom:")
        zoom_label.set_xalign(0)

        self.zoom_in_button = Gtk.Button.new_with_label("+")
        self.zoom_in_button.connect("clicked", self.on_zoom_in)

        self.zoom_out_button = Gtk.Button.new_with_label("-")
        self.zoom_out_button.connect("clicked", self.on_zoom_out)

        self.element.pack_start(zoom_label, False, False, 0)
        self.element.pack_start(self.zoom_in_button, False, False, 0)
        self.element.pack_start(self.zoom_out_button, False, False, 0)

    def connect_on_zoom_in(self, func: Callable[[], None]):
        self._external_zoom_in = func

    def connect_on_zoom_out(self, func: Callable[[], None]):
        self._external_zoom_out = func

    def on_zoom_in(self, _):
        if self._external_zoom_in:
            self._external_zoom_in()

    def on_zoom_out(self, _):
        if self._external_zoom_out:
            self._external_zoom_out()


class PanningBox:
    element: Gtk.Box
    external_on_button_up: Callable[[], None]
    external_on_button_left: Callable[[], None]
    external_on_button_right: Callable[[], None]
    external_on_button_down: Callable[[], None]
    button_up: Gtk.Button
    button_left: Gtk.Button
    button_right: Gtk.Button
    button_down: Gtk.Button

    def __init__(self):  # Directional Pad
        self.element = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        panning_label = Gtk.Label(label="Panning:")
        panning_label.set_xalign(0)

        self.button_up = Gtk.Button(label="↑")
        self.button_up.connect("clicked", self.on_button_up)
        self.button_left = Gtk.Button(label="←")
        self.button_left.connect("clicked", self.on_button_left)
        self.button_right = Gtk.Button(label="→")
        self.button_right.connect("clicked", self.on_button_right)
        self.button_down = Gtk.Button(label="↓")
        self.button_down.connect("clicked", self.on_button_down)

        grid.attach(self.button_up, 1, 0, 1, 1)
        grid.attach(self.button_left, 0, 1, 1, 1)
        grid.attach(self.button_right, 2, 1, 1, 1)
        grid.attach(self.button_down, 1, 2, 1, 1)

        self.element.pack_start(panning_label, True, True, 0)
        self.element.pack_start(grid, True, True, 0)

    def on_button_up(self, _):
        if self.external_on_button_up:
            self.external_on_button_up()

    def on_button_left(self, _):
        if self.external_on_button_left:
            self.external_on_button_left()

    def on_button_right(self, _):
        if self.external_on_button_right:
            self.external_on_button_right()

    def on_button_down(self, _):
        if self.external_on_button_down:
            self.external_on_button_down()
