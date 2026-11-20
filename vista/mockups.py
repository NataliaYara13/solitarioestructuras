"""
Módulo: mockups.py
MOCKUPS (prototipos visuales) de todas las pantallas del Solitario en Tkinter.

Solo DIBUJA cómo se verá cada pantalla: no tiene lógica ni usa el Tablero.
Los datos son de ejemplo. Las funciones de dibujo (cartas, reverso, huecos,
botones) se reutilizarán en la vista real.

Ejecutar desde la carpeta 'Solitario':
    python -m vista.mockups
Use los botones de abajo (o las teclas 1 a 8) para cambiar de pantalla.
"""

import tkinter as tk

# =============================================================================
# Paleta y medidas
# =============================================================================
COLOR_MESA = "#0f5132"
COLOR_MESA_OSCURO = "#0b3d26"
COLOR_BARRA = "#0a2e1d"
COLOR_TEXTO = "#f1f5f2"
COLOR_TEXTO_SUAVE = "#9cc5ac"
COLOR_DORADO = "#d4af37"
COLOR_DORADO_CLARO = "#f0d77a"
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
COLOR_PANEL = "#fbf8ef"
COLOR_TEXTO_PANEL = "#1f2a24"
COLOR_BOTON = "#14532d"

FUENTE_UI = "Segoe UI"
FUENTE_TITULO = "Georgia"
FUENTE_SIMBOLO = "Segoe UI Symbol"

ANCHO_CARTA = 90
ALTO_CARTA = 126
RADIO = 10
SEPARACION = 24
MARGEN = 48
ALTO_BARRA = 56
FILA_SUPERIOR_Y = ALTO_BARRA + 24
FILA_COLUMNAS_Y = FILA_SUPERIOR_Y + ALTO_CARTA + 44
DESPLAZ_TAPADA = 14
DESPLAZ_DESTAPADA = 30

ANCHO = 2 * MARGEN + 7 * ANCHO_CARTA + 6 * SEPARACION      # 870
ALTO = 760

SIMBOLOS = {"P": "♠", "C": "♥", "D": "♦", "T": "♣"}
ROJOS = ("C", "D")
FIGURAS = ("J", "Q", "K")


def x_columna(i):
    """
    Coordenada x de la columna i (0 a 6).

    Recibe:
        i (int).
    Devuelve:
        int.
    """
    return MARGEN + i * (ANCHO_CARTA + SEPARACION)


# =============================================================================
# Primitivas de dibujo (se reutilizarán en la vista real)
# =============================================================================
def rect_redondeado(cv, x1, y1, x2, y2, r, **opciones):
    """
    Dibuja un rectángulo con esquinas redondeadas.

    Recibe:
        cv (tk.Canvas), x1, y1, x2, y2 (números): esquinas.
        r (int): radio de las esquinas.
        **opciones: fill, outline, width, dash...
    Devuelve:
        int: id del polígono.
    """
    puntos = (x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
              x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1)
    return cv.create_polygon(puntos, smooth=True, **opciones)


def dibujar_carta(cv, x, y, valor, palo, seleccionada=False):
    """
    Dibuja una carta boca arriba. Las figuras (J, Q, K) llevan un marco y la
    letra grande al centro.

    Recibe:
        cv (tk.Canvas), x, y (int): esquina superior izquierda.
        valor (str): "A", "2".."10", "J", "Q", "K".
        palo (str): "P", "C", "D" o "T".
        seleccionada (bool): si True, se dibuja con borde dorado.
    Devuelve: nada.
    """
    color = COLOR_ROJO if palo in ROJOS else COLOR_NEGRO
    simbolo = SIMBOLOS[palo]
    rect_redondeado(cv, x + 2, y + 3, x + ANCHO_CARTA + 2, y + ALTO_CARTA + 3, RADIO,
                    fill=COLOR_SOMBRA, outline="")
    rect_redondeado(cv, x, y, x + ANCHO_CARTA, y + ALTO_CARTA, RADIO, fill=COLOR_CARTA,
                    outline=COLOR_DORADO if seleccionada else COLOR_BORDE_CARTA,
                    width=3 if seleccionada else 1)
    cv.create_text(x + 8, y + 5, text=f"{valor}{simbolo}", anchor="nw", fill=color,
                   font=(FUENTE_TITULO, 13, "bold"))
    cv.create_text(x + ANCHO_CARTA - 8, y + ALTO_CARTA - 6, text=valor, anchor="se",
                   fill=color, font=(FUENTE_TITULO, 12, "bold"))
    cx, cy = x + ANCHO_CARTA / 2, y + ALTO_CARTA / 2 + 6
    if valor in FIGURAS:
        cv.create_rectangle(x + 18, y + 30, x + ANCHO_CARTA - 18, y + ALTO_CARTA - 24,
                            outline=color, width=1)
        cv.create_text(cx, cy - 8, text=valor, fill=color, font=(FUENTE_TITULO, 26, "bold"))
        cv.create_text(cx, cy + 20, text=simbolo, fill=color, font=(FUENTE_SIMBOLO, 14))
    else:
        tamano = 40 if valor == "A" else 30
        cv.create_text(cx, cy, text=simbolo, fill=color, font=(FUENTE_SIMBOLO, tamano))


