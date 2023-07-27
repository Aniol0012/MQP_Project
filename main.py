import tkinter as tk
from PIL import Image, ImageTk
import fractions
import random
import config
import auxi
import globals
import movment
from figures import ResizableRectangle
from figures import ResizableCircle

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
            new_rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 50 + int(entryX.get()), 50 + int(entryY.get()),
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



def add_circle():
    color = random.choice(list(COLORS.values()))
    new_circle = ResizableCircle.ResizableCircle(canvas, 50, 50, 200, 200, fill=color, width=5)
    rectangles.append(new_circle)

    globals.last_touched_figure = new_circle


def add_rectangle():
    color = random.choice(list(COLORS.values()))
    new_rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 200, 200, fill=color, width=5)
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

globals.aspect_ratio_label = tk.Label(root, text="", bg='light gray')
globals.aspect_ratio_label.pack()

if RECTANGLE_WIDTH <= CANVAS_WIDTH and RECTANGLE_HEIGHT <= CANVAS_HEIGHT:
    rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 50 + config.RECTANGLE_WIDTH, 50 + config.RECTANGLE_HEIGHT,
                                   fill=COLORS[selected_color.get()], width=5)
else:
    rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 200, 200, fill=COLORS[selected_color.get()], width=5)

rectangles.append(rectangle)

root.focus_set()

root.bind('w', movment.move_up)
root.bind('s', movment.move_down)
root.bind('a', movment.move_left)
root.bind('d', movment.move_right)

root.mainloop()
