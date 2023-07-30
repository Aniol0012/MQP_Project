import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
import fractions
import random
import config
import auxi
import globals
import movment
from figures import ResizableRectangle
from figures import ResizableCircle
from figures import ResizableCanvas
import importlib

WINDOW_WIDTH = config.WINDOW_WIDTH
WINDOW_HEIGHT = config.WINDOW_HEIGHT
CANVAS_WIDTH = config.CANVAS_WIDTH
CANVAS_HEIGHT = config.CANVAS_HEIGHT
RECTANGLE_WIDTH = config.RECTANGLE_WIDTH
RECTANGLE_HEIGHT = config.RECTANGLE_HEIGHT
LANGUAGES = globals.LANGUAGES
COLORS = config.COLORS

if config.ENABLE_ASPECT_RATIO_INPUT:
    WINDOW_HEIGHT += 120


# Comprueba si estamos ejecutando el archivo .exe
if getattr(sys, 'frozen', False):
    # Estamos ejecutando el archivo .exe
    application_path = sys._MEIPASS
else:
    # Estamos ejecutando el script .py
    application_path = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta del archivo
logo_image_path = os.path.join(application_path, 'icons/mqp.png')
icon_path = os.path.join(application_path, 'icons/mqp.ico')

def update_label(label, string):
    label.config(text=string)


def load_translations(language):
    global translations
    translations_module = importlib.import_module(f"locales.{language}")
    translations = translations_module.translations


def switch_language(value):
    global translations
    if value == "Inglés":
        globals.language = "en"
    elif value == "Catalan":
        globals.language = "ca"
    else:
        globals.language = "es"
    load_translations(globals.language)
    clear()
    update_language()
    root.title(get_title())


def update_language():
    update_label(label1, translations["enter_horizontal"])
    update_label(label2, translations["enter_vertical"])
    update_label(button, translations["calculate"])
    update_label(insert_rectangle_bt, translations["insert_rectangle"])
    update_label(insert_oval_bt, translations["insert_oval"])
    update_label(clear_button, translations["clear"])
    update_label(add_rectangle_bt, translations["add_rect"])
    update_label(add_circle_bt, translations["add_oval"])
    update_label(remove_figure_bt, translations["del_fig"])
    update_label(buttonRatio, translations["calc_rest_value"])


load_translations(globals.language)


def calculate_aspect_ratio():
    try:
        num1 = float(entryX.get())
        num2 = float(entryY.get())
        result = round(num1 / num2, config.RESULT_DECIMAL_PRECISION)
        fraction = fractions.Fraction(int(num1), int(num2))
        if fraction.denominator == 1:
            fraction_str = f"{fraction.numerator}:1"
        else:
            fraction_str = str(fraction).replace("/", ":")
        update_label(result_label, auxi.get_aspect_ratio_message(fraction_str, result))
    except ValueError:
        update_label(result_label, translations["err_msg"])
    except ZeroDivisionError:
        update_label(result_label, translations["no_divide_zero"])


rectangles = []
ovals = []


def clear():
    try:
        entryX.delete(0, tk.END)
        entryY.delete(0, tk.END)
        entryRatio.delete(0, tk.END)
        rectangle.reset()
        update_label(result_label, "")
        for rectangleCanvas in rectangles:
            rectangleCanvas.canvas.delete(rectangleCanvas.id)
            rectangles.remove(rectangleCanvas)
        clear_mirror_canvas()
        update_label(result_label, "")
    except ValueError:
        pass


def clear_mirror_canvas():
    if globals.mirror_window is not None:
        mirror_canvas = globals.mirror_window.winfo_children()[0]
        mirror_canvas.delete("all")
        canvas.delete("all")


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f"{width}x{height}+{position_right}+{position_top}")


def get_title():
    if globals.language == "es":
        return "Calculadora de relación de aspecto"
    elif globals.language == "en":
        return "Aspect ratio calculator"
    elif globals.language == "ca":
        return "Calculadora de relació d'aspecte"
    else:
        return "Idioma no valido"


