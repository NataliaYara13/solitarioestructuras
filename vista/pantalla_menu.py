"""
Módulo: pantalla_menu.py
Clase PantallaMenu: la pantalla de entrada del juego.

Muestra el título, un abanico decorativo con los 4 ases, las opciones
principales y el mejor puntaje guardado (que se obtiene del Árbol BST
a través de GestorPuntajes.mejor(), es decir, el máximo del árbol).

Atajos de teclado:
    Enter -> Nueva partida
    P     -> Mejores puntajes
    R     -> Reglas
    Esc   -> Salir
"""

import tkinter as tk

from modelo.carta import Carta, AS, PICAS, CORAZONES, DIAMANTES, TREBOLES
from vista import estilos as e
from vista.dibujo import dibujar_carta, BotonCanvas


class PantallaMenu(tk.Frame):
    """
    Pantalla del menú principal.

    Atributos:
        app (VentanaPrincipal): la ventana que cambia entre pantallas.
        lienzo (tk.Canvas): donde se dibuja todo.
        botones (tuple de BotonCanvas): las opciones del menú.
    """

    def __init__(self, padre, app):
        """
        Crea y dibuja el menú.

        Recibe:
            padre (tk.Widget): contenedor (la ventana principal).
            app (VentanaPrincipal): para pedirle que cambie de pantalla.
        Devuelve: nada.
        """
        super().__init__(padre, bg=e.COLOR_MESA)
        self.app = app
        self.lienzo = tk.Canvas(self, width=e.ANCHO_VENTANA, height=e.ALTO_VENTANA,
                                bg=e.COLOR_MESA, highlightthickness=0)
        self.lienzo.pack(fill="both", expand=True)
        self.botones = ()
        self._dibujar()

    def _dibujar(self):
        """
        Dibuja todos los elementos del menú.

        Recibe: nada.
        Devuelve: nada.
        """
        cv = self.lienzo
        centro = e.ANCHO_VENTANA / 2

        # Abanico de ases (cartas reales del modelo, boca arriba)
        for i, palo in enumerate((PICAS, CORAZONES, DIAMANTES, TREBOLES)):
            x = centro - 212 + i * 106
            y = 70 + abs(1.5 - i) * 16
            dibujar_carta(cv, x, y, Carta(AS, palo, boca_arriba=True))

        cv.create_text(centro + 3, 271, text="SOLITARIO", fill=e.COLOR_SOMBRA,
                       font=(e.FUENTE_TITULO, 46, "bold"))
        cv.create_text(centro, 268, text="SOLITARIO", fill=e.COLOR_DORADO,
                       font=(e.FUENTE_TITULO, 46, "bold"))
        cv.create_text(centro, 318, text="Klondike  ·  Proyecto final de Estructuras de Datos",
                       fill=e.COLOR_TEXTO, font=(e.FUENTE_UI, 12))

        opciones = (
            ("▶   Nueva partida", self.app.mostrar_juego, "principal"),
            ("★   Mejores puntajes", self.app.mostrar_puntajes, "normal"),
            ("?   Reglas y controles", self.app.mostrar_reglas, "normal"),
            ("✕   Salir", self.app.salir, "normal"),
        )
        botones = ()
        for i, (texto, comando, estilo) in enumerate(opciones):
            botones += (BotonCanvas(cv, centro - 150, 368 + i * 64, 300, 48, texto,
                                    comando, estilo, tamano=13),)
        self.botones = botones

        cv.create_text(centro, 650, text=self._texto_mejor_puntaje(),
                       fill=e.COLOR_DORADO_CLARO, font=(e.FUENTE_UI, 11, "bold"))
        cv.create_text(centro, e.ALTO_VENTANA - 48,
                       text="Enter: jugar   ·   P: puntajes   ·   R: reglas   ·   Esc: salir",
                       fill=e.COLOR_TEXTO_SUAVE, font=(e.FUENTE_UI, 9))
        cv.create_text(centro, e.ALTO_VENTANA - 24, text=e.PIE_DE_PAGINA,
                       fill=e.COLOR_TEXTO_SUAVE, font=(e.FUENTE_UI, 9))

    def _texto_mejor_puntaje(self):
        """
        Arma el texto del mejor puntaje usando el máximo del Árbol BST.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "Mejor puntaje: Carlos — 950 pts".
        """
        mejor = self.app.gestor.mejor()
        if mejor is None:
            return "Aún no hay puntajes: ¡sé el primero en el ranking!"
        return f"Mejor puntaje: {mejor.nombre} — {mejor.puntos} pts"

    def activar_atajos(self):
        """
        Conecta los atajos de teclado de esta pantalla (la ventana principal
        los llama al mostrarla y los quita al cambiar de pantalla).

        Recibe: nada.
        Devuelve: nada.
        """
        raiz = self.app
        raiz.bind("<Return>", lambda _e: self.app.mostrar_juego())
        raiz.bind("<Escape>", lambda _e: self.app.salir())
        for tecla in ("p", "P"):
            raiz.bind(tecla, lambda _e: self.app.mostrar_puntajes())
        for tecla in ("r", "R"):
            raiz.bind(tecla, lambda _e: self.app.mostrar_reglas())

    def desactivar_atajos(self):
        """
        Quita los atajos de teclado de esta pantalla.

        Recibe: nada.
        Devuelve: nada.
        """
        for tecla in ("<Return>", "<Escape>", "p", "P", "r", "R"):
            self.app.unbind(tecla)
