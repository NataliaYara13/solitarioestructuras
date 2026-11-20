"""
Módulo: dibujo.py
Funciones para dibujar en un tk.Canvas los elementos del juego (cartas,
reverso, espacios vacíos) y la clase BotonCanvas (botón redondeado con
efecto al pasar el mouse).

Todas las pantallas usan estas mismas funciones, así el juego se ve
igual en todas partes.

Las cartas se dibujan con figuras del Canvas (sin imágenes), por eso el
juego no necesita archivos extra.
"""

from vista import estilos as e

FIGURAS = (11, 12, 13)          # Jota, Reina, Rey


def rect_redondeado(cv, x1, y1, x2, y2, r, **opciones):
    """
    Dibuja un rectángulo con esquinas redondeadas.
    Truco: un polígono con smooth=True suaviza las esquinas; se repiten
    los puntos de cada esquina para que los lados queden rectos.

    Recibe:
        cv (tk.Canvas): donde se dibuja.
        x1, y1, x2, y2 (números): esquinas superior izquierda e inferior derecha.
        r (int): radio de las esquinas.
        **opciones: fill, outline, width, dash, tags...
    Devuelve:
        int: id del polígono creado.
    """
    puntos = (x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
              x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1)
    return cv.create_polygon(puntos, smooth=True, **opciones)


def dibujar_carta(cv, x, y, carta, seleccionada=False, tags=()):
    """
    Dibuja una carta boca arriba a partir de un objeto Carta.
    Las figuras (J, Q, K) llevan un marco y la letra grande al centro.

    Recibe:
        cv (tk.Canvas).
        x, y (int): esquina superior izquierda.
        carta (Carta): la carta a dibujar.
        seleccionada (bool): si True, borde dorado grueso.
        tags (tuple): etiquetas del Canvas para reconocer los clics.
    Devuelve: nada.
    """
    color = e.COLOR_ROJO if carta.es_roja() else e.COLOR_NEGRO
    valor = carta.texto_valor()
    simbolo = carta.simbolo()
    rect_redondeado(cv, x + 2, y + 3, x + e.ANCHO_CARTA + 2, y + e.ALTO_CARTA + 3,
                    e.RADIO_CARTA, fill=e.COLOR_SOMBRA, outline="", tags=tags)
    rect_redondeado(cv, x, y, x + e.ANCHO_CARTA, y + e.ALTO_CARTA, e.RADIO_CARTA,
                    fill=e.COLOR_CARTA,
                    outline=e.COLOR_DORADO if seleccionada else e.COLOR_BORDE_CARTA,
                    width=3 if seleccionada else 1, tags=tags)
    cv.create_text(x + 8, y + 5, text=f"{valor}{simbolo}", anchor="nw", fill=color,
                   font=(e.FUENTE_TITULO, 13, "bold"), tags=tags)
    cv.create_text(x + e.ANCHO_CARTA - 8, y + e.ALTO_CARTA - 6, text=valor, anchor="se",
                   fill=color, font=(e.FUENTE_TITULO, 12, "bold"), tags=tags)
    cx, cy = x + e.ANCHO_CARTA / 2, y + e.ALTO_CARTA / 2 + 6
    if carta.valor in FIGURAS:
        cv.create_rectangle(x + 18, y + 30, x + e.ANCHO_CARTA - 18, y + e.ALTO_CARTA - 24,
                            outline=color, width=1, tags=tags)
        cv.create_text(cx, cy - 8, text=valor, fill=color,
                       font=(e.FUENTE_TITULO, 26, "bold"), tags=tags)
        cv.create_text(cx, cy + 20, text=simbolo, fill=color,
                       font=(e.FUENTE_SIMBOLO, 14), tags=tags)
    else:
        tamano = 40 if carta.valor == 1 else 30
        cv.create_text(cx, cy, text=simbolo, fill=color,
                       font=(e.FUENTE_SIMBOLO, tamano), tags=tags)


