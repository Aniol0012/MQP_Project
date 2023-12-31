import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from utils import config_menu, globals, auxi
from figures import ResizableRectangle
from figures import ResizableTriangle
from figures import ResizableCircle
from figures import ResizableCanvas
import os
import sys
import fractions
import random
import importlib
import pickle
import config

WINDOW_WIDTH = config.WINDOW_WIDTH
WINDOW_HEIGHT = config.WINDOW_HEIGHT
CANVAS_WIDTH = config.CANVAS_WIDTH
CANVAS_HEIGHT = config.CANVAS_HEIGHT
RECTANGLE_WIDTH = config.RECTANGLE_WIDTH
RECTANGLE_HEIGHT = config.RECTANGLE_HEIGHT
LANGUAGES = globals.LANGUAGES
COLORS = config.COLORS

toggle_button = globals.aspect_ratio_label
canvas_image = None

if config.ENABLE_ASPECT_RATIO_INPUT:
    WINDOW_HEIGHT += 120

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

logo_image_path = os.path.join(application_path, 'icons/mqp.png')
icon_path = os.path.join(application_path, 'icons/mqp.ico')


def update_label(label, string, color=None):
    if color:
        label.config(text=string, fg=color)
    else:
        label.config(text=string, fg="black")


def clear_result_label():
    result_label.config(text="", fg="black")


def load_translations(language):
    global translations
    translations_module = importlib.import_module(f"locales.{language}")
    translations = translations_module.translations


def switch_language(value):
    if value == "Inglés":
        globals.language = "en"
    elif value == "Catalan":
        globals.language = "ca"
    else:
        globals.language = "es"
    load_translations(globals.language)
    clear()
    update_language()
    root.title(translations["title"])


def update_language():
    update_label(label1, translations["enter_horizontal"])
    update_label(label2, translations["enter_vertical"])
    update_label(calculate_bt, translations["calculate"])
    update_label(insert_rectangle_bt, translations["insert_rectangle"])
    update_label(insert_oval_bt, translations["insert_oval"])
    update_label(clear_button, translations["clear"])
    update_label(add_rectangle_bt, translations["add_rect"])
    update_label(add_triangle_bt, translations["add_tri"])
    update_label(add_circle_bt, translations["add_oval"])
    update_label(remove_figure_bt, translations["del_fig"])
    if config.ENABLE_ASPECT_RATIO_INPUT:
        update_label(button_ratio, translations["calc_rest_value"])
    if toggle_button:
        update_label(toggle_button, translations["absolute_pos"])
    update_label(save_bt, translations["save_bt"], "green")
    update_label(load_bt, translations["load_bt"], "#24a0ed")
    update_label(delete_bt, translations["delete_bt"], "red")
    update_label(open_folder_bt, translations["open_folder_bt"], "#d1c92c")
    update_label(mirror_bt, translations["create_mirror_window"])
    update_label(copy_buttonX, translations["copy"])
    update_label(copy_buttonY, translations["copy"])
    update_label(copy_button_ratio, translations["copy"])
    update_label(load_canvas_img_bt, translations["load_img"])
    update_label(remove_canvas_img_bt, translations["remove_img"])
    update_label(set_canvas_size_bt, translations["set_canvas_size"])


load_translations(globals.language)


def calculate_aspect_ratio():
    """Calculates the aspect ratio from user inputs and displays the result or an error message."""
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
        update_label(result_label, translations["err_msg"], "red")
    except ZeroDivisionError:
        update_label(result_label, translations["no_divide_zero"], "red")


rectangles = []
triangles = []
circles = []


def clear():
    """Clears all input fields, removes drawn figures, and resets the mirror canvas and result label."""
    entryX.delete(0, tk.END)
    entryY.delete(0, tk.END)
    if entry_ratio.winfo_exists():
        entry_ratio.delete(0, tk.END)
    remove_figures()
    clear_mirror_canvas()
    clear_result_label()


def clear_canvas():
    """Removes all figures from the canvas and clears the mirror canvas."""
    remove_figures()
    clear_mirror_canvas()


