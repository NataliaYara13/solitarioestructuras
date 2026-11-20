"""
Módulo: pantalla_reglas.py
Clase PantallaReglas: explica las reglas del Klondike y los controles.
"""

import tkinter as tk

from modelo.carta import Carta, CORAZONES, TREBOLES, DIAMANTES
from vista import estilos as e
from vista.dibujo import BotonCanvas, rect_redondeado, dibujar_carta

SECCIONES = (
    ("Objetivo", "Subir las 52 cartas a las 4 fundaciones,\nuna por palo, del As al Rey."),
    ("Columnas", "Las cartas bajan de valor alternando color:\nun 7 negro va sobre un 8 rojo.\n"
                 "En una columna vacía solo entra un Rey."),
    ("Fundaciones", "Mismo palo y en orden: A, 2, 3 … J, Q, K.\nSe sube una carta a la vez."),
    ("Mazo y final", "Clic en el mazo para robar 1 carta; al\nacabarse, vuelve a empezar. "
                     "Si no quedan\nmovimientos útiles, puedes deshacer o terminar."),
)

CONTROLES = (
    ("Clic en una carta", "la selecciona (junto con las de encima)"),
    ("Clic en el destino", "mueve la selección si es válido"),
    ("Doble clic", "sube la carta a su fundación"),
    ("Clic derecho / Esc", "cancela la selección"),
    ("Ctrl+Z  ·  H  ·  Espacio", "deshacer  ·  pista  ·  robar"),
)


class PantallaReglas(tk.Frame):
    """
    Pantalla de reglas y controles.

    Atributos:
        app (VentanaPrincipal).
        lienzo (tk.Canvas).
    """

    def __init__(self, padre, app):
        """
        Crea y dibuja la pantalla.

        Recibe:
            padre (tk.Widget), app (VentanaPrincipal).
        Devuelve: nada.
        """
        super().__init__(padre, bg=e.COLOR_MESA)
        self.app = app
        self.lienzo = tk.Canvas(self, width=e.ANCHO_VENTANA, height=e.ALTO_VENTANA,
                                bg=e.COLOR_MESA, highlightthickness=0)
        self.lienzo.pack(fill="both", expand=True)
        self._dibujar()

    def _dibujar(self):
        """Dibuja las secciones, el ejemplo con cartas y los controles."""
        cv = self.lienzo
        cv.create_text(e.ANCHO_VENTANA / 2, 56, text="?  Reglas y controles",
                       fill=e.COLOR_DORADO, font=(e.FUENTE_TITULO, 28, "bold"))
        for i, (titulo, texto) in enumerate(SECCIONES):
            x, y = 50 + (i % 2) * 395, 100 + (i // 2) * 170
            rect_redondeado(cv, x, y, x + 375, y + 150, 14, fill=e.COLOR_MESA_OSCURO, outline="")
            cv.create_text(x + 20, y + 26, text=titulo, anchor="w", fill=e.COLOR_DORADO_CLARO,
                           font=(e.FUENTE_UI, 13, "bold"))
            cv.create_text(x + 20, y + 50, text=texto, anchor="nw", fill=e.COLOR_TEXTO,
                           font=(e.FUENTE_UI, 11))

        # Ejemplo de escalera válida con cartas reales: 8♥, 7♣, 6♦
        for k, (valor, palo) in enumerate(((8, CORAZONES), (7, TREBOLES), (6, DIAMANTES))):
            dibujar_carta(cv, 620, 430 + k * 30, Carta(valor, palo, boca_arriba=True))
        cv.create_text(738, 520, text="✓", fill="#7ddc9a", font=(e.FUENTE_SIMBOLO, 30, "bold"))
        cv.create_text(665, 630, text="Escalera válida", fill=e.COLOR_TEXTO_SUAVE,
                       font=(e.FUENTE_UI, 10))

        x, y = 50, 450
        cv.create_text(x, y, text="Controles", anchor="w", fill=e.COLOR_DORADO_CLARO,
                       font=(e.FUENTE_UI, 13, "bold"))
        for i, (accion, efecto) in enumerate(CONTROLES):
            yy = y + 34 + i * 32
            cv.create_text(x, yy, text=accion, anchor="w", fill=e.COLOR_TEXTO,
                           font=(e.FUENTE_UI, 11, "bold"))
            cv.create_text(x + 215, yy, text=efecto, anchor="w", fill=e.COLOR_TEXTO_SUAVE,
                           font=(e.FUENTE_UI, 11))
        BotonCanvas(cv, e.ANCHO_VENTANA / 2 - 100, e.ALTO_VENTANA - 72, 200, 46,
                    "←  Volver al menú", self.app.mostrar_menu, "principal", tamano=12)

    def activar_atajos(self):
        """Esc vuelve al menú."""
        self.app.bind("<Escape>", lambda _e: self.app.mostrar_menu())

    def desactivar_atajos(self):
        """Quita los atajos."""
        self.app.unbind("<Escape>")
