import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from figures import ResizableRectangle
from figures import ResizableCircle
from figures import ResizableCanvas
import os
import sys
import fractions
import random
import importlib
import pickle
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

toggle_button = globals.aspect_ratio_label
rectangle = None
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
    root.title(translations["title"])


def update_language():
    update_label(label1, translations["enter_horizontal"])
    update_label(label2, translations["enter_vertical"])
    update_label(calculate_bt, translations["calculate"])
    update_label(insert_rectangle_bt, translations["insert_rectangle"])
    update_label(insert_oval_bt, translations["insert_oval"])
    update_label(clear_button, translations["clear"])
    update_label(add_rectangle_bt, translations["add_rect"])
    update_label(add_circle_bt, translations["add_oval"])
    update_label(remove_figure_bt, translations["del_fig"])
    update_label(buttonRatio, translations["calc_rest_value"])
    if toggle_button is not None:
        update_label(toggle_button, translations["absolute_pos"])
    update_label(save_bt, translations["save_bt"], "green")
    update_label(load_bt, translations["load_bt"], "#24a0ed")
    update_label(delete_bt, translations["delete_bt"], "red")
    update_label(open_folder_bt, translations["open_folder_bt"], "#d1c92c")
    update_label(mirror_bt, translations["create_mirror_window"])
    update_label(copy_buttonX, translations["copy"])
    update_label(copy_buttonY, translations["copy"])
    update_label(load_canvas_img_bt, translations["load_img"])
    update_label(remove_canvas_img_bt, translations["remove_img"])


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
        # update_label(result_label, translations["aspect_ratio_msg"])
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")
    except ZeroDivisionError:
        update_label(result_label, translations["no_divide_zero"], "red")


rectangles = []
ovals = []


def clear():
    entryX.delete(0, tk.END)
    entryY.delete(0, tk.END)
    entryRatio.delete(0, tk.END)
    remove_figures()
    clear_mirror_canvas()
    clear_result_label()


def clear_canvas():
    remove_figures()
    clear_mirror_canvas()


def remove_figures():
    try:
        for rectangleCanvas in rectangles.copy():
            rectangleCanvas.canvas.delete(rectangleCanvas.id)
            rectangles.remove(rectangleCanvas)

        for ovalCanvas in ovals.copy():
            ovalCanvas.canvas.delete(ovalCanvas.id)
            ovals.remove(ovalCanvas)
    except ValueError:
        pass


def clear_mirror_canvas():
    if globals.mirror_window is not None:
        mirror_canvas = globals.mirror_window.winfo_children()[0]
        mirror_canvas.delete("all")
        canvas.delete("all")


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

logo_label = tk.Label(root, image=photo, bg=config.LABELS_BG)
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
            clear_result_label()
        else:
            update_label(result_label, translations["too_big_message"], "red")
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")


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
            clear_result_label()
        else:
            update_label(result_label, translations["too_big_message"], "red")
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")


# Menú desplegable
dropdown = tk.OptionMenu(root, idioma_seleccionado, *LANGUAGES, command=switch_language)
dropdown.pack(anchor='nw', padx=30)

# Entry X
label1 = tk.Label(root, text=translations["enter_horizontal"], bg=config.LABELS_BG,
                  font=config.LABEL_TITLE_FONT)
label1.pack()

entry_frameX = tk.Frame(root, bg=config.CANVAS_BACKGROUND_COLOR)
entry_frameX.pack()

entryX = tk.Entry(entry_frameX, bd=2, width=30)
entryX.pack(side='left', padx=config.PADX)

copy_buttonX = tk.Button(entry_frameX, text=translations["copy"], command=lambda: auxi.copy_to_clipboard(entryX))
copy_buttonX.pack(side='left')

# Entry Y
label2 = tk.Label(root, text=translations["enter_vertical"], bg=config.LABELS_BG, font=config.LABEL_TITLE_FONT)
label2.pack()

entry_frameY = tk.Frame(root, bg=config.CANVAS_BACKGROUND_COLOR)
entry_frameY.pack()

entryY = tk.Entry(entry_frameY, bd=2, width=30)
entryY.pack(side='left', padx=config.PADX)

copy_buttonY = tk.Button(entry_frameY, text=translations["copy"], command=lambda: auxi.copy_to_clipboard(entryY))
copy_buttonY.pack(side='left')

# Frame for buttons
button_frame = tk.Frame(root, bg='light grey')
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

result_label = tk.Label(root, text="", bg=config.LABELS_BG, font=('Helvetica', '14'))
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
                update_label(result_label, translations["intr_X_Y_value"], "red")
        else:
            update_label(result_label, translations["valid_aspect_ratio"], "red")
    except ValueError:
        update_label(result_label, translations["err_msg"], "red")


if config.ENABLE_ASPECT_RATIO_INPUT:
    labelRatio = tk.Label(root, text=translations["intr_aspect_ratio"], bg=config.LABELS_BG,
                          font=config.LABEL_TITLE_FONT)
    labelRatio.pack()

    entry_frameRatio = tk.Frame(root, bg=config.CANVAS_BACKGROUND_COLOR)
    entry_frameRatio.pack()

    entryRatio = tk.Entry(entry_frameRatio, bd=2, width=30)
    entryRatio.pack(side='left', padx=config.PADX)

    copy_buttonRatio = tk.Button(entry_frameRatio, text=translations["copy"],
                                 command=lambda: auxi.copy_to_clipboard(entryRatio))
    copy_buttonRatio.pack(side='left')

    buttonRatio = tk.Button(root, text=translations["calc_rest_value"], command=calculate_remaining_value, bg='#37dea1',
                            height=config.BT_HEIGHT,
                            width=config.BT_WIDTH + 5)
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

    create_toggle()