def dibujar_reverso(cv, x, y):
    """
    Dibuja una carta boca abajo (reverso azul con rombos).

    Recibe:
        cv (tk.Canvas), x, y (int).
    Devuelve: nada.
    """
    rect_redondeado(cv, x + 2, y + 3, x + ANCHO_CARTA + 2, y + ALTO_CARTA + 3, RADIO,
                    fill=COLOR_SOMBRA, outline="")
    rect_redondeado(cv, x, y, x + ANCHO_CARTA, y + ALTO_CARTA, RADIO, fill=COLOR_CARTA,
                    outline=COLOR_BORDE_CARTA)
    rect_redondeado(cv, x + 5, y + 5, x + ANCHO_CARTA - 5, y + ALTO_CARTA - 5, RADIO - 3,
                    fill=COLOR_REVERSO, outline="")
    for fila in range(0, ALTO_CARTA - 22, 12):
        desplaz = 6 if (fila // 12) % 2 else 0
        for col in range(0, ANCHO_CARTA - 22, 12):
            cx, cy = x + 13 + col + desplaz, y + 13 + fila
            if cx <= x + ANCHO_CARTA - 12:
                cv.create_polygon(cx, cy - 4, cx + 4, cy, cx, cy + 4, cx - 4, cy,
                                  fill=COLOR_REVERSO_DETALLE, outline="")


def dibujar_hueco(cv, x, y, texto="", resaltado=False):
    """
    Dibuja un lugar vacío (fundación, columna vacía o mazo agotado).

    Recibe:
        cv (tk.Canvas), x, y (int).
        texto (str): símbolo tenue opcional en el centro.
        resaltado (bool): si True, borde dorado (destino válido).
    Devuelve: nada.
    """
    rect_redondeado(cv, x, y, x + ANCHO_CARTA, y + ALTO_CARTA, RADIO, fill=COLOR_HUECO,
                    outline=COLOR_DORADO if resaltado else COLOR_BORDE_HUECO,
                    width=3 if resaltado else 2, dash=() if resaltado else (4, 3))
    if texto:
        cv.create_text(x + ANCHO_CARTA / 2, y + ALTO_CARTA / 2, text=texto,
                       fill=COLOR_BORDE_HUECO, font=(FUENTE_SIMBOLO, 30))


def boton(cv, x, y, ancho, alto, texto, estilo="normal", tamano=11):
    """
    Dibuja un botón redondeado en el canvas.

    Recibe:
        cv (tk.Canvas), x, y (int): esquina superior izquierda.
        ancho, alto (int).
        texto (str).
        estilo (str): "principal" (dorado), "normal" (verde), "claro" (borde)
            o "peligro" (rojo).
        tamano (int): tamaño de la letra.
    Devuelve: nada.
    """
    fondos = {"principal": (COLOR_DORADO, COLOR_NEGRO, ""),
              "normal": (COLOR_BOTON, COLOR_TEXTO, ""),
              "claro": (COLOR_PANEL, COLOR_TEXTO_PANEL, "#b9b2a0"),
              "peligro": ("#9b2c2c", COLOR_TEXTO, "")}
    fondo, letra, borde = fondos[estilo]
    rect_redondeado(cv, x, y, x + ancho, y + alto, min(12, alto // 2), fill=fondo,
                    outline=borde, width=1 if borde else 0)
    cv.create_text(x + ancho / 2, y + alto / 2, text=texto, fill=letra,
                   font=(FUENTE_UI, tamano, "bold"))


def aviso(cv, texto, color, y=ALTO - 44):
    """
    Dibuja un aviso tipo "píldora" centrado (errores, pistas, estado).

    Recibe:
        cv (tk.Canvas), texto (str), color (str): fondo.
        y (int): centro vertical.
    Devuelve: nada.
    """
    ancho = max(360, len(texto) * 8 + 60)
    rect_redondeado(cv, ANCHO / 2 - ancho / 2, y - 19, ANCHO / 2 + ancho / 2, y + 19, 19,
                    fill=color, outline="")
    cv.create_text(ANCHO / 2, y, text=texto, fill=COLOR_TEXTO, font=(FUENTE_UI, 11, "bold"))


def panel_modal(cv, ancho, alto, titulo, icono=""):
    """
    Dibuja un panel claro centrado sobre la mesa (para diálogos).

    Recibe:
        cv (tk.Canvas), ancho, alto (int), titulo (str), icono (str).
    Devuelve:
        (x, y): esquina superior izquierda del panel.
    """
    x, y = (ANCHO - ancho) / 2, (ALTO - alto) / 2 + 10
    for d, color in ((16, "#0c4229"), (11, "#0a3823"), (6, "#072b1b")):
        rect_redondeado(cv, x - d + 8, y - d + 12, x + ancho + d + 8, y + alto + d + 12,
                        18 + d, fill=color, outline="")
    rect_redondeado(cv, x, y, x + ancho, y + alto, 18, fill=COLOR_PANEL, outline=COLOR_DORADO,
                    width=2)
    if icono:
        cv.create_text(ANCHO / 2, y + 42, text=icono, fill=COLOR_DORADO,
                       font=(FUENTE_SIMBOLO, 30))
    cv.create_text(ANCHO / 2, y + (88 if icono else 40), text=titulo, fill=COLOR_TEXTO_PANEL,
                   font=(FUENTE_TITULO, 22, "bold"))
    return x, y


def oscurecer(cv):
    """
    Marca que hay un diálogo abierto: atenúa la barra superior (sus botones
    no se pueden usar mientras el diálogo esté abierto).
    Nota: Tk no tiene transparencia real, por eso no se cubre toda la mesa;
    el diálogo se distingue por su sombra y su borde dorado.

    Recibe:
        cv (tk.Canvas).
    Devuelve: nada.
    """
    cv.create_rectangle(0, 0, ANCHO, ALTO_BARRA, fill=COLOR_BARRA, outline="")
    cv.create_text(ANCHO - 20, ALTO_BARRA / 2, text="Termina el diálogo para seguir",
                   anchor="e", fill=COLOR_TEXTO_SUAVE, font=(FUENTE_UI, 10, "italic"))


# =============================================================================
# Partes de la mesa
# =============================================================================
def barra_superior(cv, tiempo="03:27", movimientos="42", puntos="315", modo="juego"):
    """
    Dibuja la barra superior con estadísticas y botones.

    Recibe:
        cv (tk.Canvas), tiempo, movimientos, puntos (str).
        modo (str): "juego" (botones de partida) o "repeticion".
    Devuelve: nada.
    """
    cv.create_rectangle(0, 0, ANCHO, ALTO_BARRA, fill=COLOR_BARRA, outline="")
    x = 22
    for etiqueta, valor in (("Tiempo", tiempo), ("Movimientos", movimientos),
                            ("Puntos", puntos)):
        cv.create_text(x, 15, text=etiqueta, anchor="w", fill=COLOR_TEXTO_SUAVE,
                       font=(FUENTE_UI, 9))
        cv.create_text(x, 36, text=valor, anchor="w", fill=COLOR_TEXTO,
                       font=(FUENTE_UI, 14, "bold"))
        x += 108
    if modo == "juego":
        botones = (("↶  Deshacer", "principal", 112), ("?  Pista", "normal", 84),
                   ("Rendirse", "normal", 90), ("Menú", "normal", 70))
    else:
        botones = (("✕  Salir de la repetición", "normal", 196),)
        cv.create_text(ANCHO / 2 - 20, ALTO_BARRA / 2, text="REPETICIÓN", fill=COLOR_DORADO,
                       font=(FUENTE_UI, 12, "bold"))
    x = ANCHO - 16
    for texto, estilo, ancho in botones:
        x -= ancho
        boton(cv, x, 11, ancho, 34, texto, estilo, 10)
        x -= 8


def fila_superior(cv, cartas_mazo=18, descarte=("9", "D"), fundaciones=None,
                  descarte_seleccionado=False, fundacion_resaltada=-1):
    """
    Dibuja el mazo, el descarte y las 4 fundaciones.

    Recibe:
        cv (tk.Canvas).
        cartas_mazo (int): cartas por robar (0 = mazo agotado).
        descarte (tuple | None): (valor, palo) de la carta visible.
        fundaciones (tuple): 4 elementos (valor, palo) o (None, palo).
        descarte_seleccionado (bool), fundacion_resaltada (int).
    Devuelve: nada.
    """
    if fundaciones is None:
        fundaciones = (("3", "P"), ("A", "C"), (None, "D"), (None, "T"))
    y = FILA_SUPERIOR_Y
    if cartas_mazo > 0:
        dibujar_reverso(cv, x_columna(0), y)
    else:
        dibujar_hueco(cv, x_columna(0), y, "↻")
    cv.create_text(x_columna(0) + ANCHO_CARTA / 2, y + ALTO_CARTA + 14,
                   text=f"Mazo ({cartas_mazo})", fill=COLOR_TEXTO_SUAVE, font=(FUENTE_UI, 9))
    if descarte:
        dibujar_carta(cv, x_columna(1), y, descarte[0], descarte[1], descarte_seleccionado)
    else:
        dibujar_hueco(cv, x_columna(1), y)
    cv.create_text(x_columna(1) + ANCHO_CARTA / 2, y + ALTO_CARTA + 14, text="Descarte",
                   fill=COLOR_TEXTO_SUAVE, font=(FUENTE_UI, 9))
    for i, (valor, palo) in enumerate(fundaciones):
        x = x_columna(3 + i)
        if valor:
            dibujar_carta(cv, x, y, valor, palo)
        else:
            dibujar_hueco(cv, x, y, SIMBOLOS[palo], resaltado=(i == fundacion_resaltada))
    cv.create_text((x_columna(3) + x_columna(6) + ANCHO_CARTA) / 2, y + ALTO_CARTA + 14,
                   text="Fundaciones (A → K por palo)", fill=COLOR_TEXTO_SUAVE,
                   font=(FUENTE_UI, 9))


COLUMNAS_EJEMPLO = (
    (0, (("K", "P"), ("Q", "C"), ("J", "T"))),
    (1, (("8", "T"),)),
    (0, ()),
    (3, (("10", "C"), ("9", "P"), ("8", "D"), ("7", "T"))),
    (4, (("5", "D"),)),
    (5, (("J", "D"), ("10", "P"))),
    (6, (("Q", "T"), ("J", "C"), ("10", "T"), ("9", "C"))),
)


def columnas(cv, datos=COLUMNAS_EJEMPLO, seleccion=None, destinos=()):
    """
    Dibuja las 7 columnas.

    Recibe:
        cv (tk.Canvas).
        datos: por columna, (cantidad de tapadas, cartas destapadas).
        seleccion (tuple | None): (columna, índice de la primera destapada
            seleccionada); se resalta desde esa carta hasta el final.
        destinos (tuple): columnas que se resaltan como destino válido.
    Devuelve: nada.
    """
    for i, (tapadas, destapadas) in enumerate(datos):
        x, y = x_columna(i), FILA_COLUMNAS_Y
        if tapadas == 0 and not destapadas:
            dibujar_hueco(cv, x, y, "K", resaltado=(i in destinos))
            continue
        for _ in range(tapadas):
            dibujar_reverso(cv, x, y)
            y += DESPLAZ_TAPADA
        for k, (valor, palo) in enumerate(destapadas):
            marcada = seleccion is not None and seleccion[0] == i and k >= seleccion[1]
            dibujar_carta(cv, x, y, valor, palo, seleccionada=marcada)
            y += DESPLAZ_DESTAPADA
        if i in destinos:
            yf = y - DESPLAZ_DESTAPADA
            rect_redondeado(cv, x - 4, yf - 4, x + ANCHO_CARTA + 4, yf + ALTO_CARTA + 4,
                            RADIO + 3, fill="", outline=COLOR_DORADO_CLARO, width=2, dash=(6, 4))


def mesa(cv, **opciones):
    """
    Dibuja la mesa completa (fondo, barra, fila superior y columnas).

    Recibe:
        cv (tk.Canvas).
        **opciones: se reparten a barra_superior, fila_superior y columnas.
    Devuelve: nada.
    """
    cv.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_MESA, outline="")
    barra_superior(cv, **{k: v for k, v in opciones.items()
                          if k in ("tiempo", "movimientos", "puntos", "modo")})
    fila_superior(cv, **{k: v for k, v in opciones.items()
                         if k in ("cartas_mazo", "descarte", "fundaciones",
                                  "descarte_seleccionado", "fundacion_resaltada")})
    columnas(cv, **{k: v for k, v in opciones.items()
                    if k in ("datos", "seleccion", "destinos")})


# =============================================================================
# Las 8 pantallas
# =============================================================================
def pantalla_menu(cv):
    """1. Menú principal."""
    cv.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_MESA, outline="")
    centro = ANCHO / 2
    for i, palo in enumerate(("P", "C", "D", "T")):
        dibujar_carta(cv, centro - 212 + i * 106, 70 + abs(1.5 - i) * 16, "A", palo)
    cv.create_text(centro, 268, text="SOLITARIO", fill=COLOR_DORADO,
                   font=(FUENTE_TITULO, 46, "bold"))
    cv.create_text(centro, 318, text="Klondike  ·  Proyecto final de Estructuras de Datos",
                   fill=COLOR_TEXTO, font=(FUENTE_UI, 12))
    opciones = (("▶   Nueva partida", "principal"), ("★   Mejores puntajes", "normal"),
                ("?   Reglas y controles", "normal"), ("✕   Salir", "normal"))
    for i, (texto, estilo) in enumerate(opciones):
        boton(cv, centro - 150, 368 + i * 64, 300, 48, texto, estilo, 13)
    cv.create_text(centro, 650, text="Mejor puntaje: Carlos — 950 pts",
                   fill=COLOR_DORADO_CLARO, font=(FUENTE_UI, 11, "bold"))
    cv.create_text(centro, ALTO - 26,
                   text="Carlos Andrés Muñoz Ortega  ·  Ingeniería de Software  ·  "
                        "Uniautónoma del Cauca  ·  2026",
                   fill=COLOR_TEXTO_SUAVE, font=(FUENTE_UI, 9))


