from gi.repository import Gtk

from .object_form import ObjectForm, ObjectWindow
from .object_list import ObjectList
from .window_form import WindowForm


class MenuBox:
    element: Gtk.Box
    object_list: ObjectList
    object_form: ObjectForm
    window_form: WindowForm

    def __init__(self, grid: Gtk.Grid):
        self.element = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        self.external_on_create_object = None

        title_label = Gtk.Label()
        title_label.set_markup("<b>Menu de Funções</b>")
        self.add_element(title_label)
        self.add_element(Gtk.Separator())

        # Atualmente, o acesso/conexão de botões e funções estarão ao nível de FORM.
        # Essa classe, então, sendo apenas um WRAPPER.
        self.object_list = ObjectList(self)
        create_object_button = Gtk.Button(label="Criar novo objeto")
        create_object_button.connect("clicked", self.on_create_object)
        self.add_element(create_object_button)
        self.add_element(Gtk.Separator())
        self.window_form = WindowForm(self)

        grid.attach(self.element, 0, 0, 1, 2)

    def add_element(self, new_element: Gtk.Widget):
        self.element.pack_start(new_element, False, True, 0)

    def on_create_object(self, _):
        modal_window = ObjectWindow(ObjectForm(self.external_on_create_object), self.element)
        modal_window.show_all()

    def set_on_create_object(self, func):
        self.external_on_create_object = func
