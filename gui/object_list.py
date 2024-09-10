from gi.repository import Gtk


class ObjectList():
    """
    element: Gtk.ScrolledWindow
    listbox: Gtk.ListBox
    selected_object: str
    """

    def __init__(self, parent_component):
        """ parent_component: Gtk.Box """

        # TODO: Tratar modelagem da seleção de objetos.
        self.selected_object = None
        self._config_element()

        parent_component.add_element(Gtk.Label(label="Objetos"))
        parent_component.add_element(Gtk.HSeparator())
        parent_component.add_element(self.element)
        parent_component.add_element(Gtk.HSeparator())

    def add_item(self, item_text):
        self.listbox.add(self._create_row(item_text))
        self.listbox.show_all()  # Atualiza a exibição

    def on_row_selected(self, _, row):
        if row:
            label = row.get_child()
            self.selected_object = label.get_text()
        else:
            self.selected_object = None

    def _config_element(self):
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(
            Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self.on_row_selected)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.listbox)
        scrolled_window.set_size_request(-1, 100)

        self.element = scrolled_window

    def _create_row(self, text):
        row = Gtk.ListBoxRow()
        label = Gtk.Label(label=text)
        label.set_xalign(0)
        label.set_margin_top(2)
        label.set_margin_bottom(2)
        label.set_margin_start(2)
        label.set_margin_end(2)
        row.add(label)
        return row
