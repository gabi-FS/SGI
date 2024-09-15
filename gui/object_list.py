from gi.repository import Gtk

from gui.transform_window import TransformWindow


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
        # Setar para False depois, por enquanto só pra facilitar desenvolvimento
        self._transform_button.set_sensitive(True)

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
        modal_window = TransformWindow(self.element)
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
