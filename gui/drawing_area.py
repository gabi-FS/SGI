from gi.repository import Gtk


class DrawingArea():

    """
    _element: Gtk.DrawingArea
    _external_on_draw: Função que recebe o context do Cairo
    """

    def __init__(self, grid: Gtk.Grid, viewport_size):
        self._external_on_draw = None
        self._element = Gtk.DrawingArea()
        self._element.set_size_request(viewport_size, viewport_size)
        self._element.set_hexpand(True)
        self._element.set_vexpand(True)
        self._element.connect("draw", self._on_draw)

        grid.attach(self._element, 1, 0, 2, 2)

    def connect_on_draw(self, on_draw):
        ''' Determina uma função que será executada no fluxo da on_draw'''
        self._external_on_draw = on_draw

    def queue_draw(self):
        """ Força o redesenho da tela """
        self._element.queue_draw()

    def _on_draw(self, _, context):
        ''' Função que executa toda vez que o evento DRAW é disparado.
        O evento pode ser forçado a ser executado utilizando .queue_draw() na adição de novos elementos.
        '''

        # context.set_source_rgb(1, 1, 1)
        # context.paint()

        if self._external_on_draw:
            self._external_on_draw(context)
