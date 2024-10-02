from gi.repository import Gdk, Gtk

from globals import ObjectType


class ObjectForm:
    """Formulário para a criação do objeto"""

    def __init__(self, menu_box):
        self.on_submit = None
        self.object_radio = ObjectRadio()
        self.color_box = ColorBox()
        self.name_input = Gtk.Entry()
        self.coordinate_input = Gtk.Entry()
        self.coordinate_input.set_placeholder_text("(x1, y1), (x2, y2),...")
        self.submit_button = Gtk.Button.new_with_label("Adicionar objeto")
        self.submit_button.connect("clicked", self.on_add)

        menu_box.add_element(Gtk.Label(label="Criação de objeto"))
        menu_box.add_element(Gtk.Separator())
        menu_box.add_element(self.color_box.element)
        menu_box.add_element(self.object_radio.element)
        menu_box.add_element(self.create_form_label("Nome do objeto (Opcional):"))
        menu_box.add_element(self.name_input)
        menu_box.add_element(self.create_form_label("Coordenadas (Obrigatório):"))
        menu_box.add_element(self.coordinate_input)
        menu_box.add_element(self.submit_button)
        menu_box.add_element(Gtk.Separator())

    def get_color(self) -> tuple[float]:
        return self.color_box.get_color_tuple()

    def create_form_label(self, name):
        form_label = Gtk.Label()
        form_label.set_markup(f"<b>{name}</b>")
        form_label.set_xalign(0)
        return form_label

    def set_on_submit(self, function):
        self.on_submit = function

    def on_add(self, _):
        if self.on_submit:
            self.on_submit(
                self.object_radio.selected_type,
                self.name_input.get_text(),
                self.coordinate_input.get_text(),
            )
        self.clear_form()  # TODO: Reavaliar necessidade

    def clear_form(self):
        self.name_input.set_text("")
        self.coordinate_input.set_text("")


class ObjectRadio:
    def __init__(self):
        self.element = Gtk.FlowBox()
        self.selected_type = ObjectType.POINT
        self.buttons = []

        first_button = Gtk.RadioButton.new_with_label_from_widget(None, "Ponto")
        first_button.connect("toggled", self.on_toggle, self.selected_type)
        self.buttons.append(first_button)

        self.add_button("Reta", ObjectType.LINE)
        self.add_button("Polígono (arame)", ObjectType.WIREFRAME_POLYGON)
        self.add_button("Polígono (preenchido)", ObjectType.FILLED_POLYGON)

        for button in self.buttons:
            self.element.add(button)

    def add_button(self, name, object_type):
        button = Gtk.RadioButton.new_with_label_from_widget(self.buttons[0], name)
        button.connect("toggled", self.on_toggle, object_type)
        self.buttons.append(button)

    def on_toggle(self, button, type):
        if button.get_active():
            self.selected_type = type


class ColorBox:
    def __init__(self) -> None:
        self.element = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.color_button = Gtk.ColorButton()

        self.color_button.connect("color-set", self.on_color_chosen)

        self.color = Gdk.RGBA(1, 0, 0, 1)  # starting color is RED (opaque)
        self.color_button.set_rgba(self.color)

        coloring_label = Gtk.Label(label="Cor do pincel:")
        coloring_label.set_xalign(0)

        self.element.pack_start(coloring_label, True, True, 0)
        self.element.pack_start(self.color_button, True, True, 0)

    def on_color_chosen(self, widget):
        self.color = widget.get_rgba()

    def get_color_tuple(self) -> tuple[float]:
        """Returns a tuple with the current color"""
        return (self.color.red, self.color.green, self.color.blue)
