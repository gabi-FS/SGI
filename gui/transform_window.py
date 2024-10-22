from typing import Any, Callable, Dict

from gi.repository import Gtk

from globals import RotationType, TransformationType, TranslationType


class TransformWindow(Gtk.Window):
    element: Gtk.Box
    selected_object_id: int
    notebook: Gtk.Notebook
    _external_on_apply: Callable[[int, Dict[TransformationType, Any]], int]

    def __init__(
        self,
        widget: Gtk.Widget,
        selected_object_id: int,
        external_on_apply: Callable[[int, Dict[TransformationType, Any]], int],
    ):
        super().__init__(title="Transformação do objeto")
        self.selected_object_id = selected_object_id
        self._external_on_apply = external_on_apply

        self.set_modal(True)
        self.set_default_size(900, 300)
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        self.add(self.element)

        self.notebook = Gtk.Notebook()
        self.translation_page = TranslationPage()
        self.rotation_page = RotationPage()
        self.scaling_page = ScalingPage()

        self.notebook.append_page(
            self.translation_page.element, Gtk.Label(label="Translação")
        )
        self.notebook.append_page(
            self.rotation_page.element, Gtk.Label(label="Rotação")
        )
        self.notebook.append_page(
            self.scaling_page.element, Gtk.Label(label="Escalonamento")
        )

        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_valign(Gtk.Align.END)
        cancel_button = Gtk.Button(label="Cancelar")
        cancel_button.connect("clicked", self.on_close_clicked)
        apply_button = Gtk.Button(label="Aplicar")
        apply_button.connect("clicked", self.on_apply)

        button_box.pack_start(cancel_button, False, False, 0)
        button_box.pack_start(apply_button, False, False, 0)

        self.element.pack_start(self.notebook, False, False, 0)
        self.element.pack_start(button_box, False, False, 0)
        self.set_transient_for(widget.get_toplevel())
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def on_close_clicked(self, _):
        self.destroy()

    def create_input_object(self):
        return {
            TransformationType.TRANSLATION: self.translation_page.get_input_object(),
            TransformationType.ROTATION: self.rotation_page.get_input_object(),
            TransformationType.SCALING: self.scaling_page.get_input_object(),
        }

    def on_apply(self, _):
        if self._external_on_apply:
            result = self._external_on_apply(
                self.selected_object_id, self.create_input_object()
            )
            if result == 1:  # SUCCESSFUL
                self.destroy()


class TranslationPage:
    element: Gtk.Box
    entry_x: Gtk.Entry
    entry_y: Gtk.Entry

    def __init__(self):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        instructions = Gtk.Label(
            label="Aceita valores numéricos (positivos e negativos)."
        )
        instructions.set_xalign(0)
        instructions.set_margin_bottom(10)

        self.buttons = []
        self.selected_radio = TranslationType.WORLD_AXIS
        self.add_radio_button("Em relação ao eixo do mundo", TranslationType.WORLD_AXIS)
        self.add_radio_button(
            "Em relação ao eixo da janela", TranslationType.SCREEN_AXIS
        )

        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        input_box.set_border_width(10)
        self.entry_x = Gtk.Entry()
        self.entry_x.set_placeholder_text("0")

        self.entry_y = Gtk.Entry()
        self.entry_y.set_placeholder_text("0")

        self.entry_z = Gtk.Entry()
        self.entry_z.set_placeholder_text("0")

        input_box.pack_start(Gtk.Label(label="X:"), False, False, 0)
        input_box.pack_start(self.entry_x, True, True, 0)
        input_box.pack_start(Gtk.Label(label="Y:"), False, False, 0)
        input_box.pack_start(self.entry_y, True, True, 0)
        input_box.pack_start(Gtk.Label(label="Z:"), False, False, 0)
        input_box.pack_start(self.entry_z, True, True, 0)

        for button in self.buttons:
            self.element.pack_start(button, False, False, 0)
        self.element.pack_start(input_box, False, False, 0)
        self.element.pack_start(instructions, False, False, 0)

    def add_radio_button(self, name, radio_type):
        if len(self.buttons) == 0:
            button = Gtk.RadioButton.new_with_label_from_widget(None, name)
        else:
            button = Gtk.RadioButton.new_with_label_from_widget(self.buttons[0], name)
        button.connect("toggled", self.on_toggle, radio_type)
        self.buttons.append(button)

    def on_toggle(self, button, radio_type):
        if button.get_active():
            self.selected_radio = radio_type

    def get_input_object(self):
        return {
            "x": self.entry_x.get_text(),
            "y": self.entry_y.get_text(),
            "z": self.entry_z.get_text(),
            "type": self.selected_radio,
        }


