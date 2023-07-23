import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("800x600")  # Cambia el tamaño de la ventana a 800x600

# Carga el logo y lo coloca en la esquina superior izquierda
logo_image = Image.open("logo.png")
photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=photo)
logo_label.pack(anchor="nw")

# Cambia el icono de la aplicación
root.iconbitmap('icono.ico')

root.mainloop()