root = tk.Tk()
root.title(get_title())
root.configure(bg=config.BACKGROUND_COLOR)

center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

logo_image = Image.open(logo_image_path)
photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=photo, bg='light grey')
logo_label.pack(anchor="center")

root.iconbitmap(icon_path)

idioma_seleccionado = tk.StringVar(root)
idioma_seleccionado.set(globals.default_language_name)


def insert_rectangle():
    color = random.choice(list(COLORS.values()))
    try:
        if int(entryX.get()) < CANVAS_WIDTH and int(entryY.get()) < CANVAS_HEIGHT:
            new_rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 50 + int(entryX.get()),
                                                                  50 + int(entryY.get()),
                                                                  fill=color,
                                                                  width=5)
            rectangles.append(new_rectangle)
            create_mirror_rectangle(new_rectangle, color)

            globals.last_touched_figure = new_rectangle
            update_label(result_label, "")
        else:
            update_label(result_label, translations["too_big_message"])
    except ValueError:
        update_label(result_label, translations["err_msg"])


def insert_oval():
    color = random.choice(list(COLORS.values()))
    try:
        if int(entryX.get()) < CANVAS_WIDTH and int(entryY.get()) < CANVAS_HEIGHT:
            new_circle = ResizableCircle.ResizableCircle(canvas, 50, 50, 50 + int(entryX.get()),
                                                         50 + int(entryY.get()),
                                                         fill=color,
                                                         width=5)
            ovals.append(new_circle)

            globals.last_touched_figure = new_circle
            update_label(result_label, "")
        else:
            update_label(result_label, translations["too_big_message"])
    except ValueError:
        update_label(result_label, translations["err_msg"])


# Menú desplegable
dropdown = tk.OptionMenu(root, idioma_seleccionado, *LANGUAGES, command=switch_language)
dropdown.pack(anchor='nw', padx=30)

label1 = tk.Label(root, text=translations["enter_horizontal"], bg='light grey',
                  font=('Helvetica', '14', 'bold'))
label1.pack()

entryX = tk.Entry(root, bd=2, width=30)
entryX.pack()

label2 = tk.Label(root, text=translations["enter_vertical"], bg='light grey', font=('Helvetica', '14', 'bold'))
label2.pack()

entryY = tk.Entry(root, bd=2, width=30)
entryY.pack()

button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text=translations["clear"], command=clear, bg='orange', height=2, width=15)
clear_button.grid(row=0, column=0)

button = tk.Button(button_frame, text=translations["calculate"], command=calculate_aspect_ratio, bg='green', height=2,
                   width=15)
button.grid(row=0, column=1, padx=10, pady=15)

insert_rectangle_bt = tk.Button(button_frame, text="Insertar Cuadrado", command=insert_rectangle, bg='yellow', height=2,
                                width=15)
insert_rectangle_bt.grid(row=1, column=0, padx=10)

insert_oval_bt = tk.Button(button_frame, text="Insertar Circulo", command=insert_oval, bg='orange', height=2, width=15)
insert_oval_bt.grid(row=1, column=1, padx=10)

result_label = tk.Label(root, text="", bg='light grey', font=('Helvetica', '14'))
result_label.pack()


def calculate_remaining_value():
    try:
        aspect_ratio = entryRatio.get().split(":")
        if aspect_ratio[0].isdigit() and aspect_ratio[1].isdigit():
            aspect_ratio = [int(i) for i in aspect_ratio]
            if entryX.get():
                x = float(entryX.get())
                y = x * aspect_ratio[1] / aspect_ratio[0]
                entryY.delete(0, tk.END)
                entryY.insert(0, str(y))
            elif entryY.get():
                y = float(entryY.get())
                x = y * aspect_ratio[0] / aspect_ratio[1]
                entryX.delete(0, tk.END)
                entryX.insert(0, str(x))
            else:
                update_label(result_label, translations["intr_X_Y_value"])
        else:
            update_label(result_label, translations["valid_aspect_ratio"])
    except ValueError:
        update_label(result_label, translations["err_msg"])


