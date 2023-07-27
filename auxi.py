import globals


def get_division_by_zero_message():
    if globals.language == "en":
        return "You can't divide by 0"
    elif globals.language == "ca":
        return "No pots dividir per 0"
    else:
        return "No puedes dividir por 0"


def get_error_message():
    if globals.language == "en":
        return "Incorrect values have been entered"
    elif globals.language == "ca":
        return "S'han introduït valors incorrectes"
    else:
        return "Se han introducido valores incorrectos"


def get_too_big_message():
    if globals.language == "en":
        return "The introduced values are too big"
    elif globals.language == "ca":
        return "Els valors intrdouïts són massa grans"
    else:
        return "Los valores introducidos son demasiado grandes"


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
