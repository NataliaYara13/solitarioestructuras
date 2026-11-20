"""
Módulo: mesa.py
Dibuja la mesa del Solitario (mazo, descarte, fundaciones y columnas) a
partir de un Tablero REAL. Lo usan la pantalla de juego y la de repetición.

ETIQUETAS (tags) PARA RECONOCER LOS CLICS
-----------------------------------------
Cada figura dibujada lleva etiquetas del Canvas que dicen qué es:
    "mazo"              -> el mazo de robo
    "descarte"          -> la carta visible del mazo
    "fund_<i>"          -> la fundación i (0 a 3)
    "col_<i>_<pos>"     -> la carta en la posición pos de la columna i
    "colzona_<i>"       -> el área libre de la columna i (para soltar ahí)
Además, todo lo de la mesa lleva la etiqueta "mesa", para borrarlo y
redibujarlo de una vez.

La función 'que_hay_en(cv, x, y)' traduce un clic en uno de esos lugares.

COLUMNAS LARGAS
---------------
Si una columna no cabe en la ventana, se reduce automáticamente cuánto se
ve de cada carta boca arriba (nunca menos de lo necesario para leer su
esquina).
"""

from modelo.reglas import Reglas
from modelo.tablero import NUM_COLUMNAS, NUM_FUNDACIONES
from vista import estilos as e
from vista.dibujo import dibujar_carta, dibujar_reverso, dibujar_hueco, rect_redondeado

FILA_SUPERIOR_Y = e.ALTO_BARRA + 24
FILA_COLUMNAS_Y = FILA_SUPERIOR_Y + e.ALTO_CARTA + 44
LIMITE_INFERIOR = e.ALTO_VENTANA - 70        # deja espacio para los avisos
DESPLAZ_MINIMO = 20


def x_columna(i):
    """
    Coordenada x de la columna i (0 a 6). Las fundaciones usan las
    columnas 3 a 6 y el mazo/descarte las columnas 0 y 1.

    Recibe:
        i (int).
    Devuelve:
        int.
    """
    return e.MARGEN + i * (e.ANCHO_CARTA + e.SEPARACION_COLUMNAS)


def desplazamiento_columna(columna):
    """
    Calcula cuánto se ve de cada carta boca arriba para que la columna
    quepa en la ventana.

    Recibe:
        columna (ListaDoble de Carta).
    Devuelve:
        int con el desplazamiento vertical entre cartas boca arriba.
    Complejidad: O(n).
    """
    tapadas = 0
    destapadas = 0
    for carta in columna.recorrer_adelante():
        if carta.boca_arriba:
            destapadas += 1
        else:
            tapadas += 1
    if destapadas <= 1:
        return e.DESPLAZ_DESTAPADA
    disponible = LIMITE_INFERIOR - FILA_COLUMNAS_Y - e.ALTO_CARTA - tapadas * e.DESPLAZ_TAPADA
    return int(max(DESPLAZ_MINIMO, min(e.DESPLAZ_DESTAPADA, disponible / (destapadas - 1))))


