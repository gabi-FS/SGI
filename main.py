import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

print("GTK+ version:", Gtk.get_major_version(), Gtk.get_minor_version())
