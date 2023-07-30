import tkinter as tk
import config


class ResizableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Configure>", self.on_resize)
        self.press = None
        self.resizing = False
        if config.SHOW_RED_DOT_CANVAS:
            self.resize_indicator = self.create_oval(190, 190, 200, 200, fill='red')
        else:
            self.resize_indicator = self.create_oval(190, 190, 200, 200, outline=config.CANVAS_BACKGROUND_COLOR)

    def on_press(self, event):
        self.press = (event.x, event.y)
        width = self.winfo_width()
        height = self.winfo_height()
        if abs(width - event.x) < 10 and abs(height - event.y) < 10:
            self.resizing = True

    def on_drag(self, event):
        if self.resizing:
            new_width, new_height = event.x, event.y
            if new_width < 0:
                new_width = 0
            if new_height < 0:
                new_height = 0
            self.config(width=new_width, height=new_height)
        self.press = (event.x, event.y)

    def on_release(self, event):
        self.resizing = False

    def on_resize(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        self.coords(self.resize_indicator, width - 10, height - 10, width, height)