def destinos_validos(tablero, seleccion):
    """
    Calcula a qué columnas y fundaciones se puede llevar la selección,
    preguntándole a Reglas (así se resaltan en dorado).

    Recibe:
        tablero (Tablero).
        seleccion (tuple | None): ("descarte",), ("col", i, pos) o ("fund", i).
    Devuelve:
        (columnas, fundaciones): dos tuplas con los índices válidos.
    Complejidad: O(n).
    """
    if seleccion is None:
        return (), ()
    columnas, fundaciones = (), ()
    tipo = seleccion[0]
    if tipo == "descarte":
        carta = tablero.carta_visible_mazo()
        for i in range(NUM_COLUMNAS):
            if Reglas.puede_ir_a_columna(carta, tablero.columnas[i]):
                columnas += (i,)
        for i in range(NUM_FUNDACIONES):
            if Reglas.puede_ir_a_fundacion(carta, tablero.fundaciones[i]):
                fundaciones += (i,)
    elif tipo == "col":
        origen, pos = seleccion[1], seleccion[2]
        col = tablero.columnas[origen]
        for i in range(NUM_COLUMNAS):
            if Reglas.puede_mover_grupo(col, pos, tablero.columnas[i]):
                columnas += (i,)
        if pos == col.tamano() - 1:
            carta = col.ver_final()
            for i in range(NUM_FUNDACIONES):
                if Reglas.puede_ir_a_fundacion(carta, tablero.fundaciones[i]):
                    fundaciones += (i,)
    elif tipo == "fund":
        carta = tablero.fundaciones[seleccion[1]].ver_tope()
        for i in range(NUM_COLUMNAS):
            if Reglas.puede_ir_a_columna(carta, tablero.columnas[i]):
                columnas += (i,)
    return columnas, fundaciones


def dibujar_mesa(cv, tablero, seleccion=None, mostrar_destinos=True):
    """
    Borra y vuelve a dibujar toda la mesa a partir del estado del Tablero.

    Recibe:
        cv (tk.Canvas).
        tablero (Tablero).
        seleccion (tuple | None): lo que el jugador tiene seleccionado
            (en la repetición: la última jugada, para resaltarla).
        mostrar_destinos (bool): si True, resalta a dónde puede ir la selección.
    Devuelve: nada.
    Complejidad: O(n), n = cartas en la mesa.
    """
    cv.delete("mesa")
    if mostrar_destinos:
        destinos_col, destinos_fund = destinos_validos(tablero, seleccion)
    else:
        destinos_col, destinos_fund = (), ()
    _dibujar_fila_superior(cv, tablero, seleccion, destinos_fund)
    _dibujar_columnas(cv, tablero, seleccion, destinos_col)


def _dibujar_fila_superior(cv, tablero, seleccion, destinos_fund):
    """
    Dibuja mazo, descarte y fundaciones.

    Recibe:
        cv, tablero, seleccion, destinos_fund (tuple de índices).
    Devuelve: nada.
    """
    y = FILA_SUPERIOR_Y
    por_robar = tablero.cartas_por_robar()
    if por_robar > 0:
        dibujar_reverso(cv, x_columna(0), y, tags=("mesa", "mazo"))
    elif tablero.mazo.esta_vacia():
        dibujar_hueco(cv, x_columna(0), y, "", tags=("mesa", "mazo"))
    else:
        dibujar_hueco(cv, x_columna(0), y, "↻", tags=("mesa", "mazo"))
    cv.create_text(x_columna(0) + e.ANCHO_CARTA / 2, y + e.ALTO_CARTA + 14,
                   text=f"Mazo ({por_robar})", fill=e.COLOR_TEXTO_SUAVE,
                   font=(e.FUENTE_UI, 9), tags=("mesa",))

    visible = tablero.carta_visible_mazo()
    if visible is not None:
        dibujar_carta(cv, x_columna(1), y, visible,
                      seleccionada=(seleccion == ("descarte",)), tags=("mesa", "descarte"))
    else:
        dibujar_hueco(cv, x_columna(1), y, tags=("mesa", "descarte"))
    cv.create_text(x_columna(1) + e.ANCHO_CARTA / 2, y + e.ALTO_CARTA + 14, text="Descarte",
                   fill=e.COLOR_TEXTO_SUAVE, font=(e.FUENTE_UI, 9), tags=("mesa",))

    for i in range(NUM_FUNDACIONES):
        x = x_columna(3 + i)
        etiquetas = ("mesa", f"fund_{i}")
        tope = tablero.fundaciones[i].ver_tope()
        if tope is not None:
            dibujar_carta(cv, x, y, tope, seleccionada=(seleccion == ("fund", i)),
                          tags=etiquetas)
            if i in destinos_fund:
                _marco_destino(cv, x, y)
        else:
            dibujar_hueco(cv, x, y, "A", resaltado=(i in destinos_fund), tags=etiquetas)
    cv.create_text((x_columna(3) + x_columna(6) + e.ANCHO_CARTA) / 2, y + e.ALTO_CARTA + 14,
                   text="Fundaciones (del As al Rey, por palo)", fill=e.COLOR_TEXTO_SUAVE,
                   font=(e.FUENTE_UI, 9), tags=("mesa",))


