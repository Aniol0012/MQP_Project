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

center_window(root, 800, 600)

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

root.mainloop()
