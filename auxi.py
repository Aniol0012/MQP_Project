import globals


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
