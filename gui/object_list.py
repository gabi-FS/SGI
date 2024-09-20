from typing import Any, Callable, Dict

from gi.repository import Gtk

from globals import TransformationType
from gui.transform_window import TransformWindow


class ObjectList:
    selected_object: int
    element: Gtk.ScrolledWindow
    listbox: Gtk.ListBox
    _transform_button: Gtk.Button
    _on_apply_transform: Callable[[int, Dict[TransformationType, Any]], int]

    def __init__(self, parent_component):
        """ parent_component: MenuBox """

        self.selected_object = None
        self._config_element()
        self._transform_button = Gtk.Button(label="Transformar")
        self._transform_button.connect("clicked", self._on_transform)
        self._transform_button.set_sensitive(False)

        parent_component.add_element(Gtk.Label(label="Objetos"))
        parent_component.add_element(Gtk.Separator())
        parent_component.add_element(self.element)
        parent_component.add_element(self._transform_button)
        parent_component.add_element(Gtk.Separator())

    def add_item(self, item_text: str, object_id: int):
        self.listbox.add(self._create_row(item_text, object_id))
        self.listbox.show_all()  # Atualiza a exibição

    def set_on_apply_transform(self, on_apply: Callable[[int, Dict[TransformationType, Any]], int]):
        self._on_apply_transform = on_apply

    def _on_row_selected(self, _, row: Gtk.ListBoxRow):
        if row:
            self.selected_object = row.id
            self._transform_button.set_sensitive(True)
        else:
            self.selected_object = None
            self._transform_button.set_sensitive(False)

    def _on_transform(self, _):
        modal_window = TransformWindow(self.element, self.selected_object, self._on_apply_transform)
        modal_window.show_all()

    def _config_element(self):
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self._on_row_selected)

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
