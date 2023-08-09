import fractions
import auxi
import globals
import config


class ResizableTriangle:
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, **kwargs):
        self.canvas = canvas
        self.id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline='black', **kwargs)
        self.original_coords = (x1, y1, x2, y2, x3, y3)
        self.canvas.tag_bind(self.id, '<Button-1>', self.on_press)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.press = None
        self.resizing = None
        self.mirror_figures = []

    def on_press(self, event):
        globals.last_touched_figure = self
        self.press = (event.x, event.y)
        x1, y1, x2, y2, x3, y3 = self.get_coords()
        tolerance = 15

        if abs(x1 - event.x) < 10 and abs(y1 - event.y) < tolerance:
            self.resizing = 'v1'
        elif abs(x2 - event.x) < 10 and abs(y2 - event.y) < tolerance:
            self.resizing = 'v2'
        elif abs(x3 - event.x) < 10 and abs(y3 - event.y) < tolerance:
            self.resizing = 'v3'
        else:
            self.resizing = None

    def on_drag(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        x1, y1, x2, y2, x3, y3 = self.get_coords()

        if self.resizing:
            if self.resizing == 'v1':
                x1, y1 = event.x, event.y
            elif self.resizing == 'v2':
                x2, y2 = event.x, event.y
            elif self.resizing == 'v3':
                x3, y3 = event.x, event.y

            if config.ENABLE_CANVAS_LIMIT:
                x1 = max(0, min(canvas_width, x1))
                y1 = max(0, min(canvas_height, y1))
                x2 = max(0, min(canvas_width, x2))
                y2 = max(0, min(canvas_height, y2))
                x3 = max(0, min(canvas_width, x3))
                y3 = max(0, min(canvas_height, y3))

            self.canvas.coords(self.id, x1, y1, x2, y2, x3, y3)
        else:
            dx = event.x - self.press[0]
            dy = event.y - self.press[1]

            new_x1, new_y1 = x1 + dx, y1 + dy
            new_x2, new_y2 = x2 + dx, y2 + dy
            new_x3, new_y3 = x3 + dx, y3 + dy

            if config.ENABLE_CANVAS_LIMIT:
                min_x = min(new_x1, new_x2, new_x3)
                max_x = max(new_x1, new_x2, new_x3)
                min_y = min(new_y1, new_y2, new_y3)
                max_y = max(new_y1, new_y2, new_y3)

                if min_x < 0:
                    dx -= min_x
                if min_y < 0:
                    dy -= min_y
                if max_x > canvas_width:
                    dx -= (max_x - canvas_width)
                if max_y > canvas_height:
                    dy -= (max_y - canvas_height)

            self.canvas.move(self.id, dx, dy)
            self.press = (event.x, event.y)

        self.update_aspect_ratio()
        self.update_mirror_figures()

    def on_release(self, event):
        self.press = None
        self.resizing = None

    def update_mirror_figures(self):
        x1, y1, x2, y2, x3, y3 = self.get_coords()
        for mirror_figure in self.mirror_figures:
            if mirror_figure.canvas.winfo_exists():
                if globals.ENABLE_RELATIVE_POSITION:
                    canvas_width = self.canvas.winfo_width()
                    canvas_height = self.canvas.winfo_height()
                    mirror_canvas_width = mirror_figure.canvas.winfo_width()
                    mirror_canvas_height = mirror_figure.canvas.winfo_height()
                    new_x1 = x1 * mirror_canvas_width / canvas_width
                    new_y1 = y1 * mirror_canvas_height / canvas_height
                    new_x2 = x2 * mirror_canvas_width / canvas_width
                    new_y2 = y2 * mirror_canvas_height / canvas_height
                    mirror_figure.canvas.coords(mirror_figure.id, new_x1, new_y1, new_x2, new_y2)
                else:
                    mirror_figure.canvas.coords(mirror_figure.id, x1, y1, x2, y2)

    def update_aspect_ratio(self):
        try:
            x1, y1, x2, y2, x3, y3 = self.get_coords()

            min_x = min(x1, x2, x3)
            max_x = max(x1, x2, x3)
            min_y = min(y1, y2, y3)
            max_y = max(y1, y2, y3)

            width = max_x - min_x
            height = max_y - min_y

            if height != 0:
                aspect_ratio = width / height
                fraction = fractions.Fraction(int(width), int(height))
                fraction_str = str(fraction).replace("/", ":")
            else:
                aspect_ratio = float('inf')
                fraction_str = "Indefinido"

            globals.aspect_ratio_label.config(
                text=auxi.get_aspect_ratio_message2(fraction_str, aspect_ratio, width, height))
        except ValueError:
            pass
        except ZeroDivisionError:
            pass

    def reset(self):
        self.canvas.coords(self.id, *self.original_coords)
        self.update_aspect_ratio()

    def set_fill_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def update(self):
        x1, y1, x2, y2, x3, y3 = self.canvas.coords(self.id)
        for mirror_triangle in self.mirror_triangle:
            mirror_triangle.canvas.coords(mirror_triangle.id, x1, y1, x2, y2)

    def get_coords(self):
        return self.canvas.coords(self.id)