class RotationPage:
    def __init__(self):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.element.set_border_width(10)
        self.buttons = []
        self.selected_radio = RotationType.WORLD_CENTER
        self.add_radio_button("Em torno do centro do mundo", RotationType.WORLD_CENTER)
        self.add_radio_button(
            "Em torno do centro do objeto", RotationType.OBJECT_CENTER
        )
        self.add_radio_button("Em torno de um ponto", RotationType.AROUND_POINT)

        main_input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_input_box.set_border_width(10)

        # angle_input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        # self.angle_input = Gtk.Entry()
        # self.angle_input.set_placeholder_text("0")
        # angle_input_box.pack_start(
        #     Gtk.Label(label="Ângulo (em graus):"), False, False, 0
        # )
        # angle_input_box.pack_start(self.angle_input, False, False, 0)

        angle_input_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        angle_input_box.set_border_width(10)
        self.entry_x = Gtk.Entry()
        self.entry_x.set_placeholder_text("0")

        self.entry_y = Gtk.Entry()
        self.entry_y.set_placeholder_text("0")

        self.entry_z = Gtk.Entry()
        self.entry_z.set_placeholder_text("0")

        angle_input_box.pack_start(
            Gtk.Label(label="Ângulo (em graus):"), False, False, 0
        )

        angle_input_box.pack_start(Gtk.Label(label="X:"), False, False, 0)
        angle_input_box.pack_start(self.entry_x, True, True, 0)
        angle_input_box.pack_start(Gtk.Label(label="Y:"), False, False, 0)
        angle_input_box.pack_start(self.entry_y, True, True, 0)
        angle_input_box.pack_start(Gtk.Label(label="Z:"), False, False, 0)
        angle_input_box.pack_start(self.entry_z, True, True, 0)

        self.point_input_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10
        )
        self.point_input = Gtk.Entry()
        self.point_input.set_placeholder_text("(x, y)")
        self.point_input_box.pack_start(
            Gtk.Label(label="Ponto de rotação:"), False, False, 0
        )
        self.point_input_box.pack_start(self.point_input, False, False, 0)
        self.point_input_box.set_sensitive(False)

        main_input_box.pack_start(angle_input_box, False, False, 0)
        main_input_box.pack_start(self.point_input_box, False, False, 0)

        for button in self.buttons:
            self.element.pack_start(button, False, False, 0)
        self.element.pack_start(main_input_box, False, False, 0)

    def add_radio_button(self, name, radio_type):
        if len(self.buttons) == 0:
            button = Gtk.RadioButton.new_with_label_from_widget(None, name)
        else:
            button = Gtk.RadioButton.new_with_label_from_widget(self.buttons[0], name)
        button.connect("toggled", self.on_toggle, radio_type)
        self.buttons.append(button)

    def on_toggle(self, button, radio_type):
        if button.get_active():
            self.selected_radio = radio_type
            self.point_input_box.set_sensitive(RotationType.AROUND_POINT == radio_type)

    def get_input_object(self):
        return {
            "type": self.selected_radio,
            "x": self.entry_x.get_text(),
            "y": self.entry_y.get_text(),
            "z": self.entry_z.get_text(),
            "point": self.point_input.get_text(),
        }


class ScalingPage:
    element: Gtk.Box
    entry_x: Gtk.Entry
    entry_y: Gtk.Entry

    def __init__(self):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.element.set_border_width(10)

        instructions = Gtk.Label(
            label="Aceita valores numéricos;\nPara diminuir um objeto, insira um valor entre 0 e 1;\nPara aumentar um objeto, insira um valor maior que 1."
        )
        instructions.set_xalign(0)
        instructions.set_margin_bottom(10)

        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        input_box.set_border_width(10)
        self.entry_x = Gtk.Entry()
        self.entry_x.set_placeholder_text("1")

        self.entry_y = Gtk.Entry()
        self.entry_y.set_placeholder_text("1")

        self.entry_z = Gtk.Entry()
        self.entry_z.set_placeholder_text("1")

        input_box.pack_start(Gtk.Label(label="X:"), False, False, 0)
        input_box.pack_start(self.entry_x, True, True, 0)
        input_box.pack_start(Gtk.Label(label="Y:"), False, False, 0)
        input_box.pack_start(self.entry_y, True, True, 0)
        input_box.pack_start(Gtk.Label(label="Z:"), False, False, 0)
        input_box.pack_start(self.entry_z, True, True, 0)

        self.element.pack_start(input_box, False, False, 0)
        self.element.pack_start(instructions, False, False, 0)

    def get_input_object(self):
        return {
            "x": self.entry_x.get_text(),
            "y": self.entry_y.get_text(),
            "z": self.entry_z.get_text(),
        }
