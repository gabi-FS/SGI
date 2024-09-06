from gi.repository import Gtk


class ObjectList():
    def __init__(self, menu_box):
        # Basicamente o que vai ser alterado pelas outras ações! No futuro, pode ser realmente uma lista de objetos de tipo X, aí printo object.name
        # Tratarei como strings no momento.
        self.objects = []
        self.selected_object = None  # Tratar

        # Teste de adição de itens
        for i in range(20):
            self.objects.append(f"Item {i+1}")

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

        for obj in self.objects:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=obj)
            label.set_xalign(0)
            label.set_margin_top(2)
            label.set_margin_bottom(2)
            label.set_margin_start(2)
            label.set_margin_end(2)
            row.add(label)
            self.listbox.add(row)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.listbox)
        scrolled_window.set_size_request(-1, 100)

        self.element = scrolled_window

    def on_row_selected(self, listbox, row):
        if row:
            label = row.get_child()
            # Atualmente texto, depois configurar dependendo dos objetos!
            self.selected_object = label.get_text()
            print(f"Selecionado: {self.selected_object}")
        else:
            self.selected_object = None
