import tkinter as tk
from PIL import Image, ImageTk


def calculate():
    num1 = float(entry1.get())
    num2 = float(entry2.get())
    result = num1 + num2
    result_label.config(text=f"Resultado: {result}")


root = tk.Tk()
root.geometry("800x600")
root.title("Calculadora de Suma")

logo_image = Image.open("mqp.png")
photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=photo)
logo_label.pack(anchor="nw")

root.iconbitmap('mqp.ico')  # https://convertio.co/es/png-ico/

label1 = tk.Label(root, text="Número 1:")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Número 2:")
label2.pack()

entry2 = tk.Entry(root)
entry2.pack()

button = tk.Button(root, text="Calcular", command=calculate)
button.pack()

result_label = tk.Label(root, text="Resultado:")
result_label.pack()

root.mainloop()