def dibujar_reverso(cv, x, y, tags=()):
    """
    Dibuja una carta boca abajo (reverso azul con rombos).

    Recibe:
        cv (tk.Canvas), x, y (int), tags (tuple).
    Devuelve: nada.
    """
    rect_redondeado(cv, x + 2, y + 3, x + e.ANCHO_CARTA + 2, y + e.ALTO_CARTA + 3,
                    e.RADIO_CARTA, fill=e.COLOR_SOMBRA, outline="", tags=tags)
    rect_redondeado(cv, x, y, x + e.ANCHO_CARTA, y + e.ALTO_CARTA, e.RADIO_CARTA,
                    fill=e.COLOR_CARTA, outline=e.COLOR_BORDE_CARTA, tags=tags)
    rect_redondeado(cv, x + 5, y + 5, x + e.ANCHO_CARTA - 5, y + e.ALTO_CARTA - 5,
                    e.RADIO_CARTA - 3, fill=e.COLOR_REVERSO, outline="", tags=tags)
    for fila in range(0, e.ALTO_CARTA - 22, 12):
        desplaz = 6 if (fila // 12) % 2 else 0
        for col in range(0, e.ANCHO_CARTA - 22, 12):
            cx, cy = x + 13 + col + desplaz, y + 13 + fila
            if cx <= x + e.ANCHO_CARTA - 12:
                cv.create_polygon(cx, cy - 4, cx + 4, cy, cx, cy + 4, cx - 4, cy,
                                  fill=e.COLOR_REVERSO_DETALLE, outline="", tags=tags)


def dibujar_hueco(cv, x, y, texto="", resaltado=False, tags=()):
    """
    Dibuja un lugar vacío (fundación, columna vacía o mazo agotado).

    Recibe:
        cv (tk.Canvas), x, y (int).
        texto (str): símbolo tenue opcional en el centro.
        resaltado (bool): si True, borde dorado (destino válido).
        tags (tuple).
    Devuelve: nada.
    """
    rect_redondeado(cv, x, y, x + e.ANCHO_CARTA, y + e.ALTO_CARTA, e.RADIO_CARTA,
                    fill=e.COLOR_HUECO,
                    outline=e.COLOR_DORADO if resaltado else e.COLOR_BORDE_HUECO,
                    width=3 if resaltado else 2, dash=() if resaltado else (4, 3), tags=tags)
    if texto:
        cv.create_text(x + e.ANCHO_CARTA / 2, y + e.ALTO_CARTA / 2, text=texto,
                       fill=e.COLOR_BORDE_HUECO, font=(e.FUENTE_SIMBOLO, 30), tags=tags)


# Estilos de botón: (fondo, fondo al pasar el mouse, color de letra, borde)
ESTILOS_BOTON = {
    "principal": (e.COLOR_DORADO, e.COLOR_DORADO_HOVER, e.COLOR_NEGRO, ""),
    "normal": (e.COLOR_BOTON, e.COLOR_BOTON_HOVER, e.COLOR_TEXTO, ""),
    "claro": (e.COLOR_PANEL, "#efe7d2", e.COLOR_TEXTO_PANEL, "#b9b2a0"),
    "peligro": (e.COLOR_PELIGRO, e.COLOR_PELIGRO_HOVER, e.COLOR_TEXTO, ""),
}


class BotonCanvas:
    """
    Botón redondeado dibujado dentro de un Canvas.
    Cambia de color al pasar el mouse, muestra la mano como cursor y
    ejecuta una función al hacer clic.

    ¿Por qué no usar tk.Button? Porque tk.Button no permite esquinas
    redondeadas y en Windows ignora parte de los colores. Dibujarlo en
    el Canvas garantiza que se vea igual en cualquier computador.

    Atributos:
        cv (tk.Canvas): canvas donde vive el botón.
        comando (función | None): lo que se ejecuta al hacer clic.
        estilo (str): clave de ESTILOS_BOTON.
        habilitado (bool): si False, se ve apagado y no responde.
        _etiqueta (str): tag único que agrupa las figuras del botón.
        _fondo (int): id del rectángulo de fondo.
        _texto (int): id del texto.
    """

    _contador = 0

    def __init__(self, cv, x, y, ancho, alto, texto, comando=None, estilo="normal",
                 tamano=11):
        """
        Dibuja el botón y conecta los eventos del mouse.

        Recibe:
            cv (tk.Canvas), x, y (int): esquina superior izquierda.
            ancho, alto (int): tamaño.
            texto (str): texto del botón.
            comando (función | None): función sin parámetros para el clic.
            estilo (str): "principal", "normal", "claro" o "peligro".
            tamano (int): tamaño de la letra.
        Devuelve: nada.
        """
        BotonCanvas._contador += 1
        self.cv = cv
        self.comando = comando
        self.estilo = estilo
        self.habilitado = True
        self._etiqueta = f"boton_{BotonCanvas._contador}"
        fondo, _, letra, borde = ESTILOS_BOTON[estilo]
        # Etiquetas: una única para este botón y "boton" para todos los botones
        # (sirve para subirlos por encima de lo que se redibuje después).
        self._fondo = rect_redondeado(cv, x, y, x + ancho, y + alto, min(12, alto // 2),
                                      fill=fondo, outline=borde, width=1 if borde else 0,
                                      tags=(self._etiqueta, "boton"))
        self._texto = cv.create_text(x + ancho / 2, y + alto / 2, text=texto, fill=letra,
                                     font=(e.FUENTE_UI, tamano, "bold"),
                                     tags=(self._etiqueta, "boton"))
        cv.tag_bind(self._etiqueta, "<Enter>", self._al_entrar)
        cv.tag_bind(self._etiqueta, "<Leave>", self._al_salir)
        cv.tag_bind(self._etiqueta, "<ButtonRelease-1>", self._al_hacer_clic)

    def _al_entrar(self, _evento):
        """Mouse encima: color más claro y cursor de mano."""
        if self.habilitado:
            self.cv.itemconfigure(self._fondo, fill=ESTILOS_BOTON[self.estilo][1])
            self.cv.configure(cursor="hand2")

    def _al_salir(self, _evento):
        """Mouse afuera: color normal y cursor normal."""
        if self.habilitado:
            self.cv.itemconfigure(self._fondo, fill=ESTILOS_BOTON[self.estilo][0])
        self.cv.configure(cursor="")

    def _al_hacer_clic(self, _evento):
        """Ejecuta el comando si el botón está habilitado."""
        if self.habilitado and self.comando is not None:
            self.comando()

    def habilitar(self, valor=True):
        """
        Habilita o deshabilita el botón (deshabilitado se ve apagado).

        Recibe:
            valor (bool).
        Devuelve: nada.
        """
        self.habilitado = valor
        fondo, _, letra, _ = ESTILOS_BOTON[self.estilo]
        self.cv.itemconfigure(self._fondo, fill=fondo if valor else "#3c5a48")
        self.cv.itemconfigure(self._texto, fill=letra if valor else "#7f9a8a")

    def cambiar_texto(self, texto):
        """
        Cambia el texto del botón.

        Recibe:
            texto (str).
        Devuelve: nada.
        """
        self.cv.itemconfigure(self._texto, text=texto)
