from gi.repository import Gtk


class ObjectList():
    def __init__(self, menu_box):
        self.selected_object = None  # Tratar

        self.config_element()

        menu_box.add_element(Gtk.Label(label="Objetos"))
        menu_box.add_element(Gtk.HSeparator())
        menu_box.add_element(self.element)
        menu_box.add_element(Gtk.HSeparator())

    def config_element(self):
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(
            Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self.on_row_selected)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.listbox)
        scrolled_window.set_size_request(-1, 100)

        self.element = scrolled_window

    def add_item(self, item_text):
        self.listbox.add(self._create_row(item_text))
        self.listbox.show_all()  # Atualiza a exibição

    # TODO: Tratar remoção de objeto no futuro

    def on_row_selected(self, _, row):
        if row:
            label = row.get_child()
            # Atualmente texto, depois configurar dependendo dos objetos!
            self.selected_object = label.get_text()
            print(f"Selecionado: {self.selected_object}")
        else:
            self.selected_object = None

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
