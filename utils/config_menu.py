import tkinter as tk
import config
from utils import globals, auxi
import pickle


# Aún le queda mucho XD
# TODO: Hacer que el archivo creado se use para cambiar la config
# TODO: Hacer que funcione realmente la configuración
# TODO: Incluir la configuración en un archivo de configuración (que implementa main.py) para que los cambios
#  realizados en la configuración tengan efecto

CONFIG_LABELS = {
    "CANVAS_WIDTH": "Ancho del lienzo",
    "CANVAS_HEIGHT": "Alto del lienzo",
    "ENABLE_ASPECT_RATIO_INPUT": "Habilitar entrada de relación de aspecto",
    "ENABLE_CANVAS_LIMIT": "Prohibir que las figuras se salgan del canvas",
    "BACKGROUND_COLOR": "Color de fondo"
}


def save_config(config_frame, update_function):
    """Guarda las configuraciones modificadas en config.py."""
    for index, (config_key, label_text) in enumerate(CONFIG_LABELS.items()):
        entry_value = config_frame.grid_slaves(row=index, column=1)[0].get()

        if config_key in ["CANVAS_WIDTH", "CANVAS_HEIGHT"]:
            setattr(config, config_key, int(entry_value))
        elif config_key in ["ENABLE_ASPECT_RATIO_INPUT", "ENABLE_CANVAS_LIMIT"]:
            setattr(config, config_key, entry_value.lower() == "true")
        else:
            setattr(config, config_key, entry_value)

    with open("config.pkl", "wb") as f:
        pickle.dump(config.__dict__, f)

    update_function()


def show_config(root, update_configurations):
    if globals.config_window is not None and globals.config_window.winfo_exists():
        globals.config_window.destroy()

    globals.config_window = tk.Toplevel(root)

    window_width = config.CONFIG_WINDOW_WIDTH
    window_height = config.CONFIG_WINDOW_HEIGHT
    globals.config_window.geometry(f"{window_width}x{window_height}")

    globals.config_window.title("Configuración")
    globals.config_window.configure(bg=config.BACKGROUND_COLOR)
    auxi.center_window(globals.config_window, window_width, window_height)

    main_title = tk.Label(globals.config_window, text="Configuración (Modo beta, aun no funciona correctamente)", font=config.LABEL_TITLE_FONT,
                          bg=config.BACKGROUND_COLOR)
    main_title.pack(pady=20)

    config_frame = tk.Frame(globals.config_window, bg=config.BACKGROUND_COLOR)
    config_frame.pack(pady=20)

    config_frame = tk.Frame(globals.config_window, bg=config.BACKGROUND_COLOR, borderwidth=2, relief="groove", padx=20,
                            pady=20)
    config_frame.pack(pady=20)

    for index, (config_key, label_text) in enumerate(CONFIG_LABELS.items()):
        tk.Label(config_frame, text=label_text, bg=config.BACKGROUND_COLOR).grid(row=index, column=0, pady=10, padx=10)

        entry = tk.Entry(config_frame)
        entry.insert(0, getattr(config, config_key))
        entry.grid(row=index, column=1)

    save_button = tk.Button(globals.config_window, text="Guardar",
                            command=lambda: save_config(config_frame, update_configurations),
                            bg="#4CAF50", fg="white",
                            font=config.LABEL_TITLE_FONT)
    save_button.pack(pady=20)