def get_color():
    """Returns a color for a figure, either randomly chosen or based on user selection."""
    if config.RANDOM_COLOR:
        return random.choice(list(COLORS.values()))
    else:
        return COLORS[selected_color.get()]


def remove_figures():
    """Removes all figures (rectangles, triangles, circles) from the canvas."""
    try:
        for rectangle in rectangles.copy():
            rectangle.canvas.delete(rectangle.id)
            rectangles.remove(rectangle)

        for triangle in triangles.copy():
            triangle.canvas.delete(triangle.id)
            triangles.remove(triangle)

        for circle in circles.copy():
            circle.canvas.delete(circle.id)
            circles.remove(circle)

        globals.last_touched_figure = None
    except ValueError:
        pass


def clear_mirror_canvas():
    """Clears all figures from the mirror canvas."""
    if globals.mirror_window and globals.mirror_window.winfo_exists():
        mirror_canvas = globals.mirror_window.winfo_children()[0]
        mirror_canvas.delete("all")
        canvas.delete("all")


def concatenate_canvas_wh():
    """Returns a string representing the maximum dimensions of the canvas."""
    return " (max: " + str(canvas.winfo_width()) + "x" + str(canvas.winfo_height()) + ")"


def insert_rectangle():
    """Inserts a rectangle onto the canvas based on user-defined dimensions or displays an error."""
    color = get_color()
    try:
        if float(entryX.get()) <= canvas.winfo_width() and float(entryY.get()) <= canvas.winfo_height():
            x1, y1 = auxi.get_coords_figure(canvas, "rectangle", "1")
            new_rectangle = ResizableRectangle.ResizableRectangle(canvas, x1, y1, 50 + float(entryX.get()),
                                                                  50 + float(entryY.get()), fill=color, width=5)
            rectangles.append(new_rectangle)
            create_mirror_figure(new_rectangle, color)

            globals.last_touched_figure = new_rectangle
            clear_result_label()
        else:
            update_label(result_label, translations["too_big_message"] + concatenate_canvas_wh(), "red")
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")


def insert_oval():
    """Inserts an oval onto the canvas based on user-defined dimensions or displays an error."""
    color = get_color()
    try:
        if float(entryX.get()) <= canvas.winfo_width() and float(entryY.get()) <= canvas.winfo_height():
            x1, y1 = auxi.get_coords_figure(canvas, "circle", "1")
            new_circle = ResizableCircle.ResizableCircle(canvas, x1, y1, 50 + float(entryX.get()),
                                                         50 + float(entryY.get()), fill=color, width=5)
            circles.append(new_circle)
            create_mirror_figure(new_circle, color)

            globals.last_touched_figure = new_circle
            clear_result_label()
        else:
            update_label(result_label, translations["too_big_message"] + concatenate_canvas_wh(), "red")
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")


def calculate_remaining_value():
    """Computes the missing value based on the provided aspect ratio and displays an error if invalid."""
    try:
        aspect_ratio = entry_ratio.get().split(":")
        if aspect_ratio[0].isdigit() and aspect_ratio[1].isdigit():
            clear_result_label()
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
                update_label(result_label, translations["intr_X_Y_value"], "red")
        else:
            update_label(result_label, translations["valid_aspect_ratio"], "red")
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")


def add_rectangle():
    """Adds a resizable rectangle in canvas."""
    clear_result_label()
    color = get_color()

    x1, y1 = auxi.get_coords_figure(canvas, "rectangle", "1")
    x2, y2 = auxi.get_coords_figure(canvas, "rectangle", "2")

    new_rectangle = ResizableRectangle.ResizableRectangle(canvas, x1, y1, x2, y2, fill=color, width=5)

    rectangles.append(new_rectangle)
    create_mirror_figure(new_rectangle, color)
    globals.last_touched_figure = new_rectangle


