import globals
import config

CANVAS_HEIGHT = config.CANVAS_HEIGHT
CANVAS_WIDTH = config.CANVAS_WIDTH


def move_up(event):
    if globals.last_touched_figure is not None:
        x1, y1, x2, y2 = globals.last_touched_figure.get_coords()
        if y1 - 5 >= 0:
            globals.last_touched_figure.canvas.move(globals.last_touched_figure.id, 0, -5)


def move_down(event):
    if globals.last_touched_figure is not None:
        x1, y1, x2, y2 = globals.last_touched_figure.get_coords()
        if y2 + 5 <= CANVAS_HEIGHT:
            globals.last_touched_figure.canvas.move(globals.last_touched_figure.id, 0, 5)


def move_left(event):
    if globals.last_touched_figure is not None:
        x1, y1, x2, y2 = globals.last_touched_figure.get_coords()
        if x1 - 5 >= 0:
            globals.last_touched_figure.canvas.move(globals.last_touched_figure.id, -5, 0)


def move_right(event):
    if globals.last_touched_figure is not None:
        x1, y1, x2, y2 = globals.last_touched_figure.get_coords()
        if x2 + 5 <= CANVAS_WIDTH:
            globals.last_touched_figure.canvas.move(globals.last_touched_figure.id, 5, 0)