def pantalla_juego(cv):
    """2. Mesa en juego: grupo seleccionado, destinos resaltados y pista."""
    mesa(cv, seleccion=(1, 0), destinos=(6,))
    aviso(cv, "Seleccionado: 8♣  —  haz clic en una columna resaltada para moverlo",
          COLOR_INFO, y=ALTO - 92)
    aviso(cv, "Pista: pon el 8♣ de la columna 2 sobre el 9♥ de la columna 7  (destapa una carta)",
          "#3d5a1e")


def pantalla_invalido(cv):
    """3. Mesa con aviso de movimiento inválido."""
    mesa(cv, descarte_seleccionado=True)
    aviso(cv, "✕  Movimiento inválido: el 9♦ no va sobre el 8♣ (debe valer uno menos)",
          COLOR_ERROR)


def pantalla_bloqueada(cv):
    """4. Partida bloqueada: sin movimientos útiles."""
    mesa(cv, cartas_mazo=0, descarte=None)
    oscurecer(cv)
    x, y = panel_modal(cv, 470, 300, "No quedan movimientos", "⚠")
    cv.create_text(ANCHO / 2, y + 140,
                   text="Ninguna carta del mazo ni de las columnas\n"
                        "se puede mover a un lugar útil.",
                   fill="#4a5a52", font=(FUENTE_UI, 11), justify="center")
    cv.create_text(ANCHO / 2, y + 190, text="Puedes deshacer para probar otro camino.",
                   fill="#4a5a52", font=(FUENTE_UI, 11, "italic"))
    boton(cv, x + 40, y + 226, 180, 46, "↶  Deshacer", "principal", 12)
    boton(cv, x + 250, y + 226, 180, 46, "Terminar partida", "peligro", 12)