def add_triangle():
    """Adds a resizable triangle on canvas."""
    clear_result_label()
    color = get_color()

    x1, y1 = auxi.get_coords_figure(canvas, "triangle", "1")
    x2, y2 = auxi.get_coords_figure(canvas, "triangle", "2")
    x3, y3 = auxi.get_coords_figure(canvas, "triangle", "3")

    new_triangle = ResizableTriangle.ResizableTriangle(canvas, x1, y1, x2, y2, x3, y3, fill=color, width=5)
    triangles.append(new_triangle)

    create_mirror_figure(new_triangle, color)
    globals.last_touched_figure = new_triangle


def add_circle():
    """Adds a resizable circle in canvas."""
    clear_result_label()
    color = get_color()

    x1, y1 = auxi.get_coords_figure(canvas, "circle", "1")
    x2, y2 = auxi.get_coords_figure(canvas, "circle", "2")

    new_circle = ResizableCircle.ResizableCircle(canvas, x1, y1, x2, y2, fill=color, width=5)

    circles.append(new_circle)
    create_mirror_figure(new_circle, color)
    globals.last_touched_figure = new_circle


def remove_figure():
    """Removes the last touched figure in canvas."""
    clear_result_label()
    try:
        if globals.last_touched_figure:
            figure_to_remove = globals.last_touched_figure
            figure_to_remove.canvas.delete(figure_to_remove.id)

            if isinstance(figure_to_remove, ResizableRectangle.ResizableRectangle):
                rectangles.remove(figure_to_remove)
            elif isinstance(figure_to_remove, ResizableTriangle.ResizableTriangle):
                triangles.remove(figure_to_remove)
            elif isinstance(figure_to_remove, ResizableCircle.ResizableCircle):
                circles.remove(figure_to_remove)
            else:
                print("La figura es de un tipo desconocido.")

            for mirror_figure in figure_to_remove.mirror_figures:
                mirror_figure.canvas.delete(mirror_figure.id)

            globals.last_touched_figure = None
    except ValueError:
        pass


def change_color(value):
    """Changes the color of last touched figure"""
    if globals.last_touched_figure:
        globals.last_touched_figure.set_fill_color(COLORS[value])

    if globals.mirror_window and globals.mirror_window.winfo_exists():
        for mirror_figure in globals.last_touched_figure.mirror_figures:
            color = canvas.itemcget(globals.last_touched_figure.id, "fill")
            mirror_figure.canvas.itemconfig(mirror_figure.id, fill=color)


def create_mirror_window():
    """It creates a mirror canvas in a new window"""
    if globals.mirror_window and globals.mirror_window.winfo_exists():
        globals.mirror_window.destroy()

    globals.mirror_window = tk.Toplevel(root)
    globals.mirror_window.title("")
    globals.mirror_window.state('zoomed')
    globals.mirror_window.geometry(f'+{root.winfo_screenwidth() * config.SCREEN_TO_OPEN_MIRROR}+0')

    mirror_canvas = tk.Canvas(globals.mirror_window, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                              bg=config.CANVAS_BACKGROUND_COLOR)
    mirror_canvas.pack(anchor='nw')

    for rectangle in rectangles:
        coords = canvas.coords(rectangle.id)
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
        elif len(coords) == 6:
            x1, y1, x2, y2, x3, y3 = coords
        else:
            print(f"Error: Número inesperado de coordenadas: {coords}")
            continue
        color = canvas.itemcget(rectangle.id, "fill")
        mirror_rectangle = ResizableRectangle.ResizableRectangle(mirror_canvas, x1, y1, x2, y2, fill=color, width=5)
        rectangle.mirror_figures.append(mirror_rectangle)

    for triangle in triangles:
        x1, y1, x2, y2, x3, y3 = canvas.coords(triangle.id)
        color = canvas.itemcget(triangle.id, "fill")
        mirror_triangle = ResizableTriangle.ResizableTriangle(mirror_canvas, x1, y1, x2, y2, x3, y3, fill=color,
                                                              width=5)
        triangle.mirror_figures.append(mirror_triangle)

    for circle in circles:
        x1, y1, x2, y2 = canvas.coords(circle.id)
        color = canvas.itemcget(circle.id, "fill")
        ResizableCircle.ResizableCircle(mirror_canvas, x1, y1, x2, y2, fill=color, width=5)

    create_toggle()


