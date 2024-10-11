from gi.repository import Gdk, Gtk

from globals import ObjectType


class ObjectWindow(Gtk.Window):
    """ Janela para comportar o formulário de criação de objeto"""

    def __init__(self, object_form, reference_widget):
        super().__init__(title="Criação do objeto")
        self.set_modal(True)
        self.set_default_size(900, 300)
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        self.add(self.element)
        self.object_form = object_form

        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_valign(Gtk.Align.END)
        cancel_button = Gtk.Button(label="Cancelar")
        cancel_button.connect("clicked", self.on_close_clicked)
        confirm_button = Gtk.Button(label="Adicionar objeto")
        confirm_button.connect("clicked", self.on_confirm)

        button_box.pack_start(cancel_button, False, False, 0)
        button_box.pack_start(confirm_button, False, False, 0)

        self.element.pack_start(self.object_form.element, False, False, 0)
        self.element.pack_start(button_box, False, False, 0)
        self.set_transient_for(reference_widget.get_toplevel())
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def on_close_clicked(self, _):
        self.destroy()

    def on_confirm(self, _):
        result = self.object_form.on_add()
        if result == 1:  # SUCCESSFUL
            self.destroy()


class ObjectForm:
    """Formulário para a criação do objeto"""

    def __init__(self, on_submit):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)

        self.on_submit = on_submit
        self.object_radio = ObjectRadio()
        self.color_box = ColorBox()
        self.name_input = Gtk.Entry()
        self.coordinate_input = Gtk.Entry()
        self.coordinate_input.set_placeholder_text("(x1, y1), (x2, y2),...")

        self.add_element(self.color_box.element)
        self.add_element(self.object_radio.element)
        self.add_element(self.create_form_label("Nome do objeto (Opcional):"))
        self.add_element(self.name_input)
        self.add_element(self.create_form_label("Coordenadas (Obrigatório):"))
        self.add_element(self.coordinate_input)
        self.add_element(Gtk.Separator())

    def add_element(self, new_element: Gtk.Widget):
        self.element.pack_start(new_element, False, True, 0)

    def get_color(self) -> tuple[float]:
        return self.color_box.get_color_tuple()

    @staticmethod
    def create_form_label(name):
        form_label = Gtk.Label()
        form_label.set_markup(f"<b>{name}</b>")
        form_label.set_xalign(0)
        return form_label

    def on_add(self):
        return self.on_submit(
            self.object_radio.selected_type,
            self.name_input.get_text(),
            self.coordinate_input.get_text(),
            self.get_color()
        )

    def clear_form(self):
        self.name_input.set_text("")
        self.coordinate_input.set_text("")


class ObjectRadio:
    def __init__(self):
        self.element = Gtk.Box(spacing=10)
        self.selected_type = ObjectType.POINT
        self.buttons = []

        first_button = Gtk.RadioButton.new_with_label_from_widget(None, "Ponto")
        first_button.connect("toggled", self.on_toggle, self.selected_type)
        self.buttons.append(first_button)

        self.add_button("Reta", ObjectType.LINE)
        self.add_button("Polígono (arame)", ObjectType.WIREFRAME_POLYGON)
        self.add_button("Polígono (preenchido)", ObjectType.FILLED_POLYGON)
        self.add_button("Curva (Bézier)", ObjectType.BEZIER_CURVE)

        for button in self.buttons:
            self.element.pack_start(button, False, False, 0)

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