def pantalla_victoria(cv):
    """5. Victoria: resumen y nombre para el ranking."""
    fund = (("K", "P"), ("K", "C"), ("K", "D"), ("K", "T"))
    mesa(cv, cartas_mazo=0, descarte=None, fundaciones=fund,
         datos=tuple((0, ()) for _ in range(7)), tiempo="06:41", movimientos="128",
         puntos="560")
    oscurecer(cv)
    x, y = panel_modal(cv, 500, 470, "¡Ganaste!", "★")
    filas = (("Puntos de la partida", "560"), ("Bono por tiempo (600 − 401 s)", "+199"),
             ("Puntaje final", "759"), ("Tiempo  ·  Movimientos", "06:41  ·  128"))
    for i, (etiqueta, valor) in enumerate(filas):
        yy = y + 132 + i * 30
        negrita = "bold" if i == 2 else "normal"
        cv.create_text(x + 60, yy, text=etiqueta, anchor="w", fill="#4a5a52",
                       font=(FUENTE_UI, 11, negrita))
        cv.create_text(x + 440, yy, text=valor, anchor="e",
                       fill=COLOR_TEXTO_PANEL if i != 2 else "#8a6d10",
                       font=(FUENTE_UI, 12 if i == 2 else 11, "bold"))
    cv.create_line(x + 60, y + 238, x + 440, y + 238, fill="#d9d2bf")
    cv.create_text(ANCHO / 2, y + 262, text="¡Entraste al ranking en el puesto 2!",
                   fill="#8a6d10", font=(FUENTE_UI, 12, "bold"))
    cv.create_text(x + 60, y + 296, text="Tu nombre:", anchor="w", fill="#4a5a52",
                   font=(FUENTE_UI, 10))
    rect_redondeado(cv, x + 60, y + 310, x + 440, y + 350, 8, fill="white", outline="#b9b2a0")
    cv.create_text(x + 74, y + 330, text="Carlos|", anchor="w", fill=COLOR_TEXTO_PANEL,
                   font=(FUENTE_UI, 12))
    boton(cv, x + 40, y + 382, 136, 44, "Guardar", "principal", 11)
    boton(cv, x + 182, y + 382, 136, 44, "▶ Repetición", "claro", 11)
    boton(cv, x + 324, y + 382, 136, 44, "Menú", "claro", 11)