def create_mirror_figure(new_figure, color):
    """Replica la figura que se acaba de crear en la pantalla espejo en caso de que exista."""
    if globals.mirror_window and globals.mirror_window.winfo_exists():
        mirror_canvas = globals.mirror_window.winfo_children()[0]
        mirror_figure = None
        if isinstance(new_figure, ResizableRectangle.ResizableRectangle):
            x1, y1, x2, y2 = canvas.coords(new_figure.id)
            mirror_figure = ResizableRectangle.ResizableRectangle(mirror_canvas, x1, y1, x2, y2, fill=color, width=5)
        elif isinstance(new_figure, ResizableTriangle.ResizableTriangle):
            x1, y1, x2, y2, x3, y3 = canvas.coords(new_figure.id)
            mirror_figure = ResizableTriangle.ResizableTriangle(mirror_canvas, x1, y1, x2, y2, x3, y3, fill=color,
                                                                width=5)
        elif isinstance(new_figure, ResizableCircle.ResizableCircle):
            x1, y1, x2, y2 = canvas.coords(new_figure.id)
            mirror_figure = ResizableCircle.ResizableCircle(mirror_canvas, x1, y1, x2, y2, fill=color, width=5)
        else:
            print("No se ha podido crear la figura en la pantalla espejo")
        new_figure.mirror_figures.append(mirror_figure)


def load_canvas_image():
    """Loads a background image for canvas."""
    global canvas_image
    filepath = filedialog.askopenfilename(filetypes=[(translations["img"], "*.png;*.jpg;*.jpeg;*.bmp")])

    if filepath:
        clear_canvas()
        bg_image = Image.open(filepath)
        bg_image = bg_image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.BICUBIC)
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        canvas_image = canvas.create_image(0, 0, anchor='nw', image=bg_image_tk)
        root.image = bg_image_tk
        imatge = os.path.basename(filepath)
        update_label(result_label, translations["suc_load_img"] + imatge, "green")


def delete_canvas_image():
    """Deletes the background image in canvas"""
    global canvas_image
    if canvas_image is not None:
        canvas.delete(canvas_image)
        canvas_image = None
        clear_result_label()
    else:
        update_label(result_label, translations["err_load_img"], "red")


def toggle_bt():
    """Switches the configuration of the canvas relative position on figures"""
    if not globals.ENABLE_RELATIVE_POSITION:
        globals.ENABLE_RELATIVE_POSITION = True
    else:
        globals.ENABLE_RELATIVE_POSITION = False
    update_figures()


def update_figures():
    """Updates the figures in canvas on the mirror window."""
    for rectangle in rectangles:
        rectangle.update_mirror_figures()

    for triangle in triangles:
        triangle.update_mirror_figures()

    for circle in circles:
        circle.update_mirror_figures()


# ########################################## UI ###########################################

root = tk.Tk()
root.title(translations["title"])
root.configure(bg=config.BACKGROUND_COLOR)
root.geometry(f'+{root.winfo_screenwidth() * config.SCREEN_TO_OPEN_ROOT}+0')

if config.MAXIMIZED_WINDOW:
    root.state('zoomed')
    CANVAS_WIDTH = root.winfo_screenwidth()
else:
    auxi.center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

logo_image = Image.open(logo_image_path)
photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=photo, bg=config.BACKGROUND_COLOR)
logo_label.pack(anchor="center")

root.iconbitmap(icon_path)

idioma_seleccionado = tk.StringVar(root)
idioma_seleccionado.set(globals.default_language_name)

# Menú desplegable
dropdown = tk.OptionMenu(root, idioma_seleccionado, *LANGUAGES, command=switch_language)
dropdown.pack(anchor='nw', padx=30)

