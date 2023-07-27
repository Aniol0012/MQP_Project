import tkinter as tk
from PIL import Image, ImageTk
import fractions
import random
import config
import auxi
import globals
import movment

WINDOW_WIDTH = config.WINDOW_WIDTH
WINDOW_HEIGHT = config.WINDOW_HEIGHT
CANVAS_WIDTH = config.CANVAS_WIDTH
CANVAS_HEIGHT = config.CANVAS_HEIGHT
RECTANGLE_WIDTH = config.RECTANGLE_WIDTH
RECTANGLE_HEIGHT = config.RECTANGLE_HEIGHT
LANGUAGES = globals.LANGUAGES
COLORS = config.COLORS


def update_label(label, string):
    label.config(text=string)


def update_language():
    if globals.language == "en":
        update_label(label1, "Enter the horizontal measure (x):")
        update_label(label2, "Enter the vertical measure (y):")
        update_label(button, "Calculate")
        update_label(insert_button, "Insert")
        update_label(clear_button, "Clear")
    elif globals.language == "ca":
        update_label(label1, "Introdueix la mesura horitzontal (x):")
        update_label(label2, "Introdueix la mesura vertical (y):")
        update_label(button, "Calcular")
        update_label(insert_button, "Introduïr")
        update_label(clear_button, "Netejar")
    else:
        update_label(label1, "Introduce la medida horizontal (x):")
        update_label(label2, "Introduce la medida vertical (y):")
        update_label(button, "Calcular")
        update_label(insert_button, "Insertar")
        update_label(clear_button, "Limpiar")


def switch_language(value):
    if value == "Inglés":
        globals.language = "en"
    elif value == "Catalan":
        globals.language = "ca"
    else:
        globals.language = "es"
    clear()
    update_language()


def calculate_aspect_ratio():
    try:
        num1 = float(entryX.get())
        num2 = float(entryY.get())
        result = round(num1 / num2, 4)
        fraction = fractions.Fraction(int(num1), int(num2))
        if fraction.denominator == 1:
            fraction_str = f"{fraction.numerator}:1"
        else:
            fraction_str = str(fraction).replace("/", ":")
        update_label(result_label, auxi.get_aspect_ratio_message(fraction_str, result))
    except ValueError:
        update_label(result_label, auxi.get_error_message())
    except ZeroDivisionError:
        update_label(result_label, auxi.get_division_by_zero_message())


rectangles = []


def clear():
    try:
        entryX.delete(0, tk.END)
        entryY.delete(0, tk.END)
        rectangle.reset()
        update_label(result_label, "")
        for rectangleCanvas in rectangles:
            rectangleCanvas.canvas.delete(rectangleCanvas.id)
            rectangles.remove(rectangleCanvas)
    except ValueError:
        pass


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f"{width}x{height}+{position_right}+{position_top}")


root = tk.Tk()
root.title("Calculador de aspect ratio")
root.configure(bg='light grey')

center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

logo_image = Image.open("icons/mqp.png")
photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=photo, bg='light grey')
logo_label.pack(anchor="center")

root.iconbitmap("icons/mqp.ico")

idioma_seleccionado = tk.StringVar(root)
idioma_seleccionado.set(LANGUAGES[0])

# Menú desplegable
dropdown = tk.OptionMenu(root, idioma_seleccionado, *LANGUAGES, command=switch_language)
dropdown.pack(anchor='nw', padx=30)

label1 = tk.Label(root, text="Introduce la medida en horizontal (x):", bg='light grey',
                  font=('Helvetica', '14', 'bold'))
label1.pack()

entryX = tk.Entry(root, bd=2, width=30)
entryX.pack()

label2 = tk.Label(root, text="Introduce la medida en vertical (y):", bg='light grey', font=('Helvetica', '14', 'bold'))
label2.pack()

entryY = tk.Entry(root, bd=2, width=30)
entryY.pack()

button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text="Limpiar", command=clear, bg='orange', height=2, width=10)
clear_button.grid(row=0, column=0)

button = tk.Button(button_frame, text="Calcular", command=calculate_aspect_ratio, bg='green', height=2, width=10)
button.grid(row=0, column=1, padx=15)


def insert_rectangle():
    color = random.choice(list(COLORS.values()))
    try:
        if int(entryX.get()) < CANVAS_WIDTH and int(entryY.get()) < CANVAS_HEIGHT:
            new_rectangle = ResizableRectangle(canvas, 50, 50, 50 + int(entryX.get()), 50 + int(entryY.get()),
                                               fill=color,
                                               width=5)
            rectangles.append(new_rectangle)

            globals.last_touched_figure = new_rectangle
            update_label(result_label, "")
        else:
            update_label(result_label, auxi.get_too_big_message())
    except ValueError:
        update_label(result_label, auxi.get_error_message())


