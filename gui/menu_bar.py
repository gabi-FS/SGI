from gi.repository import Gtk


class MenuBar:
    def __init__(self):
        self.element = Gtk.MenuBar()
        file_menu_item = Gtk.MenuItem(label="Arquivo")
        file_menu = Gtk.Menu()
        file_menu_item.set_submenu(file_menu)

        import_item = Gtk.MenuItem(label="Importar")
        export_item = Gtk.MenuItem(label="Exportar")
        file_menu.append(import_item)
        file_menu.append(export_item)

        self.element.append(file_menu_item)
