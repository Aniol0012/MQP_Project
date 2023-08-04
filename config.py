# Archivo de configuración

# Dimensiones de la ventana
WINDOW_WIDTH = 800  # Default: 800
WINDOW_HEIGHT = 1000  # Default: 900

# Dimensiones del canvas
CANVAS_WIDTH = 700  # Default: 700 (Si esta activado MAXIMIZED_WINDOW este parámetro no tendra ningún efecto)
CANVAS_HEIGHT = 450  # Default: 450

# Dimensiones del rectángulo por defecto que deben de ser inferiores a las del canvas
RECTANGLE_WIDTH = 150  # Default: 150
RECTANGLE_HEIGHT = 150  # Default 150

# Dimensiones del círculo por defecto que deben de ser inferiores a las del canvas
CIRCLE_WIDTH = 150  # Default: 150
CIRCLE_HEIGHT = 150  # Default 150

# Abrir la ventana maximizada
MAXIMIZED_WINDOW = True  # Default: True

# Añadir una relacion de aspecto debajo de los cuadrados
ENABLE_ASPECT_RATIO_INPUT = True  # Default: True

# Mostrar un punto rojo en la esquina inferior derecha del canvas para redimensionarlo
SHOW_RED_DOT_CANVAS = True  # Default: True

# Precision de decimales del resultado
RESULT_DECIMAL_PRECISION = 2  # Default: 2

# En que pantalla se debe abrir la pantalla principal
SCREEN_TO_OPEN_ROOT = 1  # 1 Para la segunda pantalla y 0 para la primera

# En que pantalla se debe abrir la pantalla espejo
SCREEN_TO_OPEN_MIRROR = 1  # 1 Para la segunda pantalla y 0 para la primera

# Idioma predefinido ["es", "en", "ca"]
DEFAULT_LANGUAGE = "es"

# Colores
COLORS = {"Verde": "#3bec24", "Azul": "#24a0ed", "Rojo": "red", "Amarillo": "yellow", "Morado": "purple",
          "Gris": "gray"}

# Nombre del archivo para guardar (tiene que terminar en .pkl)
FILE_NAME = "proyectoMQP.pkl"  # Default: "proyectoMQP.pkl"

# Color del fondo de pantalla
BACKGROUND_COLOR = "light grey"  # Default: "light grey"

LABELS_BG = BACKGROUND_COLOR  # Default: "light grey"

# Fuente de los títulos de los labels
LABEL_TITLE_FONT = ('Helvetica', '14', 'bold')

# Color del fondo del Canvas
CANVAS_BACKGROUND_COLOR = "light grey"  # Default: "light grey"

# Botones
# Separación horizontal botones
PADX = 10

# Altura estándar de la mayoría de botones
BT_HEIGHT = 2  # Default: 2

# Anchura estándar de la mayoría de botones
BT_WIDTH = 15  # Default: 15
