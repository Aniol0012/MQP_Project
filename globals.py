import config

LANGUAGES = ["Español", "Inglés", "Catalan"]

LANGUAGE_MAP = {
    LANGUAGES[0]: "es",
    LANGUAGES[1]: "en",
    LANGUAGES[2]: "ca",
}

default_language_name = [name for name, code in LANGUAGE_MAP.items() if code == config.DEFAULT_LANGUAGE][0]

# Hacer la ventana espejo con posicion relativa
ENABLE_RELATIVE_POSITION = True

last_touched_figure = None

language = config.DEFAULT_LANGUAGE

aspect_ratio_label = None

mirror_window = None