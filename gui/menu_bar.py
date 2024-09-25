from typing import Any, Callable

from gi.repository import Gtk


class MenuBar:
    element: Gtk.MenuBar
    import_function: Callable[[str], Any]
    export_function: Callable[[str], None]

    def __init__(self):
        self.element = Gtk.MenuBar()
        file_menu_item = Gtk.MenuItem(label="Arquivo")
        file_menu = Gtk.Menu()
        file_menu_item.set_submenu(file_menu)

        import_item = Gtk.MenuItem(label="Importar")
        import_item.connect("activate", self.on_import)
        export_item = Gtk.MenuItem(label="Exportar")
        export_item.connect("activate", self.on_export)
        file_menu.append(import_item)
        file_menu.append(export_item)

        self.element.append(file_menu_item)

    def connect_on_import(self, import_function: Callable[[str], None]):
        self.import_function = import_function

    def connect_on_export(self, export_function: Callable[[str], None]):
        self.export_function = export_function

    def on_import(self, _):
        dialog = Gtk.FileChooserDialog(
            title="Selecione um arquivo",
            parent=self.element.get_toplevel(),
            action=Gtk.FileChooserAction.OPEN
        )

        filter_obj = Gtk.FileFilter()
        filter_obj.set_name("Object File")
        filter_obj.add_pattern("*.obj")
        dialog.add_filter(filter_obj)

        filter_all = Gtk.FileFilter()
        filter_all.set_name("All Files")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)

        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if self.import_function:
                self.import_function(dialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            print("Seleção cancelada")

        dialog.destroy()

    def on_export(self, _):
        dialog = Gtk.FileChooserDialog(
            title="Salvar arquivo como",
            parent=self.element.get_toplevel(),
            action=Gtk.FileChooserAction.SAVE
        )

        filter_obj = Gtk.FileFilter()
        filter_obj.set_name("Object File")
        filter_obj.add_pattern("*.obj")
        dialog.add_filter(filter_obj)

        filter_all = Gtk.FileFilter()
        filter_all.set_name("All Files")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)

        dialog.set_current_name("object_file.obj")

        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if self.export_function:
                self.export_function(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Ação cancelada")

        dialog.destroy()