# Entry X
label1 = tk.Label(root, text=translations["enter_horizontal"], bg=config.BACKGROUND_COLOR,
                  font=config.LABEL_TITLE_FONT)
label1.pack()

entry_frameX = tk.Frame(root, bg=config.BACKGROUND_COLOR)
entry_frameX.pack()

entryX = tk.Entry(entry_frameX, bd=2, width=30)
entryX.pack(side='left', padx=config.PADX)

copy_buttonX = tk.Button(entry_frameX, text=translations["copy"], command=lambda: auxi.copy_to_clipboard(entryX))
copy_buttonX.pack(side='left')

# Entry Y
label2 = tk.Label(root, text=translations["enter_vertical"], bg=config.BACKGROUND_COLOR, font=config.LABEL_TITLE_FONT)
label2.pack()

entry_frameY = tk.Frame(root, bg=config.BACKGROUND_COLOR)
entry_frameY.pack()

entryY = tk.Entry(entry_frameY, bd=2, width=30)
entryY.pack(side='left', padx=config.PADX)

copy_buttonY = tk.Button(entry_frameY, text=translations["copy"], command=lambda: auxi.copy_to_clipboard(entryY))
copy_buttonY.pack(side='left')

# Frame for buttons
button_frame = tk.Frame(root, bg=config.BACKGROUND_COLOR)
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text=translations["clear"], command=clear, bg='orange', height=config.BT_HEIGHT,
                         width=config.BT_WIDTH)
clear_button.grid(row=0, column=0, padx=config.PADX, )

calculate_bt = tk.Button(button_frame, text=translations["calculate"], command=calculate_aspect_ratio, bg='#37de59',
                         height=config.BT_HEIGHT,
                         width=config.BT_WIDTH)
calculate_bt.grid(row=0, column=1, padx=config.PADX, pady=15)

insert_rectangle_bt = tk.Button(button_frame, text=translations["insert_rectangle"], command=insert_rectangle,
                                bg='#6f2aa3', fg='white', height=config.BT_HEIGHT,
                                width=config.BT_WIDTH)
insert_rectangle_bt.grid(row=0, column=2, padx=config.PADX)

insert_oval_bt = tk.Button(button_frame, text=translations["insert_oval"], command=insert_oval, bg='#db306c',
                           fg='white', height=config.BT_HEIGHT,
                           width=config.BT_WIDTH)
insert_oval_bt.grid(row=0, column=3, padx=config.PADX)

result_label = tk.Label(root, text="", bg=config.BACKGROUND_COLOR, font=('Helvetica', '14'))
result_label.pack()

if config.ENABLE_ASPECT_RATIO_INPUT:
    labelRatio = tk.Label(root, text=translations["intr_aspect_ratio"], bg=config.BACKGROUND_COLOR,
                          font=config.LABEL_TITLE_FONT)
    labelRatio.pack()

    entry_frameRatio = tk.Frame(root, bg=config.BACKGROUND_COLOR)
    entry_frameRatio.pack()

    entry_ratio = tk.Entry(entry_frameRatio, bd=2, width=30)
    entry_ratio.pack(side='left', padx=config.PADX)

    copy_button_ratio = tk.Button(entry_frameRatio, text=translations["copy"],
                                  command=lambda: auxi.copy_to_clipboard(entry_ratio))
    copy_button_ratio.pack(side='left')

    button_ratio = tk.Button(root, text=translations["calc_rest_value"], command=calculate_remaining_value,
                             bg='#37dea1',
                             height=config.BT_HEIGHT,
                             width=config.BT_WIDTH + 5)
    button_ratio.pack(pady=10)

button_var = tk.IntVar()

selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

# Marco para los botones y el desplegable
button_frame = tk.Frame(root, bg=config.BACKGROUND_COLOR)
button_frame.pack(anchor='nw', padx=30, pady=10)

color_dropdown = tk.OptionMenu(button_frame, selected_color, *COLORS.keys(), command=change_color)
color_dropdown.grid(row=0, column=0, padx=config.PADX)