RANKING_EJEMPLO = (
    ("Carlos", 950, "04:58", 102, "2026-11-17", True),
    ("Carlos", 759, "06:41", 128, "2026-11-18", True),
    ("Luis", 700, "07:12", 140, "2026-11-16", True),
    ("Sofía", 610, "08:03", 151, "2026-11-15", True),
    ("Ana", 540, "05:30", 97, "2026-11-15", True),
    ("Mateo", 410, "09:47", 176, "2026-11-14", False),
    ("Valentina", 355, "03:12", 61, "2026-11-14", False),
    ("Andrés", 290, "06:05", 88, "2026-11-13", False),
)


def pantalla_puntajes(cv):
    """6. Mejores puntajes (top 10 desde el Árbol BST)."""
    cv.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_MESA, outline="")
    cv.create_text(ANCHO / 2, 60, text="★  Mejores puntajes", fill=COLOR_DORADO,
                   font=(FUENTE_TITULO, 30, "bold"))
    cv.create_text(ANCHO / 2, 100,
                   text="Top 10 · ordenado con el recorrido inorden inverso del Árbol BST",
                   fill=COLOR_TEXTO_SUAVE, font=(FUENTE_UI, 10))
    x0, x1, y0 = 70, ANCHO - 70, 130
    rect_redondeado(cv, x0, y0, x1, y0 + 500, 16, fill=COLOR_PANEL, outline="")
    columnas_tabla = (("#", x0 + 40, "center"), ("Jugador", x0 + 80, "w"),
                      ("Puntos", x0 + 330, "e"), ("Tiempo", x0 + 420, "e"),
                      ("Mov.", x0 + 495, "e"), ("Fecha", x0 + 600, "e"),
                      ("Resultado", x1 - 30, "e"))
    for titulo, x, ancla in columnas_tabla:
        cv.create_text(x, y0 + 30, text=titulo, anchor=ancla, fill="#7a8780",
                       font=(FUENTE_UI, 10, "bold"))
    cv.create_line(x0 + 20, y0 + 50, x1 - 20, y0 + 50, fill="#d9d2bf")
    medallas = {0: "#d4af37", 1: "#a8a9ad", 2: "#b87333"}
    for i, (nombre, pts, tiempo, mov, fecha, gano) in enumerate(RANKING_EJEMPLO):
        yy = y0 + 78 + i * 48
        if i == 1:
            rect_redondeado(cv, x0 + 14, yy - 20, x1 - 14, yy + 20, 10, fill="#f6ecc4",
                            outline=COLOR_DORADO)
        if i in medallas:
            cv.create_oval(x0 + 27, yy - 13, x0 + 53, yy + 13, fill=medallas[i], outline="")
            cv.create_text(x0 + 40, yy, text=str(i + 1), fill="white",
                           font=(FUENTE_UI, 11, "bold"))
        else:
            cv.create_text(x0 + 40, yy, text=str(i + 1), fill="#4a5a52",
                           font=(FUENTE_UI, 11, "bold"))
        valores = (nombre + ("   ← nuevo" if i == 1 else ""), str(pts), tiempo, str(mov),
                   fecha, "Ganó" if gano else "Perdió")
        for (_, x, ancla), valor in zip(columnas_tabla[1:], valores):
            negrita = "bold" if valor == str(pts) else "normal"
            color = COLOR_TEXTO_PANEL
            if valor in ("Ganó", "Perdió"):
                color = "#2f7a4a" if gano else "#9b2c2c"
            cv.create_text(x, yy, text=valor, anchor=ancla, fill=color,
                           font=(FUENTE_UI, 11, negrita))
    boton(cv, ANCHO / 2 - 210, ALTO - 96, 200, 46, "←  Volver al menú", "principal", 12)
    boton(cv, ANCHO / 2 + 10, ALTO - 96, 200, 46, "Borrar ranking", "normal", 12)


