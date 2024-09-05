from gi.repository import Gtk


class MenuBox():
    def __init__(self, grid):
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        grid.attach(self.element, 0, 0, 1, 2)

        self.add_element(Gtk.Label(label="Menu de Funções"))
        self.add_element(Gtk.HSeparator())

        self.object_list = ObjectList(self)

        self.element.set_hexpand(False)

    def add_element(self, new_element):
        self.element.pack_start(new_element, False, True, 0)

# Dependendo da quantidade, adicionar mais arquivos pra separar as classes (não gosto de scroll vertical, perdão)
# Mas só se não fizer tudo explodir


class ObjectList():
    # Maybe usar padrão que o elemento tem a si próprio, o pai e todos os filhos, se for necessário no futuro...

    def __init__(self, menu_box: MenuBox):
        # Basicamente o que vai ser alterado pelas outras ações! No futuro, pode ser realmente uma lista de objetos de tipo X, aí printo object.name
        # Tratarei como strings no momento.
        self.objects = []
        self.selected_object = None  # Tratar

        # Teste de adição de itens
        for i in range(20):
            self.objects.append(f"Item {i+1}")

        self.config_element()

        menu_box.add_element(Gtk.Label(label="Objetos"))
        menu_box.add_element(self.element)

    def config_element(self):
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)  # Seleção única

        for obj in self.objects:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=obj)
            label.set_xalign(0)
            row.add(label)
            listbox.add(row)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(listbox)
        scrolled_window.set_size_request(-1, 100)

        self.element = scrolled_window
