from gi.repository import Gtk


class MenuBox():
    def __init__(self, grid):
        self.element = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.element.set_border_width(10)
        grid.attach(self.element, 0, 0, 1, 2)

        title_label = Gtk.Label()
        title_label.set_markup("<b>Menu de Funções</b>")
        self.add_element(title_label)
        self.add_element(Gtk.HSeparator())

        self.object_list = ObjectList(self)
        self.object_form = ObjectForm(self)

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
        menu_box.add_element(Gtk.HSeparator())

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


class ObjectForm():
    def __init__(self, menu_box: MenuBox):
        self.object_radio = ObjectRadio()
        self.name_input = Gtk.Entry()
        self.coordinate_input = Gtk.Entry()
        self.coordinate_input.set_placeholder_text(
            "(x1, y1), (x2, y2),...")

        # Button -> Posso conectar uma função de fora também se necessário no futuro.
        self.submit_button = Gtk.Button.new_with_label("Adicionar objeto")
        self.submit_button.connect("clicked", self.on_add)

        menu_box.add_element(Gtk.Label(label="Criação de objeto"))
        menu_box.add_element(self.object_radio.element)
        menu_box.add_element(self.create_form_label(
            "Nome do objeto (Opcional):"))
        menu_box.add_element(self.name_input)
        menu_box.add_element(self.create_form_label(
            "Coordenadas (Obrigatório):"))
        menu_box.add_element(self.coordinate_input)
        menu_box.add_element(self.submit_button)

    def create_form_label(self, name):
        form_label = Gtk.Label()
        form_label.set_markup(f"<b>{name}</b>")
        form_label.set_xalign(0)
        return form_label

    def on_add(self, button):
        print(f"Selecionado: {self.object_radio.selected_name}")
        print(f"Nome: {self.name_input.get_text()}")
        print(f"Coordenadas: {self.coordinate_input.get_text()}")
        self.clear_form()  # Avaliar necessidade

    def clear_form(self):
        self.name_input.set_text("")
        self.coordinate_input.set_text("")


class ObjectRadio():
    def __init__(self):
        self.element = Gtk.Box(spacing=10)
        self.selected_name = "Ponto"  # Modo de acessar tipo de objeto que estou criando
        self.buttons = []

        first_button = Gtk.RadioButton.new_with_label_from_widget(
            None, self.selected_name)
        first_button.connect("toggled", self.on_toggle, self.selected_name)
        self.buttons.append(first_button)

        self.add_button("Reta")
        self.add_button("Polígono")

        for button in self.buttons:
            self.element.pack_start(button, False, False, 0)

    def add_button(self, name):
        button = Gtk.RadioButton.new_with_label_from_widget(
            self.buttons[0], name)
        button.connect("toggled", self.on_toggle, name)
        self.buttons.append(button)

    def on_toggle(self, button, name):
        if button.get_active():
            self.selected_name = name
