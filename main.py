import tkinter as tk
from PIL import Image, ImageTk
import fractions


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
        update_result_label(f"La relación de aspecto es {fraction_str} ({result})")
    except ValueError:
        update_result_label("Se han introducido valores incorrectos")
    except ZeroDivisionError:
        update_result_label("No puedes dividir por 0")


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

label1 = tk.Label(root, text="Introduce la medida en horizontal (x):", bg='light grey',
                  font=('Helvetica', '10', 'bold'))
label1.pack()

entryX = tk.Entry(root, bd=2, width=25)
entryX.pack()

label2 = tk.Label(root, text="Introduce la medida en vertical (y):", bg='light grey', font=('Helvetica', '10', 'bold'))
label2.pack()

entryY = tk.Entry(root, bd=2, width=25)
entryY.pack()

button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text="Limpiar", command=clear, bg='orange', height=2, width=10)
clear_button.grid(row=0, column=0, padx=10)

button = tk.Button(button_frame, text="Calcular", command=calculate_aspect_ratio, bg='green', height=2, width=10)
button.grid(row=0, column=1)

result_label = tk.Label(root, text="", bg='light grey')
result_label.pack()

root.mainloop()
