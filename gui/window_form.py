from typing import Callable

from gi.repository import Gtk

from globals import LineClippingType


class WindowForm:
    def __init__(self, menu_box):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self._zoom_box = ZoomBox()
        self._panning_box = PanningBox()
        self._rotation_input = RotationInput()
        self._clipping_radio = ClippingRadio()

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.pack_start(self._zoom_box.element, False, False, 0)
        box.pack_start(Gtk.Separator(), False, False, 0)
        box.pack_start(self._panning_box.element, False, False, 0)

        self.element.pack_start(self._rotation_input.element, False, False, 0)
        self.element.pack_start(Gtk.Separator(), False, False, 0)
        self.element.pack_start(box, False, False, 0)

        self.element.pack_start(Gtk.Separator(), False, False, 0)
        self.element.pack_start(self._clipping_radio.element, False, False, 0)

        title_label = Gtk.Label()
        title_label.set_markup("Janela")

        menu_box.add_element(title_label)
        menu_box.add_element(Gtk.Separator())
        menu_box.add_element(self.element)
        menu_box.add_element(Gtk.Separator())

    def connect_panning_buttons(
        self,
        on_up: Callable[[], None],
        on_left: Callable[[], None],
        on_right: Callable[[], None],
        on_down: Callable[[], None],
        on_front: Callable[[], None],
        on_back: Callable[[], None],
    ):
        self._panning_box.external_on_button_up = on_up
        self._panning_box.external_on_button_left = on_left
        self._panning_box.external_on_button_right = on_right
        self._panning_box.external_on_button_down = on_down
        self._panning_box.external_on_button_front = on_front
        self._panning_box.external_on_button_back = on_back

    def connect_zoom_buttons(
        self, zoom_in: Callable[[], None], zoom_out: Callable[[], None]
    ):
        self._zoom_box.external_zoom_in = zoom_in
        self._zoom_box.external_zoom_out = zoom_out

    def connect_rotate_window(self, rotate_window: Callable[[str], None]):
        self._rotation_input.rotate_window = rotate_window

    def connect_change_clipping(self, on_change):
        self._clipping_radio.external_on_toggle = on_change


class ZoomBox:
    element: Gtk.Box
    zoom_in_button: Gtk.Button
    zoom_out_button: Gtk.Button
    external_zoom_in: Callable[[], None]
    external_zoom_out: Callable[[], None]

    def __init__(self):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.zoom_in_button = Gtk.Button.new_with_label("+")
        self.zoom_in_button.connect("clicked", self.on_zoom_in)
        self.zoom_out_button = Gtk.Button.new_with_label("-")
        self.zoom_out_button.connect("clicked", self.on_zoom_out)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.pack_start(self.zoom_in_button, False, False, 0)
        box.pack_start(self.zoom_out_button, False, False, 0)

        zoom_label = Gtk.Label(label="Zoom")
        zoom_label.set_xalign(0)

        self.element.pack_start(zoom_label, False, False, 0)
        self.element.pack_start(box, False, False, 0)

    def on_zoom_in(self, _):
        if self.external_zoom_in:
            self.external_zoom_in()

    def on_zoom_out(self, _):
        if self.external_zoom_out:
            self.external_zoom_out()