def _dibujar_columnas(cv, tablero, seleccion, destinos_col):
    """
    Dibuja las 7 columnas con sus zonas de clic.

    Recibe:
        cv, tablero, seleccion, destinos_col (tuple de índices).
    Devuelve: nada.
    """
    for i in range(NUM_COLUMNAS):
        x = x_columna(i)
        columna = tablero.columnas[i]
        # Zona invisible de toda la columna: permite soltar debajo de la última carta
        cv.create_rectangle(x, FILA_COLUMNAS_Y, x + e.ANCHO_CARTA, LIMITE_INFERIOR,
                            fill="", outline="", tags=("mesa", f"colzona_{i}"))
        if columna.esta_vacia():
            dibujar_hueco(cv, x, FILA_COLUMNAS_Y, "K", resaltado=(i in destinos_col),
                          tags=("mesa", f"colzona_{i}"))
            continue
        desplaz = desplazamiento_columna(columna)
        y = FILA_COLUMNAS_Y
        pos = 0
        ultima_y = y
        for carta in columna.recorrer_adelante():
            etiquetas = ("mesa", f"col_{i}_{pos}")
            ultima_y = y
            if carta.boca_arriba:
                marcada = (seleccion is not None and seleccion[0] == "col"
                           and seleccion[1] == i and pos >= seleccion[2])
                dibujar_carta(cv, x, y, carta, seleccionada=marcada, tags=etiquetas)
                y += desplaz
            else:
                dibujar_reverso(cv, x, y, tags=etiquetas)
                y += e.DESPLAZ_TAPADA
            pos += 1
        if i in destinos_col:
            _marco_destino(cv, x, ultima_y)


def _marco_destino(cv, x, y):
    """
    Dibuja un marco dorado punteado alrededor de una carta destino válida.

    Recibe:
        cv, x, y: esquina de la carta.
    Devuelve: nada.
    """
    rect_redondeado(cv, x - 4, y - 4, x + e.ANCHO_CARTA + 4, y + e.ALTO_CARTA + 4,
                    e.RADIO_CARTA + 3, fill="", outline=e.COLOR_DORADO_CLARO, width=2,
                    dash=(6, 4), tags=("mesa",))


def que_hay_en(cv, x, y):
    """
    Traduce un punto del Canvas en el lugar de la mesa que está ahí.
    Revisa las figuras de arriba hacia abajo y devuelve la primera que
    tenga una etiqueta de la mesa.

    Recibe:
        cv (tk.Canvas), x, y (int): coordenadas del clic.
    Devuelve:
        tuple | None:
            ("mazo",)  ("descarte",)  ("fund", i)
            ("col", i, pos)   -> una carta de la columna i
            ("colzona", i)    -> espacio libre de la columna i
        o None si no hay nada de la mesa en ese punto.
    """
    figuras = cv.find_overlapping(x, y, x, y)
    for figura in reversed(figuras):            # la última es la de más arriba
        for etiqueta in cv.gettags(figura):
            if etiqueta in ("mazo", "descarte"):
                return (etiqueta,)
            if etiqueta.startswith("fund_"):
                return ("fund", int(etiqueta[5:]))
            if etiqueta.startswith("col_"):
                _, i, pos = etiqueta.split("_")
                return ("col", int(i), int(pos))
    for figura in reversed(figuras):
        for etiqueta in cv.gettags(figura):
            if etiqueta.startswith("colzona_"):
                return ("colzona", int(etiqueta[8:]))
    return None