insert_button = tk.Button(button_frame, text="Insertar", command=insert_rectangle, bg='yellow', height=2, width=10)
insert_button.grid(row=0, column=2)

result_label = tk.Label(root, text="", bg='light grey', font=('Helvetica', '14'))
result_label.pack()


class ResizableRectangle:
    def __init__(self, canvas, x1, y1, x2, y2, **kwargs):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
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
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        if height != 0:
            aspect_ratio = width / height if height != 0 else 0
            fraction = fractions.Fraction(int(width), int(height))
            if fraction.denominator == 1:
                fraction_str = f"{fraction.numerator}:1"
            else:
                fraction_str = str(fraction).replace("/", ":")
            aspect_ratio_label.config(text=auxi.get_aspect_ratio_message2(fraction_str, aspect_ratio, width, height))

    def reset(self):
        self.canvas.coords(self.id, *self.original_coords)
        self.update_aspect_ratio()

    def set_fill_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def get_coords(self):
        return self.canvas.coords(self.id)


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
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        if height != 0:
            aspect_ratio = width / height if height != 0 else 0
            fraction = fractions.Fraction(int(width), int(height))
            if fraction.denominator == 1:
                fraction_str = f"{fraction.numerator}:1"
            else:
                fraction_str = str(fraction).replace("/", ":")
            aspect_ratio_label.config(text=auxi.get_aspect_ratio_message2(fraction_str, aspect_ratio, width, height))

    def reset(self):
        self.canvas.coords(self.id, *self.original_coords)
        self.update_aspect_ratio()

    def set_fill_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def get_coords(self):
        return self.canvas.coords(self.id)


def add_circle():
    color = random.choice(list(COLORS.values()))
    new_circle = ResizableCircle(canvas, 50, 50, 200, 200, fill=color, width=5)
    rectangles.append(new_circle)

    globals.last_touched_figure = new_circle


def add_rectangle():
    color = random.choice(list(COLORS.values()))
    new_rectangle = ResizableRectangle(canvas, 50, 50, 200, 200, fill=color, width=5)
    rectangles.append(new_rectangle)

    globals.last_touched_figure = new_rectangle


def remove_rectangle():
    if rectangles:
        try:
            if globals.last_touched_figure is not None:
                rectangle_to_remove = globals.last_touched_figure
            else:
                rectangle_to_remove = rectangles[-1]
            rectangle_to_remove.canvas.delete(rectangle_to_remove.id)
            rectangles.remove(rectangle_to_remove)
        except ValueError:
            pass


def change_color(value):
    if globals.last_touched_figure is not None:
        globals.last_touched_figure.set_fill_color(COLORS[value])


selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

# Marco para los botones y el desplegable
button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(anchor='nw', padx=30, pady=10)

color_dropdown = tk.OptionMenu(button_frame, selected_color, *COLORS.keys(), command=change_color)
color_dropdown.grid(row=0, column=0, padx=10)

add_rectangle_button = tk.Button(button_frame, text="Añadir rectángulo", command=add_rectangle, bg='#0EA7FF', height=2,
                                 width=15)
add_rectangle_button.grid(row=0, column=1, padx=10)

add_circle_button = tk.Button(button_frame, text="Añadir círculo", command=add_circle, bg='green', height=2, width=15)
add_circle_button.grid(row=0, column=2, padx=10)

remove_rectangle_button = tk.Button(button_frame, text="Eliminar rectángulo", command=remove_rectangle, bg='#F37D70',
                                    height=2,
                                    width=15)
remove_rectangle_button.grid(row=0, column=3)

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='light grey')
canvas.pack(anchor='nw', padx=30)

aspect_ratio_label = tk.Label(root, text="")
aspect_ratio_label.pack()

if RECTANGLE_WIDTH <= CANVAS_WIDTH and RECTANGLE_HEIGHT <= CANVAS_HEIGHT:
    rectangle = ResizableRectangle(canvas, 50, 50, 50 + config.RECTANGLE_WIDTH, 50 + config.RECTANGLE_HEIGHT,
                                   fill=COLORS[selected_color.get()], width=5)
else:
    rectangle = ResizableRectangle(canvas, 50, 50, 200, 200, fill=COLORS[selected_color.get()], width=5)

rectangles.append(rectangle)

root.focus_set()

root.bind('w', movment.move_up)
root.bind('s', movment.move_down)
root.bind('a', movment.move_left)
root.bind('d', movment.move_right)

root.mainloop()