def pantalla_reglas(cv):
    """7. Reglas y controles."""
    cv.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_MESA, outline="")
    cv.create_text(ANCHO / 2, 56, text="?  Reglas y controles", fill=COLOR_DORADO,
                   font=(FUENTE_TITULO, 28, "bold"))
    secciones = (
        ("Objetivo", "Subir las 52 cartas a las 4 fundaciones,\nuna por palo, del As al Rey."),
        ("Columnas", "Las cartas bajan de valor alternando color:\nun 7 negro va sobre un 8 "
                     "rojo.\nEn una columna vacía solo entra un Rey."),
        ("Fundaciones", "Mismo palo y en orden: A, 2, 3 … J, Q, K.\nSe sube una carta a la vez."),
        ("Mazo", "Clic en el mazo para robar 1 carta.\nAl acabarse, vuelve a empezar."),
    )
    for i, (titulo, texto) in enumerate(secciones):
        col, fila = i % 2, i // 2
        x, y = 50 + col * 395, 100 + fila * 170
        rect_redondeado(cv, x, y, x + 375, y + 150, 14, fill=COLOR_MESA_OSCURO, outline="")
        cv.create_text(x + 20, y + 26, text=titulo, anchor="w", fill=COLOR_DORADO_CLARO,
                       font=(FUENTE_UI, 13, "bold"))
        cv.create_text(x + 20, y + 50, text=texto, anchor="nw", fill=COLOR_TEXTO,
                       font=(FUENTE_UI, 11))
    # ejemplo visual de la regla de columnas
    dibujar_carta(cv, 600, 430, "8", "C")
    dibujar_carta(cv, 600, 460, "7", "T")
    dibujar_carta(cv, 600, 490, "6", "D")
    cv.create_text(718, 520, text="✓", fill="#7ddc9a", font=(FUENTE_SIMBOLO, 30, "bold"))
    x, y = 50, 450
    cv.create_text(x, y, text="Controles", anchor="w", fill=COLOR_DORADO_CLARO,
                   font=(FUENTE_UI, 13, "bold"))
    controles = (("Clic en una carta", "la selecciona (y las que tiene encima)"),
                 ("Clic en el destino", "mueve la selección si es válido"),
                 ("Doble clic", "sube la carta a su fundación"),
                 ("Clic derecho / Esc", "cancela la selección"),
                 ("↶ Deshacer  ·  ? Pista", "botones de la barra superior"))
    for i, (accion, efecto) in enumerate(controles):
        yy = y + 34 + i * 32
        cv.create_text(x, yy, text=accion, anchor="w", fill=COLOR_TEXTO,
                       font=(FUENTE_UI, 11, "bold"))
        cv.create_text(x + 200, yy, text=efecto, anchor="w", fill=COLOR_TEXTO_SUAVE,
                       font=(FUENTE_UI, 11))
    boton(cv, ANCHO / 2 - 100, ALTO - 78, 200, 46, "←  Volver al menú", "principal", 12)


