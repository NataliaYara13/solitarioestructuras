"""
Módulo: estilos.py
Paleta de colores, fuentes y medidas de toda la interfaz.

Tenerlos en un solo lugar permite cambiar el aspecto del juego sin tocar
la lógica de las pantallas (por ejemplo, el color de la mesa o el tamaño
de las cartas).
"""

# ---------------------------------------------------------------------------
# Colores
# ---------------------------------------------------------------------------
COLOR_MESA = "#0f5132"           # verde paño
COLOR_MESA_OSCURO = "#0b3d26"
COLOR_BARRA = "#0a2e1d"
COLOR_TEXTO = "#f1f5f2"
COLOR_TEXTO_SUAVE = "#9cc5ac"
COLOR_DORADO = "#d4af37"
COLOR_DORADO_CLARO = "#f0d77a"
COLOR_DORADO_HOVER = "#e6c65c"
COLOR_CARTA = "#fffdf7"
COLOR_BORDE_CARTA = "#c9c4b5"
COLOR_ROJO = "#c0392b"
COLOR_NEGRO = "#1d1d1d"
COLOR_REVERSO = "#1e3a8a"
COLOR_REVERSO_DETALLE = "#3b5bdb"
COLOR_HUECO = "#16683f"
COLOR_BORDE_HUECO = "#2f8a5c"
COLOR_SOMBRA = "#08321f"
COLOR_ERROR = "#7f1d1d"
COLOR_INFO = "#1e3a5f"
COLOR_PISTA = "#3d5a1e"
COLOR_PANEL = "#fbf8ef"
COLOR_TEXTO_PANEL = "#1f2a24"
COLOR_BOTON = "#14532d"
COLOR_BOTON_HOVER = "#1b6b3a"
COLOR_PELIGRO = "#9b2c2c"
COLOR_PELIGRO_HOVER = "#b53636"

# ---------------------------------------------------------------------------
# Fuentes (en Windows existen todas; en otros sistemas Tk usa una parecida)
# ---------------------------------------------------------------------------
FUENTE_UI = "Segoe UI"
FUENTE_TITULO = "Georgia"
FUENTE_SIMBOLO = "Segoe UI Symbol"

# ---------------------------------------------------------------------------
# Medidas
# ---------------------------------------------------------------------------
ANCHO_CARTA = 90
ALTO_CARTA = 126
RADIO_CARTA = 10
SEPARACION_COLUMNAS = 24
MARGEN = 48
ALTO_BARRA = 56
DESPLAZ_TAPADA = 14              # cuánto se ve de una carta boca abajo
DESPLAZ_DESTAPADA = 30           # cuánto se ve de una carta boca arriba

ANCHO_VENTANA = 2 * MARGEN + 7 * ANCHO_CARTA + 6 * SEPARACION_COLUMNAS   # 870
ALTO_VENTANA = 760

TITULO_VENTANA = "Solitario Klondike"
AUTOR = "Carlos Andrés Muñoz Ortega"
PIE_DE_PAGINA = (f"{AUTOR}  ·  Ingeniería de Software  ·  "
                 "Corporación Universitaria Autónoma del Cauca  ·  2026")