if config.ENABLE_ASPECT_RATIO_INPUT:
    labelRatio = tk.Label(root, text=translations["intr_aspect_ratio"], bg='light grey',
                          font=('Helvetica', '14', 'bold'))
    labelRatio.pack()

    entryRatio = tk.Entry(root, bd=2, width=30)
    entryRatio.pack()

    buttonRatio = tk.Button(root, text=translations["calc_rest_value"], command=calculate_remaining_value, bg='green',
                            height=2,
                            width=20)
    buttonRatio.pack(pady=10)


def add_circle():
    color = random.choice(list(COLORS.values()))
    if config.CIRCLE_WIDTH <= CANVAS_WIDTH and config.CIRCLE_HEIGHT <= CANVAS_HEIGHT:
        new_circle = ResizableCircle.ResizableCircle(canvas, 50, 50, 50 + config.CIRCLE_WIDTH,
                                                     50 + config.CIRCLE_HEIGHT, fill=color, width=5)
    else:
        new_circle = ResizableCircle.ResizableCircle(canvas, 50, 50, 200, 200, fill=color, width=5)
    ovals.append(new_circle)

    globals.last_touched_figure = new_circle


def add_rectangle():
    color = random.choice(list(COLORS.values()))
    if RECTANGLE_WIDTH <= CANVAS_WIDTH and RECTANGLE_HEIGHT <= CANVAS_HEIGHT:
        new_rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 50 + config.RECTANGLE_WIDTH,
                                                              50 + config.RECTANGLE_HEIGHT, fill=color, width=5)
    else:
        new_rectangle = ResizableCircle.ResizableCircle(canvas, 50, 50, 200, 200, fill=color, width=5)
    rectangles.append(new_rectangle)
    create_mirror_rectangle(new_rectangle, color)

    globals.last_touched_figure = new_rectangle


def remove_oval():
    if ovals:
        try:
            if globals.last_touched_figure is not None:
                oval_to_remove = globals.last_touched_figure
            else:
                oval_to_remove = ovals[-1]
            oval_to_remove.canvas.delete(oval_to_remove.id)
            ovals.remove(oval_to_remove)
        except ValueError:
            pass


def remove_rectangle():
    if rectangles:
        try:
            if globals.last_touched_figure is not None:
                rectangle_to_remove = globals.last_touched_figure
            else:
                rectangle_to_remove = rectangles[-1]
            rectangle_to_remove.canvas.delete(rectangle_to_remove.id)
            rectangles.remove(rectangle_to_remove)

            for mirror_rectangle in rectangle_to_remove.mirror_figures:
                mirror_rectangle.canvas.delete(mirror_rectangle.id)
        except ValueError:
            pass
    else:
        remove_oval()


def change_color(value):
    if globals.last_touched_figure is not None:
        globals.last_touched_figure.set_fill_color(COLORS[value])

    if globals.mirror_window is not None:
        for mirror_figure in globals.last_touched_figure.mirror_figures:
            color = canvas.itemcget(rectangle.id, "fill")
            mirror_figure.canvas.itemconfig(mirror_figure.id, fill=color)


