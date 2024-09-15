from gi.repository import Gtk


class ObjectList():
    """
    element: Gtk.ScrolledWindow
    listbox: Gtk.ListBox
    selected_object: int
    """

    def __init__(self, parent_component):
        """ parent_component: Gtk.Box """

        self.selected_object = None
        self._config_element()
        self._transform_button = Gtk.Button(label="Transformar")
        self._transform_button.connect("clicked", self.on_transform)
        self._transform_button.set_sensitive(False)

        parent_component.add_element(Gtk.Label(label="Objetos"))
        parent_component.add_element(Gtk.HSeparator())
        parent_component.add_element(self.element)
        parent_component.add_element(self._transform_button)
        parent_component.add_element(Gtk.HSeparator())

    def add_item(self, item_text: str, object_id: int):
        self.listbox.add(self._create_row(item_text, object_id))
        self.listbox.show_all()  # Atualiza a exibição

    def on_transform(self, _):
        # Abrir a modal, na verdade
        print(self.selected_object)
        modal_window = ModalWindow(self.element)
        modal_window.show_all()

    def on_row_selected(self, _, row):
        if row:
            self.selected_object = row.id
            self._transform_button.set_sensitive(True)
        else:
            self.selected_object = None
            self._transform_button.set_sensitive(False)

    def _config_element(self):
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(
            Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self.on_row_selected)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.listbox)
        scrolled_window.set_size_request(-1, 100)

        self.element = scrolled_window

    def _create_row(self, text: str, id: int):
        row = Gtk.ListBoxRow()
        row.id = id
        label = Gtk.Label(label=text)
        label.set_xalign(0)
        label.set_margin_top(2)
        label.set_margin_bottom(2)
        label.set_margin_start(2)
        label.set_margin_end(2)
        row.add(label)
        return row


class ModalWindow(Gtk.Window):
    def __init__(self, widget):
        super().__init__(title="Janela Modal")
        self.set_modal(True)  # Define a janela como modal
        self.set_default_size(300, 150)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        label = Gtk.Label(label="Nome:")
        entry = Gtk.Entry()
        box.pack_start(label, True, True, 0)
        box.pack_start(entry, True, True, 0)

        close_button = Gtk.Button(label="Fechar")
        close_button.connect("clicked", self.on_close_clicked)
        box.pack_start(close_button, True, True, 0)

        # Obtém a janela base a partir do widget passado
        parent_window = widget.get_toplevel()
        self.set_transient_for(parent_window)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def on_close_clicked(self, widget):
        self.destroy()  # Fecha a janela modal
