import tkinter as tk


class ResizableRectangle:
    def __init__(self, canvas, x1, y1, x2, y2, **kwargs):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        self.canvas.tag_bind(self.id, '<Button-1>', self.on_press)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.press = None

    def on_press(self, event):
        self.press = (event.x, event.y)

    def on_drag(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        dx = event.x - self.press[0]
        dy = event.y - self.press[1]
        self.canvas.coords(self.id, x1, y1, x2 + dx, y2 + dy)
        self.press = (event.x, event.y)
        self.update_aspect_ratio()

    def on_release(self, event):
        self.press = None
        self.update_aspect_ratio()

    def update_aspect_ratio(self):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        aspect_ratio = width / height if height != 0 else 0
        aspect_ratio_label.config(text=f"Aspect Ratio: {aspect_ratio:.2f} ({width:.0f}:{height:.0f})")


root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

aspect_ratio_label = tk.Label(root, text="")
aspect_ratio_label.pack()

rectangle = ResizableRectangle(canvas, 50, 50, 200, 200, fill='green')

root.mainloop()