add_rectangle_bt = tk.Button(button_frame, text=translations["add_rect"], command=add_rectangle, bg='#0EA7FF',
                             height=config.BT_HEIGHT,
                             width=config.BT_WIDTH)
add_rectangle_bt.grid(row=0, column=1, padx=config.PADX)

add_triangle_bt = tk.Button(button_frame, text=translations["add_tri"], command=add_triangle, bg='#39DAEE',
                            height=config.BT_HEIGHT,
                            width=config.BT_WIDTH)

add_triangle_bt.grid(row=0, column=2, padx=config.PADX)

add_circle_bt = tk.Button(button_frame, text=translations["add_oval"], command=add_circle, bg='green',
                          height=config.BT_HEIGHT,
                          width=config.BT_WIDTH)
add_circle_bt.grid(row=0, column=3, padx=config.PADX)

remove_figure_bt = tk.Button(button_frame, text=translations["del_fig"], command=remove_figure, bg='#F37D70',
                             height=config.BT_HEIGHT,
                             width=config.BT_WIDTH)
remove_figure_bt.grid(row=0, column=4, padx=config.PADX)

load_canvas_img_bt = tk.Button(button_frame, text=translations["load_img"],
                               command=load_canvas_image,
                               bg='yellow', height=config.BT_HEIGHT, width=config.BT_WIDTH)
load_canvas_img_bt.grid(row=0, column=5, padx=config.PADX)

remove_canvas_img_bt = tk.Button(button_frame, text=translations["remove_img"], command=delete_canvas_image,
                                 bg='#de6137', height=config.BT_HEIGHT, width=config.BT_WIDTH)
remove_canvas_img_bt.grid(row=0, column=6, padx=config.PADX)


def set_canvas_size():
    global canvas
    try:
        canvas_resolution_w = entryX.get()
        canvas_resolution_h = entryY.get()

        if not canvas_resolution_h or not canvas_resolution_w:
            update_label(result_label, translations["err_canvas_resize"], 'red')
        elif float(canvas_resolution_h) > root.winfo_screenwidth() or float(
                canvas_resolution_h) > root.winfo_screenheight():
            update_label(result_label, translations["err_canvas_resize_window"], 'red')
        else:
            clear_result_label()

            canvas.destroy()
            canvas = ResizableCanvas.ResizableCanvas(canvas_frame, width=canvas_resolution_w,
                                                     height=canvas_resolution_h,
                                                     bg=config.CANVAS_BACKGROUND_COLOR)
            canvas.pack()

    except IndexError:
        update_label(result_label, translations["err_canvas_resize"], 'red')


set_canvas_size_bt = tk.Button(button_frame, text=translations["set_canvas_size"], command=set_canvas_size,
                               bg='purple', height=config.BT_HEIGHT, width=25)
set_canvas_size_bt.grid(row=0, column=7, padx=config.PADX)


def create_toggle():
    global toggle_button
    toggle_button = tk.Checkbutton(button_frame, text=translations["absolute_pos"], variable=button_var,
                                   command=toggle_bt, onvalue=1, offvalue=0, height=config.BT_HEIGHT,
                                   width=config.BT_WIDTH, bg='pink')
    toggle_button.grid(row=0, column=8, padx=config.PADX)


canvas_frame = tk.Frame(root)
canvas_frame.pack(anchor='nw', padx=30, pady=10)

canvas = ResizableCanvas.ResizableCanvas(canvas_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                         bg=config.CANVAS_BACKGROUND_COLOR)
canvas.pack()

mirror_bt = tk.Button(root, text=translations["create_mirror_window"], command=create_mirror_window)
mirror_bt.pack()

globals.aspect_ratio_label = tk.Label(root, text="", bg=config.BACKGROUND_COLOR)
globals.aspect_ratio_label.pack()


def disable_entries(event):
    if config.ENABLE_ASPECT_RATIO_CALCULATOR:
        entryX.config(state='disabled')
        entryY.config(state='disabled')
    if config.ENABLE_ASPECT_RATIO_INPUT:
        entry_ratio.config(state='disabled')


