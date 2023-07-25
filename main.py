import tkinter as tk
from PIL import Image, ImageTk
import fractions

language = "es"


def update_label(label, string):
    label.config(text=string)


def update_language():
    global label1, label2, button, clear_button
    if language == "en":
        update_label(label1, "Enter the horizontal measure (x):")
        update_label(label2, "Enter the vertical measure (y):")
        update_label(button, "Calculate")
        update_label(clear_button, "Clear")
    elif language == "ca":
        update_label(label1, "Introdueix la mesura horitzontal (x):")
        update_label(label2, "Introdueix la mesura vertical (y):")
        update_label(button, "Calcular")
        update_label(clear_button, "Netejar")
    else:
        update_label(label1, "Introduce la medida horizontal (x):")
        update_label(label2, "Introduce la medida vertical (y):")
        update_label(button, "Calcular")
        update_label(clear_button, "Limpiar")


def switch_language(value):
    global language
    if value == "Inglés":
        language = "en"
    elif value == "Catalan":
        language = "ca"
    else:
        language = "es"
    clear()  # Clears all inputs before switching language
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
        update_result_label(get_aspect_ratio_message(fraction_str, result))
    except ValueError:
        update_result_label(get_error_message())
    except ZeroDivisionError:
        update_result_label(get_division_by_zero_message())


def get_aspect_ratio_message(fraction_str, result):
    if language == "en":
        return f"The aspect ratio is {fraction_str} ({result})"
    elif language == "ca":
        return f"La relació d'aspecte és {fraction_str} ({result})"
    else:
        return f"La relación de aspecto es {fraction_str} ({result})"


def get_error_message():
    if language == "en":
        return "Incorrect values have been entered"
    elif language == "ca":
        return "S'han introduït valors incorrectes"
    else:
        return "Se han introducido valores incorrectos"


def get_division_by_zero_message():
    if language == "en":
        return "You can't divide by 0"
    elif language == "ca":
        return "No pots dividir per 0"
    else:
        return "No puedes dividir por 0"


def clear():
    entryX.delete(0, tk.END)
    entryY.delete(0, tk.END)
    rectangle.reset()
    update_result_label("")


def update_result_label(text):
    result_label.config(text=str(text))


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f"{width}x{height}+{position_right}+{position_top}")


root = tk.Tk()
root.title("Calculador de aspect ratio")
root.configure(bg='light grey')

center_window(root, 800, 800)

logo_image = Image.open("icons/mqp.png")
photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=photo, bg='light grey')
logo_label.pack(anchor="center")

root.iconbitmap('icons/mqp.ico')

idiomas = ["Español", "Inglés", "Catalan"]

idioma_seleccionado = tk.StringVar(root)
idioma_seleccionado.set(idiomas[0])

# Menú desplegable
dropdown = tk.OptionMenu(root, idioma_seleccionado, *idiomas, command=switch_language)
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
clear_button.grid(row=0, column=0, padx=10)

button = tk.Button(button_frame, text="Calcular", command=calculate_aspect_ratio, bg='green', height=2, width=10)
button.grid(row=0, column=1)

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
        self.press = (event.x, event.y)
        x1, y1, x2, y2 = self.get_coords()
        if abs(x2 - event.x) < 10 and abs(y2 - event.y) < 10:
            self.resizing = True

    def on_drag(self, event):
        if self.resizing:
            x1, y1, x2, y2 = self.get_coords()
            self.canvas.coords(self.id, x1, y1, event.x, event.y)
        else:
            dx = event.x - self.press[0]
            dy = event.y - self.press[1]
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
        aspect_ratio = width / height if height != 0 else 0
        fraction = fractions.Fraction(int(width), int(height))
        if fraction.denominator == 1:
            fraction_str = f"{fraction.numerator}:1"
        else:
            fraction_str = str(fraction).replace("/", ":")
        aspect_ratio_label.config(text=get_aspect_ratio_message2(fraction_str, aspect_ratio, width, height))

    def reset(self):
        self.canvas.coords(self.id, *self.original_coords)
        self.update_aspect_ratio()

    def get_coords(self):
        return self.canvas.coords(self.id)


def get_aspect_ratio_message2(fraction_str, result, width, height):
    if language == "en":
        return f"The aspect ratio is {fraction_str} ({result:.2f}) - Width: {width:.0f} px, Height: {height:.0f} px"
    elif language == "ca":
        return f"La relació d'aspecte és {fraction_str} ({result:.2f}) - Amplada: {width:.0f} px, Alçada: {height:.0f} px"
    else:
        return f"La relación de aspecto es {fraction_str} ({result:.2f}) - Ancho: {width:.0f} px, Alto: {height:.0f} px"


canvas = tk.Canvas(root, width=700, height=400, bg='light grey')
canvas.pack()

aspect_ratio_label = tk.Label(root, text="")
aspect_ratio_label.pack()

rectangle = ResizableRectangle(canvas, 50, 50, 200, 200, fill='green', width=5)

root.mainloop()