def pantalla_repeticion(cv):
    """8. Repetición de la partida (se reproduce la Cola de jugadas)."""
    mesa(cv, modo="repeticion", tiempo="06:41", movimientos="12 / 128", puntos="85",
         seleccion=(1, 0), destinos=(6,))
    y = ALTO - 112
    rect_redondeado(cv, 60, y, ANCHO - 60, y + 92, 16, fill=COLOR_BARRA, outline="")
    cv.create_text(ANCHO / 2, y + 22, text="Jugada 12 de 128:  8♣ de la columna 2 a la "
                                           "columna 7",
                   fill=COLOR_TEXTO, font=(FUENTE_UI, 11, "bold"))
    progreso = 12 / 128
    cv.create_line(100, y + 46, ANCHO - 100, y + 46, fill="#2a4a38", width=6, capstyle="round")
    cv.create_line(100, y + 46, 100 + (ANCHO - 200) * progreso, y + 46, fill=COLOR_DORADO,
                   width=6, capstyle="round")
    controles = (("|◀", 56), ("◀", 56), ("❚❚  Pausa", 110), ("▶", 56), ("▶|", 56))
    total = sum(a for _, a in controles) + 8 * (len(controles) - 1)
    x = ANCHO / 2 - total / 2
    for texto, ancho in controles:
        boton(cv, x, y + 58, ancho, 28, texto, "principal" if "Pausa" in texto else "normal", 10)
        x += ancho + 8
    cv.create_text(ANCHO - 80, y + 72, text="Velocidad: 1x", anchor="e",
                   fill=COLOR_TEXTO_SUAVE, font=(FUENTE_UI, 9))