def enable_entries(event):
    if config.ENABLE_ASPECT_RATIO_CALCULATOR:
        entryX.config(state='normal')
        entryY.config(state='normal')
    if config.ENABLE_ASPECT_RATIO_INPUT:
        entry_ratio.config(state='normal')


canvas.bind("<Enter>", disable_entries)
canvas.bind("<Leave>", enable_entries)

root.focus_set()


def get_state():
    state = {
        "rectangles": [(canvas.coords(rect.id), canvas.itemcget(rect.id, "fill")) for rect in rectangles],
        "circles": [(canvas.coords(circle.id), canvas.itemcget(circle.id, "fill")) for circle in circles],
    }
    return state


def save_state():
    update_label(result_label, translations["file_saved"], "green")
    state = get_state()
    with open(config.FILE_NAME, "wb") as f:
        pickle.dump(state, f)


def import_figures(state):
    for rect in rectangles:
        canvas.delete(rect.id)
    rectangles.clear()

    for circle in circles:
        canvas.delete(circle.id)
    circles.clear()

    for coords, color in state["rectangles"]:
        new_rect = ResizableRectangle.ResizableRectangle(canvas, *coords, fill=color, width=5)
        rectangles.append(new_rect)

    for coords, color in state["circles"]:
        new_oval = ResizableCircle.ResizableCircle(canvas, *coords, fill=color, width=5)
        circles.append(new_oval)


def load_state():
    try:
        with open(config.FILE_NAME, "rb") as f:
            state = pickle.load(f)
            import_figures(state)
        update_label(result_label, translations["file_loaded"], "green")
    except FileNotFoundError:
        update_label(result_label, translations["file_not_found"], "red")
    except UnboundLocalError:
        print("Unbound")


def delete_file():
    try:
        os.remove(config.FILE_NAME)
        update_label(result_label, translations["file_removed"], "green")
    except FileNotFoundError:
        update_label(result_label, translations["file_not_found"], "red")


def open_folder():
    clear_result_label()
    try:
        os.startfile(os.getcwd())
    except Exception as e:
        update_label(result_label, translations["err_folder"] + e, "red")


def update_configurations():
    """Actualiza las configuraciones en tiempo real."""
    # Cargar la configuración desde el archivo
    with open("config.pkl", "rb") as f:
        saved_config = pickle.load(f)

    # Actualizar las variables en main.py
    for key, value in saved_config.items():
        setattr(config, key, value)


save_bt = tk.Button(root, text=translations["save_bt"], command=save_state, fg="green")
save_bt.place(relx=0.97, rely=0.1, anchor="ne", width=110)

load_bt = tk.Button(root, text=translations["load_bt"], command=load_state, fg="#24a0ed")
load_bt.place(relx=0.97, rely=0.13, anchor="ne", width=110)

delete_bt = tk.Button(root, text=translations["delete_bt"], command=delete_file, fg="red")
delete_bt.place(relx=0.97, rely=0.16, anchor="ne", width=110)

open_folder_bt = tk.Button(root, text=translations["open_folder_bt"], command=open_folder, fg="orange")
open_folder_bt.place(relx=0.97, rely=0.19, anchor="ne", width=110)

if config.ENABLE_CONFIGURATION_BT:
    config_bt = tk.Button(root, text="Configuración",
                          command=lambda: config_menu.show_config(root, update_configurations),
                          fg="gray")
    config_bt.place(relx=0.97, rely=0.22, anchor="ne", width=110)

if not config.ENABLE_ASPECT_RATIO_CALCULATOR:
    label1.destroy()
    label2.destroy()
    entryX.destroy()
    entryY.destroy()
    copy_buttonX.destroy()
    copy_buttonY.destroy()
    entry_frameY.destroy()
    clear_button.destroy()
    calculate_bt.destroy()
    insert_rectangle_bt.destroy()
    insert_oval_bt.destroy()

root.mainloop()
