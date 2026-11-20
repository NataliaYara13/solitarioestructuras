"""
Módulo: ventana_principal.py
Clase VentanaPrincipal: la ventana de Tkinter del juego.

Se encarga de:
    - Crear la ventana (tamaño fijo, centrada en la pantalla).
    - Cambiar entre pantallas (menú, juego, puntajes, reglas, repetición).
    - Guardar el GestorPuntajes, que comparten todas las pantallas.
    - Atrapar cualquier error inesperado y mostrarlo en un mensaje, para
      que el juego NUNCA se cierre por un error (requisito del proyecto).
"""

import tkinter as tk
import traceback
from tkinter import messagebox

from modelo.gestor_puntajes import GestorPuntajes
from vista import estilos as e
from vista.dialogos import confirmar
from vista.pantalla_juego import PantallaJuego
from vista.pantalla_menu import PantallaMenu
from vista.pantalla_puntajes import PantallaPuntajes
from vista.pantalla_reglas import PantallaReglas
from vista.pantalla_repeticion import PantallaRepeticion


class VentanaPrincipal(tk.Tk):
    """
    Ventana principal del Solitario.

    Atributos:
        gestor (GestorPuntajes): ranking de mejores puntajes (Árbol BST).
        ultimo_puntaje (Puntaje | None): el último puntaje guardado, para
            resaltarlo en la pantalla de puntajes.
        pantalla_actual (tk.Frame | None): la pantalla que se está mostrando.
    """

    def __init__(self):
        """
        Crea la ventana, carga los puntajes y muestra el menú.

        Recibe: nada.
        Devuelve: nada.
        """
        super().__init__()
        self.title(e.TITULO_VENTANA)
        self.configure(bg=e.COLOR_MESA)
        self.resizable(False, False)
        self._centrar()
        self.protocol("WM_DELETE_WINDOW", self.salir)
        self.gestor = GestorPuntajes()
        self.ultimo_puntaje = None
        self.pantalla_actual = None
        self.mostrar_menu()

    def _centrar(self):
        """
        Ubica la ventana en el centro de la pantalla.

        Recibe: nada.
        Devuelve: nada.
        """
        x = max(0, (self.winfo_screenwidth() - e.ANCHO_VENTANA) // 2)
        y = max(0, (self.winfo_screenheight() - e.ALTO_VENTANA) // 2 - 30)
        self.geometry(f"{e.ANCHO_VENTANA}x{e.ALTO_VENTANA}+{x}+{y}")

    def _cambiar_pantalla(self, nueva):
        """
        Quita la pantalla actual (y sus atajos) y muestra la nueva.

        Recibe:
            nueva (tk.Frame): la pantalla a mostrar. Si tiene el método
                activar_atajos, se llama.
        Devuelve: nada.
        """
        if self.pantalla_actual is not None:
            if hasattr(self.pantalla_actual, "desactivar_atajos"):
                self.pantalla_actual.desactivar_atajos()
            self.pantalla_actual.destroy()
        self.pantalla_actual = nueva
        nueva.pack(fill="both", expand=True)
        if hasattr(nueva, "activar_atajos"):
            nueva.activar_atajos()

    # ------------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------------
    def mostrar_menu(self):
        """Muestra la pantalla de entrada. No recibe ni devuelve nada."""
        self._cambiar_pantalla(PantallaMenu(self, self))

    def mostrar_juego(self, semilla=None):
        """
        Empieza una partida nueva.

        Recibe:
            semilla (int | None): opcional, para repetir un barajado.
        Devuelve: nada.
        """
        self._cambiar_pantalla(PantallaJuego(self, self, semilla))

    def mostrar_puntajes(self):
        """Muestra el ranking de mejores puntajes. No recibe ni devuelve nada."""
        self._cambiar_pantalla(PantallaPuntajes(self, self))

    def mostrar_reglas(self):
        """Muestra las reglas y los controles. No recibe ni devuelve nada."""
        self._cambiar_pantalla(PantallaReglas(self, self))

    def mostrar_repeticion(self, tablero):
        """
        Muestra la repetición de una partida terminada.

        Recibe:
            tablero (Tablero): la partida a repetir.
        Devuelve: nada.
        """
        self._cambiar_pantalla(PantallaRepeticion(self, self, tablero))

    def salir(self):
        """
        Pregunta antes de cerrar el juego. Si hay una partida en curso,
        avisa que se perderá.

        Recibe: nada.
        Devuelve: nada.
        """
        mensaje = "¿Seguro que quieres salir del juego?"
        partida = getattr(self.pantalla_actual, "tablero", None)
        if isinstance(self.pantalla_actual, PantallaJuego) and not partida.terminada \
                and partida.movimientos > 0:
            mensaje += "\nLa partida actual se perderá."
        if confirmar(self, "Salir", mensaje, "Salir", "Cancelar", peligro=True):
            self.destroy()

    # ------------------------------------------------------------------
    # Robustez: ningún error cierra el juego
    # ------------------------------------------------------------------
    def report_callback_exception(self, tipo, valor, rastro):
        """
        Tkinter llama a este método cuando ocurre un error dentro de un
        evento (un clic, una tecla...). En vez de cerrarse, el juego muestra
        el error y sigue funcionando.

        Recibe:
            tipo, valor, rastro: datos del error que entrega Tkinter.
        Devuelve: nada.
        """
        traceback.print_exception(tipo, valor, rastro)
        messagebox.showerror(e.TITULO_VENTANA,
                             f"Ocurrió un error inesperado, pero el juego sigue abierto:\n\n"
                             f"{valor}", parent=self)
