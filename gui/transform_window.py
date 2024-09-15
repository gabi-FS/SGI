from gi.repository import Gtk


class TransformWindow(Gtk.Window):
    def __init__(self, widget):
        super().__init__(title="Transformação do objeto")
        self.set_modal(True)
        self.set_default_size(900, 300)
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        self.add(self.element)
        # Mostrar informações originais do objeto aqui? Id, nome, tipo, pontos?

        self.notebook = Gtk.Notebook()
        self.translation_page = TranslationPage()
        self.rotation_page = RotationPage()
        self.scaling_page = ScalingPage()

        self.notebook.append_page(
            self.translation_page.element,  Gtk.Label(label="Translação"))
        self.notebook.append_page(
            self.rotation_page.element,  Gtk.Label(label="Rotação"))
        self.notebook.append_page(
            self.scaling_page.element,  Gtk.Label(label="Escalonamento"))

        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_valign(Gtk.Align.END)
        cancel_button = Gtk.Button(label="Cancelar")
        cancel_button.connect("clicked", self.on_close_clicked)
        apply_button = Gtk.Button(label="Aplicar")

        button_box.pack_start(cancel_button, False, False, 0)
        button_box.pack_start(apply_button, False, False, 0)

        self.element.pack_start(self.notebook, False, False, 0)
        self.element.pack_start(button_box, False, False, 0)
        self.set_transient_for(widget.get_toplevel())
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def on_close_clicked(self, _):
        self.destroy()


class TranslationPage():
    def __init__(self):
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.element.set_border_width(10)
        instructions = Gtk.Label(
            label="Aceita valores numéricos (positivos e negativos).")
        instructions.set_xalign(0)
        instructions.set_margin_bottom(10)

        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        input_box.set_border_width(10)
        self.entry_x = Gtk.Entry()
        self.entry_x.set_text("0")
        self.entry_x.set_placeholder_text("X")

        self.entry_y = Gtk.Entry()
        self.entry_y.set_text("0")
        self.entry_y.set_placeholder_text("Y")

        input_box.pack_start(Gtk.Label(label="X:"), False, False, 0)
        input_box.pack_start(self.entry_x, True, True, 0)
        input_box.pack_start(Gtk.Label(label="Y:"), False, False, 0)
        input_box.pack_start(self.entry_y, True, True, 0)
        self.element.pack_start(input_box, False, False, 0)
        self.element.pack_start(instructions, False, False, 0)


class RotationPage():
    def __init__(self):
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.element.set_border_width(10)
        self.buttons = []

        self.add_radio_button("Em torno do centro do mundo", 1)
        self.add_radio_button("Em torno do centro do objeto", 2)
        self.add_radio_button("Em torno de um ponto", 3)

        main_input_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_input_box.set_border_width(10)

        angle_input_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        angle_input = Gtk.Entry()
        angle_input.set_text("0")
        angle_input_box.pack_start(
            Gtk.Label(label="Ângulo (em graus):"), False, False, 0)
        angle_input_box.pack_start(angle_input, False, False, 0)

        self.point_input_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        point_input = Gtk.Entry()
        point_input.set_placeholder_text("(x, y)")
        self.point_input_box.pack_start(
            Gtk.Label(label="Ponto de rotação:"), False, False, 0)
        self.point_input_box.pack_start(point_input, False, False, 0)
        self.point_input_box.set_sensitive(False)

        for button in self.buttons:
            self.element.pack_start(button, False, False, 0)

        main_input_box.pack_start(angle_input_box, False, False, 0)
        main_input_box.pack_start(self.point_input_box, False, False, 0)
        self.element.pack_start(main_input_box, False, False, 0)

    def add_radio_button(self, name, radio_type):
        if len(self.buttons) == 0:
            button = Gtk.RadioButton.new_with_label_from_widget(
                None, name)
        else:
            button = Gtk.RadioButton.new_with_label_from_widget(
                self.buttons[0], name)
        button.connect("toggled", self.on_toggle, radio_type)
        self.buttons.append(button)

    def on_toggle(self, button, radio_type):
        if button.get_active():
            self.selected_radio = radio_type
            self.point_input_box.set_sensitive(radio_type == 3)


class ScalingPage():
    def __init__(self):
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.element.set_border_width(10)

        instructions = Gtk.Label(
            label="Aceita valores numéricos (positivos)\nPara diminuir um objeto, insira um valor entre 0 e 1.\nPara aumentar um objeto, insira um valor maior que 1.")
        instructions.set_xalign(0)
        instructions.set_margin_bottom(10)

        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        input_box.set_border_width(10)
        self.entry_x = Gtk.Entry()
        self.entry_x.set_text("1")
        self.entry_x.set_placeholder_text("X")

        self.entry_y = Gtk.Entry()
        self.entry_y.set_text("1")
        self.entry_y.set_placeholder_text("Y")
        input_box.pack_start(Gtk.Label(label="X:"), False, False, 0)
        input_box.pack_start(self.entry_x, True, True, 0)
        input_box.pack_start(Gtk.Label(label="Y:"), False, False, 0)
        input_box.pack_start(self.entry_y, True, True, 0)
        self.element.pack_start(input_box, False, False, 0)
        self.element.pack_start(instructions, False, False, 0)
