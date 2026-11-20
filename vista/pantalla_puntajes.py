"""
Módulo: pantalla_puntajes.py
Clase PantallaPuntajes: muestra el top 10 de mejores puntajes.

Los datos salen del Árbol BST de GestorPuntajes con el recorrido INORDEN
INVERSO (derecho, raíz, izquierdo), que entrega los puntajes de mayor a
menor sin tener que ordenarlos.

Si el jugador acaba de guardar un puntaje, esa fila aparece resaltada.
"""

import tkinter as tk

from vista import estilos as e
from vista.dibujo import BotonCanvas, rect_redondeado
from vista.dialogos import confirmar

MEDALLAS = ("#d4af37", "#a8a9ad", "#b87333")      # oro, plata, bronce


class PantallaPuntajes(tk.Frame):
    """
    Pantalla del ranking.

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
        """
        Dibuja el título, la tabla del ranking y los botones.

        Recibe: nada.
        Devuelve: nada.
        """
        cv = self.lienzo
        cv.delete("all")
        cv.create_text(e.ANCHO_VENTANA / 2, 60, text="★  Mejores puntajes", fill=e.COLOR_DORADO,
                       font=(e.FUENTE_TITULO, 30, "bold"))
        cv.create_text(e.ANCHO_VENTANA / 2, 100,
                       text="Top 10 · ordenado con el recorrido inorden inverso del Árbol BST",
                       fill=e.COLOR_TEXTO_SUAVE, font=(e.FUENTE_UI, 10))
        x0, x1, y0 = 70, e.ANCHO_VENTANA - 70, 130
        rect_redondeado(cv, x0, y0, x1, y0 + 540, 16, fill=e.COLOR_PANEL, outline="")

        columnas = (("#", x0 + 40, "center"), ("Jugador", x0 + 80, "w"),
                    ("Puntos", x0 + 330, "e"), ("Tiempo", x0 + 420, "e"),
                    ("Mov.", x0 + 495, "e"), ("Fecha", x0 + 620, "e"),
                    ("Resultado", x1 - 30, "e"))
        for titulo, x, ancla in columnas:
            cv.create_text(x, y0 + 30, text=titulo, anchor=ancla, fill="#7a8780",
                           font=(e.FUENTE_UI, 10, "bold"))
        cv.create_line(x0 + 20, y0 + 50, x1 - 20, y0 + 50, fill="#d9d2bf")

        puesto = 0
        for puntaje in self.app.gestor.ranking():
            y = y0 + 76 + puesto * 46
            self._dibujar_fila(puesto, puntaje, y, x0, x1, columnas)
            puesto += 1
        if puesto == 0:
            cv.create_text(e.ANCHO_VENTANA / 2, y0 + 250,
                           text="Todavía no hay puntajes.\n¡Juega una partida y entra al ranking!",
                           fill="#7a8780", font=(e.FUENTE_UI, 13), justify="center")

        BotonCanvas(cv, e.ANCHO_VENTANA / 2 - 210, e.ALTO_VENTANA - 76, 200, 46,
                    "←  Volver al menú", self.app.mostrar_menu, "principal", tamano=12)
        borrar = BotonCanvas(cv, e.ANCHO_VENTANA / 2 + 10, e.ALTO_VENTANA - 76, 200, 46,
                             "Borrar ranking", self._borrar, "normal", tamano=12)
        borrar.habilitar(puesto > 0)

    def _dibujar_fila(self, puesto, puntaje, y, x0, x1, columnas):
        """
        Dibuja una fila del ranking.

        Recibe:
            puesto (int): 0 para el primero.
            puntaje (Puntaje), y (int): centro vertical de la fila.
            x0, x1 (int): bordes del panel. columnas: posiciones de cada dato.
        Devuelve: nada.
        """
        cv = self.lienzo
        if puntaje is self.app.ultimo_puntaje:
            rect_redondeado(cv, x0 + 14, y - 20, x1 - 14, y + 20, 10, fill="#f6ecc4",
                            outline=e.COLOR_DORADO)
        if puesto < len(MEDALLAS):
            cv.create_oval(x0 + 27, y - 13, x0 + 53, y + 13, fill=MEDALLAS[puesto], outline="")
            cv.create_text(x0 + 40, y, text=str(puesto + 1), fill="white",
                           font=(e.FUENTE_UI, 11, "bold"))
        else:
            cv.create_text(x0 + 40, y, text=str(puesto + 1), fill="#4a5a52",
                           font=(e.FUENTE_UI, 11, "bold"))
        nuevo = "   ← nuevo" if puntaje is self.app.ultimo_puntaje else ""
        valores = (puntaje.nombre + nuevo, str(puntaje.puntos), puntaje.tiempo_texto(),
                   str(puntaje.movimientos), puntaje.fecha[:10],
                   "Ganó" if puntaje.gano else "Perdió")
        for indice, ((_, x, ancla), valor) in enumerate(zip(columnas[1:], valores)):
            color = e.COLOR_TEXTO_PANEL
            if indice == 5:
                color = "#2f7a4a" if puntaje.gano else e.COLOR_PELIGRO
            cv.create_text(x, y, text=valor, anchor=ancla, fill=color,
                           font=(e.FUENTE_UI, 11, "bold" if indice == 1 else "normal"))

    def _borrar(self):
        """Borra todo el ranking después de confirmar."""
        if confirmar(self.app, "Borrar ranking", "¿Borrar todos los puntajes?\n"
                                                 "Esta acción no se puede deshacer.",
                     "Borrar", "Cancelar", peligro=True):
            self.app.gestor.borrar_todo()
            self.app.ultimo_puntaje = None
            self._dibujar()

    def activar_atajos(self):
        """Esc vuelve al menú."""
        self.app.bind("<Escape>", lambda _e: self.app.mostrar_menu())

    def desactivar_atajos(self):
        """Quita los atajos."""
        self.app.unbind("<Escape>")
