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

root = tk.Tk()
root.geometry("800x600")
root.title("Calculadora de Suma")
root.configure(bg='light grey')

# Centrar la ventana en la pantalla
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

logo_image = Image.open("mqp.png")
photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=photo, bg='light grey')
logo_label.pack(anchor="nw")

root.iconbitmap('mqp.ico')

label1 = tk.Label(root, text="Número 1:", bg='light grey')
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Número 2:", bg='light grey')
label2.pack()

entry2 = tk.Entry(root)
entry2.pack()

button = tk.Button(root, text="Calcular", command=calculate)
button.pack()

clear_button = tk.Button(root, text="Limpiar", command=clear)
clear_button.pack()

result_label = tk.Label(root, text="Resultado:", bg='light grey')
result_label.pack()

root.mainloop()
