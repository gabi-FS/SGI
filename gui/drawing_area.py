from gi.repository import Gdk, Gtk


class DrawingArea():

    """
    _element: Gtk.DrawingArea
    _external_on_draw: Função que recebe o context do Cairo
    _scroll_up: Função executada no scroll up
    _scroll_down: Função executada no scroll down
    _move_up
    _move_left
    _move_right
    _move_down
    """

    def __init__(self, grid: Gtk.Grid, viewport_size):
        self._element = Gtk.DrawingArea()
        self._element.set_size_request(viewport_size, viewport_size)
        self._element.set_hexpand(True)
        self._element.set_vexpand(True)

        self._element.set_events(Gdk.EventMask.SCROLL_MASK)
        self._element.connect("draw", self._on_draw)
        self._element.connect("scroll-event", self._on_scroll)

        # KEY EVENTS: NOT CONFIGURED YET
        # self._element.connect("key-press-event", self._on_key_press)

        grid.attach(self._element, 1, 0, 2, 2)

    def connect_on_draw(self, on_draw):
        ''' Determina uma função que será executada no fluxo da on_draw'''
        self._external_on_draw = on_draw

    def connect_scroll_up_down(self, scroll_up, scroll_down):
        ''' Determina as funções para os eventos de scroll '''
        self._scroll_up = scroll_up
        self._scroll_down = scroll_down

    # def connect_movement_keys(self, up, left, right, down):
    #     """ Determina as funções para as teclas de movimento (setas e wasd)"""
    #     self._move_up = up
    #     self._move_left = left
    #     self._move_right = right
    #     self._move_down = down

    def queue_draw(self):
        """ Força o redesenho da tela """
        self._element.queue_draw()

    def _on_draw(self, _, context):
        ''' Função que executa toda vez que o evento DRAW é disparado.
        O evento pode ser forçado a ser executado utilizando .queue_draw() na adição de novos elementos.
        '''

        if self._external_on_draw:
            self._external_on_draw(context)

    def _on_scroll(self, _, event):
        if event.direction == Gdk.ScrollDirection.UP and self._scroll_up:
            self._scroll_up()
        elif event.direction == Gdk.ScrollDirection.DOWN and self._scroll_down:
            self._scroll_down()

    # def _on_key_press(self, _, event):
    #     key = Gdk.keyval_name(event.keyval)
    #     if (key == "w") and self._move_up:
    #         self._move_up()
    #     elif (key == "a") and self._move_left:
    #         self._move_left()
    #     elif (key == "s") and self._move_down:
    #         self._move_down()
    #     elif (key == "d") and self._move_right:
    #         self._move_right()
