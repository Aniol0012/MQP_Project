import tkinter as tk
from PIL import Image, ImageTk


def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        result = num1 + num2
        update_result_label(result)
    except ValueError:
        update_result_label("Se han introducido valores incorrectos")


def clear():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    update_result_label("")


def update_result_label(new_text):
    result_label.config(text=f"Resultado: {new_text}")


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f"{width}x{height}+{position_right}+{position_top}")


root = tk.Tk()
root.title("Calculadora de Suma")
root.configure(bg='light grey')

center_window(root, 800, 600)

logo_image = Image.open("mqp.png")
photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=photo, bg='light grey')
logo_label.pack(anchor="center")

root.iconbitmap('mqp.ico')

label1 = tk.Label(root, text="Número 1:", bg='light grey', font=('Helvetica', '10', 'bold'))
label1.pack()

entry1 = tk.Entry(root, bd=2, width=25)
entry1.pack()

label2 = tk.Label(root, text="Número 2:", bg='light grey', font=('Helvetica', '10', 'bold'))
label2.pack()

entry2 = tk.Entry(root, bd=2, width=25)
entry2.pack()

button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text="Limpiar", command=clear, bg='orange', height=2, width=10)
clear_button.grid(row=0, column=0, padx=10)

button = tk.Button(button_frame, text="Calcular", command=calculate, bg='green', height=2, width=10)
button.grid(row=0, column=1)

result_label = tk.Label(root, text="Resultado:", bg='light grey')
result_label.pack()

root.mainloop()