class PanningBox:
    element: Gtk.Box
    button_up: Gtk.Button
    button_left: Gtk.Button
    button_right: Gtk.Button
    button_down: Gtk.Button
    external_on_button_up: Callable[[], None]
    external_on_button_left: Callable[[], None]
    external_on_button_right: Callable[[], None]
    external_on_button_down: Callable[[], None]
    external_on_button_front: Callable[[], None]
    external_on_button_back: Callable[[], None]

    def __init__(self):  # Directional Pad
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        grid = Gtk.Grid()
        grid.set_column_spacing(10)

        panning_label = Gtk.Label(label="Panning")
        panning_label.set_xalign(0)

        self.button_up = Gtk.Button(label="↑")
        self.button_up.connect("clicked", self.on_button_up)
        self.button_left = Gtk.Button(label="←")
        self.button_left.connect("clicked", self.on_button_left)
        self.button_right = Gtk.Button(label="→")
        self.button_right.connect("clicked", self.on_button_right)
        self.button_down = Gtk.Button(label="↓")
        self.button_down.connect("clicked", self.on_button_down)

        # para frente e para trás
        self.button_front = Gtk.Button(label="front")
        self.button_front.connect("clicked", self.on_button_front)
        self.button_back = Gtk.Button(label="back")
        self.button_back.connect("clicked", self.on_button_back)

        grid.attach(self.button_up, 1, 0, 1, 1)
        grid.attach(self.button_left, 0, 1, 1, 1)
        grid.attach(self.button_right, 2, 1, 1, 1)
        grid.attach(self.button_down, 1, 2, 1, 1)
        grid.attach(self.button_front, 3, 0, 1, 1)  # Front button in column 3, row 0
        grid.attach(self.button_back, 3, 1, 1, 1)  # Back button in column 3, row 1

        self.element.pack_start(panning_label, False, False, 0)
        self.element.pack_start(grid, False, False, 0)

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

    def on_button_front(self, _):
        if self.external_on_button_front:
            self.external_on_button_front()

    def on_button_back(self, _):
        if self.external_on_button_back:
            self.external_on_button_back()


class RotationInput:
    element: Gtk.Box
    angle_entry: Gtk.Entry
    rotate_button: Gtk.Button
    rotate_window: Callable[[str], None]

    def __init__(self):
        self.element = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        wrapper = Gtk.Box(spacing=10)

        self.x_angle_entry = Gtk.Entry()
        self.x_angle_entry.set_placeholder_text("0")
        self.x_angle_entry.set_width_chars(4)

        self.y_angle_entry = Gtk.Entry()
        self.y_angle_entry.set_placeholder_text("0")
        self.y_angle_entry.set_width_chars(4)

        self.z_angle_entry = Gtk.Entry()
        self.z_angle_entry.set_placeholder_text("0")
        self.z_angle_entry.set_width_chars(4)

        self.rotate_button = Gtk.Button(label="Rotacionar")
        self.rotate_button.connect("clicked", self.on_rotate_button_clicked)

        info_label = Gtk.Label(label="Ângulo (em graus): ")
        info_label.set_halign(Gtk.Align.START)

        wrapper.pack_start(Gtk.Label(label="X:"), False, False, 0)
        wrapper.pack_start(self.x_angle_entry, False, False, 0)
        wrapper.pack_start(Gtk.Label(label="Y:"), False, False, 0)
        wrapper.pack_start(self.y_angle_entry, False, False, 0)
        wrapper.pack_start(Gtk.Label(label="Z:"), False, False, 0)
        wrapper.pack_start(self.z_angle_entry, False, False, 0)
        wrapper.pack_start(self.rotate_button, False, False, 0)
        self.element.pack_start(info_label, False, False, 0)
        self.element.pack_start(wrapper, False, False, 0)

    def on_rotate_button_clicked(self, _):
        if self.rotate_window:
            self.rotate_window(
                self.x_angle_entry.get_text(),
                self.y_angle_entry.get_text(),
                self.z_angle_entry.get_text(),
            )
            for entry in (self.x_angle_entry, self.y_angle_entry, self.z_angle_entry):
                entry.set_text("")


class ClippingRadio:
    selected_type: LineClippingType
    external_on_toggle: Callable

    def __init__(self):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.selected_type = LineClippingType.LIANG_BARSKY
        self.buttons = []

        first_button = Gtk.RadioButton.new_with_label_from_widget(None, "Liang-Barsky")
        first_button.connect("toggled", self.on_toggle, self.selected_type)
        self.buttons.append(first_button)

        self.add_button("Cohen-Sutherland", LineClippingType.COHEN_SUTHERLAND)

        clipping_label = Gtk.Label(label="Método de clipping de linhas")
        clipping_label.set_xalign(0)

        self.element.pack_start(clipping_label, False, False, 0)

        for button in self.buttons:
            input_box.pack_start(button, False, False, 0)

        self.element.pack_start(input_box, False, False, 0)

    def add_button(self, name, object_type):
        button = Gtk.RadioButton.new_with_label_from_widget(self.buttons[0], name)
        button.connect("toggled", self.on_toggle, object_type)
        self.buttons.append(button)

    def on_toggle(self, button, type):
        if button.get_active():
            self.selected_type = type
            if self.external_on_toggle:
                self.external_on_toggle(type)
