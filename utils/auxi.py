import pyperclip
from utils import globals
import math
import config


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f"{width}x{height}+{position_right}+{position_top}")


def get_half_dimensions(type):
    if type == "rectangle":
        return config.RECTANGLE_WIDTH / 2, config.RECTANGLE_HEIGHT / 2
    elif type == "circle":
        return config.CIRCLE_WIDTH / 2, config.CIRCLE_HEIGHT / 2
    elif type == "triangle":
        return config.TRIANGLE_WIDTH / 2, None
    else:
        raise ValueError(f"Unknown figure type: {type}")


def get_triangle_coords(pos, center_x, center_y, half_width):
    if pos == "1":
        return center_x - half_width, center_y + half_width * math.sqrt(3) / 2
    elif pos == "2":
        return center_x + half_width, center_y + half_width * math.sqrt(3) / 2
    elif pos == "3":
        return center_x, center_y - config.TRIANGLE_WIDTH * math.sqrt(3) / 2
    else:
        raise ValueError(f"Unknown position for triangle: {pos}")


def get_coords_figure(canvas, type, pos):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    center_x, center_y = canvas_width / 2, canvas_height / 2
    half_width, half_height = get_half_dimensions(type)

    if type == "triangle":
        return get_triangle_coords(pos, center_x, center_y, half_width)
    else:
        coords_map = {
            "1": (center_x - half_width, center_y - half_height),
            "2": (center_x + half_width, center_y + half_height)
        }
        return coords_map.get(pos)


def copy_to_clipboard(entry):
    pyperclip.copy(entry.get())


def get_aspect_ratio_message(fraction_str, result):
    if globals.language == "en":
        return f"The aspect ratio is {fraction_str} ({result})"
    elif globals.language == "ca":
        return f"La relació d'aspecte és {fraction_str} ({result})"
    else:
        return f"La relación de aspecto es {fraction_str} ({result})"


def get_aspect_ratio_message2(fraction_str, result, width, height):
    if globals.language == "en":
        return f"The aspect ratio is {fraction_str} ({result:.2f}) - Width: {width:.0f} px, Height: {height:.0f} px"
    elif globals.language == "ca":
        return f"La relació d'aspecte és {fraction_str} ({result:.2f}) - Amplada: {width:.0f} px, Alçada: {height:.0f} px"
    else:
        return f"La relación de aspecto es {fraction_str} ({result:.2f}) - Ancho: {width:.0f} px, Alto: {height:.0f} px"
