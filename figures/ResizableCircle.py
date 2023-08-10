import fractions
from utils import globals, auxi
import config


class ResizableCircle:
    def __init__(self, canvas, x1, y1, x2, y2, **kwargs):
        self.canvas = canvas
        self.id = self.canvas.create_oval(x1, y1, x2, y2, **kwargs)
        self.original_coords = (x1, y1, x2, y2)
        self.canvas.tag_bind(self.id, '<Button-1>', self.on_press)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.press = None
        self.resizing = False
        self.mirror_figures = []

    def on_press(self, event):
        globals.last_touched_figure = self
        self.press = (event.x, event.y)
        x1, y1, x2, y2 = self.get_coords()
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        distance_to_center = ((event.x - center_x) ** 2 + (event.y - center_y) ** 2) ** 0.5
        radius = ((x2 - center_x) ** 2 + (y2 - center_y) ** 2) ** 0.5
        tolerance = 0.35 * radius

        if abs(distance_to_center - radius) < tolerance:
            self.resizing = True
        else:
            self.resizing = False

    def on_drag(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if self.resizing:
            x1, y1, x2, y2 = self.get_coords()
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = event.x - center_x, event.y - center_y
            new_radius = (dx ** 2 + dy ** 2) ** 0.5
            new_x1, new_y1 = center_x - new_radius, center_y - new_radius
            new_x2, new_y2 = center_x + new_radius, center_y + new_radius

            if config.ENABLE_CANVAS_LIMIT:
                new_x1 = max(0, new_x1)
                new_y1 = max(0, new_y1)
                new_x2 = min(canvas_width, new_x2)
                new_y2 = min(canvas_height, new_y2)

            self.canvas.coords(self.id, new_x1, new_y1, new_x2, new_y2)
        else:
            dx = event.x - self.press[0]
            dy = event.y - self.press[1]

            x1, y1, x2, y2 = self.get_coords()
            new_x1 = x1 + dx
            new_y1 = y1 + dy
            new_x2 = x2 + dx
            new_y2 = y2 + dy

            if config.ENABLE_CANVAS_LIMIT:
                if new_x1 < 0:
                    dx -= new_x1
                if new_y1 < 0:
                    dy -= new_y1
                if new_x2 > canvas_width:
                    dx -= (new_x2 - canvas_width)
                if new_y2 > canvas_height:
                    dy -= (new_y2 - canvas_height)

            self.canvas.move(self.id, dx, dy)
            self.press = (event.x, event.y)

        self.update_aspect_ratio()
        self.update_mirror_figures()

    def on_release(self, event):
        self.press = None
        self.resizing = False
        self.update_aspect_ratio()

    def update_mirror_figures(self):
        x1, y1, x2, y2 = self.get_coords()
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
        x1, y1, x2, y2 = self.get_coords()
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        if height != 0:
            aspect_ratio = width / height if height != 0 else 0
            fraction = fractions.Fraction(int(width), int(height))
            if fraction.denominator == 1:
                fraction_str = f"{fraction.numerator}:1"
            else:
                fraction_str = str(fraction).replace("/", ":")
            globals.aspect_ratio_label.config(
                text=auxi.get_aspect_ratio_message2(fraction_str, aspect_ratio, width, height))

    def set_fill_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def reset(self):
        self.canvas.coords(self.id, *self.original_coords)
        self.update_aspect_ratio()

    def update(self):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        for mirror_rectangle in self.mirror_rectangles:
            mirror_rectangle.canvas.coords(mirror_rectangle.id, x1, y1, x2, y2)

    def get_coords(self):
        return self.canvas.coords(self.id)