def create_mirror_rectangle(new_rectangle, color):
    if globals.mirror_window is not None:
        mirror_canvas = globals.mirror_window.winfo_children()[0]
        x = int(entryX.get()) if entryX.get() else config.RECTANGLE_WIDTH
        y = int(entryY.get()) if entryY.get() else config.RECTANGLE_HEIGHT
        mirror_rectangle = ResizableRectangle.ResizableRectangle(mirror_canvas, 50, 50, 50 + x, 50 + y, fill=color,
                                                                 width=5)
        new_rectangle.mirror_figures.append(mirror_rectangle)


def load_canvas_image(canvas, root):
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
    global canvas_image
    if canvas_image is not None:
        canvas.delete(canvas_image)
        canvas_image = None
        clear_result_label()
    else:
        update_label(result_label, translations["err_load_img"], "red")


def toggle_bt():
    if not globals.ENABLE_RELATIVE_POSITION:
        globals.ENABLE_RELATIVE_POSITION = True
    else:
        globals.ENABLE_RELATIVE_POSITION = False


button_var = tk.IntVar()

selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

selected_color = tk.StringVar(root)
selected_color.set(next(iter(COLORS)))

# Marco para los botones y el desplegable
button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(anchor='nw', padx=30, pady=10)

color_dropdown = tk.OptionMenu(button_frame, selected_color, *COLORS.keys(), command=change_color)
color_dropdown.grid(row=0, column=0, padx=config.PADX)

add_rectangle_bt = tk.Button(button_frame, text=translations["add_rect"], command=add_rectangle, bg='#0EA7FF',
                             height=config.BT_HEIGHT,
                             width=config.BT_WIDTH)
add_rectangle_bt.grid(row=0, column=1, padx=config.PADX)

add_circle_bt = tk.Button(button_frame, text=translations["add_oval"], command=add_circle, bg='green',
                          height=config.BT_HEIGHT,
                          width=config.BT_WIDTH)
add_circle_bt.grid(row=0, column=2, padx=config.PADX)

remove_figure_bt = tk.Button(button_frame, text=translations["del_fig"], command=remove_rectangle, bg='#F37D70',
                             height=config.BT_HEIGHT,
                             width=config.BT_WIDTH)
remove_figure_bt.grid(row=0, column=3, padx=config.PADX)

load_canvas_img_bt = tk.Button(button_frame, text=translations["load_img"],
                               command=lambda: load_canvas_image(canvas, root),
                               bg='yellow', height=config.BT_HEIGHT, width=config.BT_WIDTH)
load_canvas_img_bt.grid(row=0, column=4, padx=config.PADX)

remove_canvas_img_bt = tk.Button(button_frame, text=translations["remove_img"], command=delete_canvas_image,
                                 bg='#de6137', height=config.BT_HEIGHT, width=config.BT_WIDTH)
remove_canvas_img_bt.grid(row=0, column=5, padx=config.PADX)


def create_toggle():
    global toggle_button
    toggle_button = tk.Checkbutton(button_frame, text=translations["absolute_pos"], variable=button_var,
                                   command=toggle_bt, onvalue=1, offvalue=0, height=config.BT_HEIGHT,
                                   width=config.BT_WIDTH, bg='purple')
    toggle_button.grid(row=0, column=6, padx=config.PADX)


canvas = ResizableCanvas.ResizableCanvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                         bg=config.CANVAS_BACKGROUND_COLOR)
canvas.pack(anchor='nw', padx=30, pady=10)

mirror_bt = tk.Button(root, text=translations["create_mirror_window"], command=create_mirror_window)
mirror_bt.pack()

globals.aspect_ratio_label = tk.Label(root, text="", bg=config.LABELS_BG)
globals.aspect_ratio_label.pack()

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
root.bind('r', movment.increase)
root.bind('f', movment.decrease)


def get_state():
    state = {
        "rectangles": [(canvas.coords(rect.id), canvas.itemcget(rect.id, "fill")) for rect in rectangles],
        "ovals": [(canvas.coords(oval.id), canvas.itemcget(oval.id, "fill")) for oval in ovals],
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

    for oval in ovals:
        canvas.delete(oval.id)
    ovals.clear()

    for coords, color in state["rectangles"]:
        new_rect = ResizableRectangle.ResizableRectangle(canvas, *coords, fill=color, width=5)
        rectangles.append(new_rect)

    for coords, color in state["ovals"]:
        new_oval = ResizableCircle.ResizableCircle(canvas, *coords, fill=color, width=5)
        ovals.append(new_oval)


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


save_bt = tk.Button(root, text=translations["save_bt"], command=save_state, fg="green")
save_bt.place(relx=0.97, rely=0.1, anchor="ne", width=110)

load_bt = tk.Button(root, text=translations["load_bt"], command=load_state, fg="#24a0ed")
load_bt.place(relx=0.97, rely=0.13, anchor="ne", width=110)

delete_bt = tk.Button(root, text=translations["delete_bt"], command=delete_file, fg="red")
delete_bt.place(relx=0.97, rely=0.16, anchor="ne", width=110)

open_folder_bt = tk.Button(root, text=translations["open_folder_bt"], command=open_folder, fg="orange")
open_folder_bt.place(relx=0.97, rely=0.19, anchor="ne", width=110)

root.mainloop()