def create_mirror_window():
    if globals.mirror_window is not None:
        globals.mirror_window.destroy()

    # Config de la nueva ventana
    globals.mirror_window = tk.Toplevel(root)
    globals.mirror_window.title("")
    globals.mirror_window.state('zoomed')
    globals.mirror_window.geometry(f'+{root.winfo_screenwidth() * config.SCREEN_TO_OPEN_MIRROR}+0')

    mirror_canvas = tk.Canvas(globals.mirror_window, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                              bg='light grey')
    mirror_canvas.pack(anchor='nw')

    for rectangle in rectangles:
        x1, y1, x2, y2 = canvas.coords(rectangle.id)
        color = canvas.itemcget(rectangle.id, "fill")
        mirror_rectangle = ResizableRectangle.ResizableRectangle(mirror_canvas, x1, y1, x2, y2, fill=color, width=5)
        rectangle.mirror_figures.append(mirror_rectangle)

    for oval in ovals:
        x1, y1, x2, y2 = canvas.coords(oval.id)
        color = canvas.itemcget(oval.id, "fill")
        ResizableCircle.ResizableCircle(mirror_canvas, x1, y1, x2, y2, fill=color, width=5)


def create_mirror_rectangle(new_rectangle, color):
    if globals.mirror_window is not None:
        mirror_canvas = globals.mirror_window.winfo_children()[0]
        x = int(entryX.get()) if entryX.get() else config.RECTANGLE_WIDTH
        y = int(entryY.get()) if entryY.get() else config.RECTANGLE_HEIGHT
        mirror_rectangle = ResizableRectangle.ResizableRectangle(mirror_canvas, 50, 50, 50 + x, 50 + y, fill=color,
                                                                 width=5)
        new_rectangle.mirror_figures.append(mirror_rectangle)


selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

# Marco para los botones y el desplegable
button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(anchor='nw', padx=30, pady=10)

color_dropdown = tk.OptionMenu(button_frame, selected_color, *COLORS.keys(), command=change_color)
color_dropdown.grid(row=0, column=0, padx=10)

add_rectangle_bt = tk.Button(button_frame, text=translations["add_rect"], command=add_rectangle, bg='#0EA7FF', height=2,
                             width=15)
add_rectangle_bt.grid(row=0, column=1, padx=10)

add_circle_bt = tk.Button(button_frame, text=translations["add_oval"], command=add_circle, bg='green', height=2,
                          width=15)
add_circle_bt.grid(row=0, column=2, padx=10)

remove_figure_bt = tk.Button(button_frame, text=translations["del_fig"], command=remove_rectangle, bg='#F37D70',
                             height=2,
                             width=15)
remove_figure_bt.grid(row=0, column=3)

canvas = ResizableCanvas.ResizableCanvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                         bg=config.CANVAS_BACKGROUND_COLOR)
canvas.pack(anchor='nw', padx=30, pady=10)

# Crea un botón que crea una ventana espejo cuando se presiona
# TODO Cambiar el idioma a este boton
mirror_button = tk.Button(root, text="Crear ventana espejo", command=create_mirror_window)
mirror_button.pack()

globals.aspect_ratio_label = tk.Label(root, text="", bg='light gray')
globals.aspect_ratio_label.pack()

color = random.choice(list(COLORS.values()))
if RECTANGLE_WIDTH <= CANVAS_WIDTH and RECTANGLE_HEIGHT <= CANVAS_HEIGHT:
    rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 50 + config.RECTANGLE_WIDTH,
                                                      50 + config.RECTANGLE_HEIGHT,
                                                      fill=color, width=5)
else:
    rectangle = ResizableRectangle.ResizableRectangle(canvas, 50, 50, 200, 200, fill=color,
                                                      width=5)

rectangles.append(rectangle)

root.focus_set()


def disable_entries(event):
    entryX.config(state='disabled')
    entryY.config(state='disabled')
    entryRatio.config(state='disabled')


def enable_entries(event):
    entryX.config(state='normal')
    entryY.config(state='normal')
    entryRatio.config(state='normal')


canvas.bind("<Enter>", disable_entries)
canvas.bind("<Leave>", enable_entries)

root.bind('w', movment.move_up)
root.bind('s', movment.move_down)
root.bind('a', movment.move_left)
root.bind('d', movment.move_right)
root.bind('r', movment.enlarge)
root.bind('f', movment.shrink)

root.mainloop()
