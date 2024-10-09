from typing import Callable

import cairo
from gi.repository import Gdk, Gtk


class DrawingArea:
    _element: Gtk.DrawingArea
    _external_on_draw: Callable[[cairo.Context], None]
    _scroll_up: Callable[[], None]
    _scroll_down: Callable[[], None]

    def __init__(self, grid: Gtk.Grid, viewport_size):
        self._element = Gtk.DrawingArea()
        self._element.set_size_request(viewport_size, viewport_size)
        self._element.set_hexpand(True)
        self._element.set_vexpand(True)

        self._element.set_events(Gdk.EventMask.SCROLL_MASK)
        self._element.connect("draw", self._on_draw)
        self._element.connect("scroll-event", self._on_scroll)

        grid.attach(self._element, 1, 0, 1, 2)

    def connect_on_draw(self, on_draw):
        """Determina uma função que será executada no fluxo da on_draw"""
        self._external_on_draw = on_draw

    def connect_scroll_up_down(self, scroll_up, scroll_down):
        """Determina as funções para os eventos de scroll"""
        self._scroll_up = scroll_up
        self._scroll_down = scroll_down

    def queue_draw(self):
        """Força o redesenho da tela"""
        self._element.queue_draw()

    def _on_draw(self, _, context: cairo.Context):
        """
        Função que executa toda vez que o evento DRAW é disparado.
        O evento pode ser forçado a ser executado utilizando queue_draw() na adição de novos elementos.
        """
        if self._external_on_draw:
            self._external_on_draw(context)

    def _on_scroll(self, _, event):
        if event.direction == Gdk.ScrollDirection.UP and self._scroll_up:
            self._scroll_up()
        elif event.direction == Gdk.ScrollDirection.DOWN and self._scroll_down:
            self._scroll_down()
