import fractions
import auxi
import globals


class ResizableCircle:
    def __init__(self, canvas, x1, y1, x2, y2, **kwargs):
        self.canvas = canvas
        self.id = self.canvas.create_oval(x1, y1, x2, y2, **kwargs)
        self.handle = self.canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='red')
        self.original_coords = (x1, y1, x2, y2)
        self.canvas.tag_bind(self.id, '<Button-1>', self.on_press)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.press = None
        self.resizing = False

    def on_press(self, event):

        globals.last_touched_figure = self
        self.press = (event.x, event.y)
        x1, y1, x2, y2 = self.get_coords()
        if abs(x2 - event.x) < 10 and abs(y2 - event.y) < 10:
            self.resizing = True

    def on_drag(self, event):
        if self.resizing:
            x1, y1, x2, y2 = self.get_coords()
            new_x2, new_y2 = event.x, event.y
            self.canvas.coords(self.handle, new_x2 - 5, new_y2 - 5, new_x2 + 5, new_y2 + 5)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if new_x2 < 0:
                new_x2 = 0
            elif new_x2 > canvas_width:
                new_x2 = canvas_width
            if new_y2 < 0:
                new_y2 = 0
            elif new_y2 > canvas_height:
                new_y2 = canvas_height
            self.canvas.coords(self.id, x1, y1, new_x2, new_y2)
        else:
            dx = event.x - self.press[0]
            dy = event.y - self.press[1]
            x1, y1, x2, y2 = self.get_coords()
            new_x1, new_y1 = x1 + dx, y1 + dy
            new_x2, new_y2 = x2 + dx, y2 + dy
            self.canvas.move(self.handle, dx, dy)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if new_x1 < 0:
                dx = -x1
            elif new_x2 > canvas_width:
                dx = canvas_width - x2
            if new_y1 < 0:
                dy = -y1
            elif new_y2 > canvas_height:
                dy = canvas_height - y2
            self.canvas.move(self.id, dx, dy)
            self.press = (event.x, event.y)
        self.update_aspect_ratio()

    def on_release(self, event):
        self.press = None
        self.resizing = False
        self.update_aspect_ratio()

    def update_aspect_ratio(self):
        x1, y1, x2, y2 = self.get_coords()
        self.canvas.coords(self.handle, x2 - 5, y2 - 5, x2 + 5, y2 + 5)
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

    def reset(self):
        self.canvas.coords(self.id, *self.original_coords)
        x1, y1, x2, y2 = self.get_coords()
        self.canvas.coords(self.handle, x2 - 5, y2 - 5, x2 + 5, y2 + 5)
        self.canvas.coords(self.id, *self.original_coords)
        self.update_aspect_ratio()

    def set_fill_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def get_coords(self):
        return self.canvas.coords(self.id)