PANTALLAS = (
    ("1 Menú", pantalla_menu),
    ("2 En juego", pantalla_juego),
    ("3 Inválido", pantalla_invalido),
    ("4 Bloqueada", pantalla_bloqueada),
    ("5 Victoria", pantalla_victoria),
    ("6 Puntajes", pantalla_puntajes),
    ("7 Reglas", pantalla_reglas),
    ("8 Repetición", pantalla_repeticion),
)


class VisorMockups(tk.Tk):
    """
    Ventana para recorrer los mockups con botones o con las teclas 1 a 8.

    Atributos:
        lienzo (tk.Canvas): donde se dibuja la pantalla actual.
    """

    def __init__(self):
        """Crea la ventana y muestra la primera pantalla."""
        super().__init__()
        self.title("Solitario Klondike — Mockups")
        self.configure(bg=COLOR_BARRA)
        self.resizable(False, False)
        self.lienzo = tk.Canvas(self, width=ANCHO, height=ALTO, highlightthickness=0,
                                bg=COLOR_MESA)
        self.lienzo.pack()
        barra = tk.Frame(self, bg=COLOR_BARRA)
        barra.pack(fill="x", pady=4)
        for i, (nombre, _) in enumerate(PANTALLAS):
            tk.Button(barra, text=nombre, command=lambda k=i: self.mostrar(k),
                      bg=COLOR_BOTON, fg=COLOR_TEXTO, relief="flat", padx=8,
                      font=(FUENTE_UI, 9)).pack(side="left", padx=2)
            self.bind(str(i + 1), lambda _e, k=i: self.mostrar(k))
        self.mostrar(0)

    def mostrar(self, indice):
        """
        Dibuja la pantalla indicada.

        Recibe:
            indice (int): de 0 a 7.
        Devuelve: nada.
        """
        self.lienzo.delete("all")
        PANTALLAS[indice][1](self.lienzo)


if __name__ == "__main__":
    VisorMockups().mainloop()
