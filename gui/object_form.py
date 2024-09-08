from enum import Enum

from gi.repository import Gtk


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3


class ObjectForm():
    def __init__(self, menu_box):
        self.object_radio = ObjectRadio()
        self.name_input = Gtk.Entry()
        self.coordinate_input = Gtk.Entry()
        self.coordinate_input.set_placeholder_text(
            "(x1, y1), (x2, y2),...")
        self.submit_button = Gtk.Button.new_with_label("Adicionar objeto")
        self.submit_button.connect("clicked", self.on_add)

        menu_box.add_element(Gtk.Label(label="Criação de objeto"))
        menu_box.add_element(Gtk.HSeparator())
        menu_box.add_element(self.object_radio.element)
        menu_box.add_element(self.create_form_label(
            "Nome do objeto (Opcional):"))
        menu_box.add_element(self.name_input)
        menu_box.add_element(self.create_form_label(
            "Coordenadas (Obrigatório):"))
        menu_box.add_element(self.coordinate_input)
        menu_box.add_element(self.submit_button)
        menu_box.add_element(Gtk.HSeparator())

    def create_form_label(self, name):
        form_label = Gtk.Label()
        form_label.set_markup(f"<b>{name}</b>")
        form_label.set_xalign(0)
        return form_label

    def set_on_submit(self, function):
        self.on_submit = function

    def on_add(self, _):
        print(f"Selecionado: {self.object_radio.selected_type}")
        print(f"Nome: {self.name_input.get_text()}")
        print(f"Coordenadas: {self.coordinate_input.get_text()}")

        if self.on_submit:
            self.on_submit(
                self.object_radio.selected_type,
                self.name_input.get_text(),
                self.coordinate_input.get_text()
            )
        self.clear_form()  # Avaliar necessidade

    def clear_form(self):
        self.name_input.set_text("")
        self.coordinate_input.set_text("")


class ObjectRadio():
    def __init__(self):
        self.element = Gtk.Box(spacing=10)
        self.selected_type = ObjectType.POINT
        self.buttons = []

        first_button = Gtk.RadioButton.new_with_label_from_widget(
            None, "Ponto")
        first_button.connect("toggled", self.on_toggle, self.selected_type)
        self.buttons.append(first_button)

        self.add_button("Reta", ObjectType.LINE)
        self.add_button("Polígono", ObjectType.POLYGON)

        for button in self.buttons:
            self.element.pack_start(button, False, False, 0)

    def add_button(self, name, object_type):
        button = Gtk.RadioButton.new_with_label_from_widget(
            self.buttons[0], name)
        button.connect("toggled", self.on_toggle, object_type)
        self.buttons.append(button)

    def on_toggle(self, button, type):
        if button.get_active():
            self.selected_type = type
