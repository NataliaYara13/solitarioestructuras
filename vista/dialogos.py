"""
Módulo: dialogos.py
Ventanas de diálogo MODALES del juego (mientras están abiertas, la mesa no
responde): confirmar una acción, partida bloqueada y fin de partida.

Todas se dibujan en un Canvas con el mismo estilo del juego (panel claro,
borde dorado y botones BotonCanvas), en lugar de los cuadros grises de
Windows.

Uso general:
    respuesta = confirmar(ventana, "Título", "¿Seguro?")
    opcion = DialogoFin(ventana, tablero, gestor).esperar()
"""

import tkinter as tk

from modelo.puntaje import Puntaje, LARGO_MAXIMO_NOMBRE
from modelo.tablero import BONO_TIEMPO_MAXIMO
from vista import estilos as e
from vista.dibujo import BotonCanvas

COLOR_TEXTO_SECUNDARIO = "#4a5a52"
COLOR_DESTACADO = "#8a6d10"


class DialogoModal(tk.Toplevel):
    """
    Base de todos los diálogos: ventana hija, centrada sobre la principal,
    que bloquea la ventana principal hasta cerrarse.

    Atributos:
        resultado: valor que devuelve esperar() (lo fija cerrar()).
        lienzo (tk.Canvas): donde se dibuja el contenido.
        ancho, alto (int): tamaño del diálogo.
    """

    def __init__(self, padre, ancho, alto, titulo, icono="", resultado_al_cerrar=None):
        """
        Crea el diálogo con su título y, opcionalmente, un ícono.

        Recibe:
            padre (tk.Tk): ventana principal.
            ancho, alto (int): tamaño.
            titulo (str): título grande.
            icono (str): símbolo opcional sobre el título (★, ⚠...).
            resultado_al_cerrar: lo que se devuelve si se cierra con la X o Esc.
        Devuelve: nada.
        """
        super().__init__(padre)
        self.resultado = resultado_al_cerrar
        self._resultado_al_cerrar = resultado_al_cerrar
        self.ancho, self.alto = ancho, alto
        self.title(e.TITULO_VENTANA)
        self.resizable(False, False)
        self.transient(padre)
        self.configure(bg=e.COLOR_DORADO)
        self.lienzo = tk.Canvas(self, width=ancho - 4, height=alto - 4, bg=e.COLOR_PANEL,
                                highlightthickness=0)
        self.lienzo.pack(padx=2, pady=2)
        x = padre.winfo_rootx() + (padre.winfo_width() - ancho) // 2
        y = padre.winfo_rooty() + (padre.winfo_height() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{max(0, x)}+{max(0, y)}")
        self.protocol("WM_DELETE_WINDOW", self._cerrar_por_defecto)
        self.bind("<Escape>", lambda _e: self._cerrar_por_defecto())

        centro = ancho / 2
        if icono:
            self.lienzo.create_text(centro, 40, text=icono, fill=e.COLOR_DORADO,
                                    font=(e.FUENTE_SIMBOLO, 28))
        self.lienzo.create_text(centro, 84 if icono else 38, text=titulo,
                                fill=e.COLOR_TEXTO_PANEL, font=(e.FUENTE_TITULO, 21, "bold"))

    def texto(self, y, contenido, color=COLOR_TEXTO_SECUNDARIO, tamano=11, estilo="normal"):
        """
        Escribe un texto centrado en el diálogo.

        Recibe:
            y (int), contenido (str), color (str), tamano (int), estilo (str).
        Devuelve:
            int: id del texto (para cambiarlo después).
        """
        return self.lienzo.create_text(self.ancho / 2, y, text=contenido, fill=color,
                                       font=(e.FUENTE_UI, tamano, estilo), justify="center")

    def boton(self, x, y, ancho, texto, valor, estilo="claro", alto=44):
        """
        Agrega un botón que cierra el diálogo devolviendo 'valor'.

        Recibe:
            x, y, ancho (int), texto (str), valor: lo que devolverá esperar().
            estilo (str), alto (int).
        Devuelve:
            BotonCanvas.
        """
        return BotonCanvas(self.lienzo, x, y, ancho, alto, texto,
                           lambda: self.cerrar(valor), estilo, tamano=11)

    def cerrar(self, valor):
        """
        Guarda el resultado y cierra el diálogo.

        Recibe:
            valor: el resultado.
        Devuelve: nada.
        """
        self.resultado = valor
        self.grab_release()
        self.destroy()

    def _cerrar_por_defecto(self):
        """Cierra con el resultado por defecto (X de la ventana o tecla Esc)."""
        self.cerrar(self._resultado_al_cerrar)

    def esperar(self):
        """
        Muestra el diálogo de forma modal y espera a que se cierre.

        Recibe: nada.
        Devuelve:
            El resultado elegido por el jugador.
        """
        try:
            self.wait_visibility()
            self.grab_set()
        except tk.TclError:
            # La ventana se cerró antes de terminar de mostrarse, o el sistema
            # no permitió bloquear la ventana principal: se sigue sin fallar.
            pass
        if self.winfo_exists():
            self.focus_force()
            self.wait_window()
        return self.resultado


def confirmar(padre, titulo, mensaje, texto_si="Sí", texto_no="Cancelar", peligro=False):
    """
    Pregunta sí/no con el estilo del juego.

    Recibe:
        padre (tk.Tk), titulo (str), mensaje (str).
        texto_si, texto_no (str): textos de los botones.
        peligro (bool): si True, el botón "sí" es rojo.
    Devuelve:
        True si el jugador confirmó, False si no.
    """
    d = DialogoModal(padre, 440, 230, titulo, resultado_al_cerrar=False)
    d.texto(96, mensaje)
    d.boton(40, 156, 170, texto_si, True, "peligro" if peligro else "principal")
    d.boton(230, 156, 170, texto_no, False, "claro")
    d.bind("<Return>", lambda _e: d.cerrar(True))
    return d.esperar()


def dialogo_bloqueada(padre):
    """
    Avisa que no quedan movimientos útiles y ofrece deshacer o terminar.

    Recibe:
        padre (tk.Tk).
    Devuelve:
        "deshacer", "terminar" o None (si cerró la ventana).
    """
    d = DialogoModal(padre, 470, 300, "No quedan movimientos", "⚠")
    d.texto(140, "Ninguna carta del mazo ni de las columnas\nse puede mover a un lugar útil.")
    d.texto(190, "Puedes deshacer para probar otro camino.", estilo="italic")
    d.boton(40, 226, 180, "↶  Deshacer", "deshacer", "principal")
    d.boton(250, 226, 180, "Terminar partida", "terminar", "peligro")
    return d.esperar()


class DialogoFin(DialogoModal):
    """
    Diálogo de fin de partida (victoria o derrota): muestra el resumen,
    pide el nombre si el puntaje entra al ranking y ofrece qué hacer después.

    Atributos:
        tablero (Tablero): la partida terminada.
        gestor (GestorPuntajes): el ranking.
        puntaje_guardado (Puntaje | None): el puntaje si se guardó.
        _entrada (tk.Entry | None): campo para el nombre.
    """

    def __init__(self, padre, tablero, gestor):
        """
        Arma el diálogo según el resultado de la partida.

        Recibe:
            padre (tk.Tk), tablero (Tablero), gestor (GestorPuntajes).
        Devuelve: nada.
        """
        self.tablero = tablero
        self.gestor = gestor
        self.puntaje_guardado = None
        self._entrada = None
        self._final = tablero.puntaje_final()
        self._puede_guardar = self._final > 0 and gestor.entra_en_ranking(self._final)
        alto = 500 if self._puede_guardar else 400
        if tablero.gano:
            titulo, icono = "¡Ganaste!", "★"
        elif tablero.tiempo_agotado:
            titulo, icono = "Se acabó el tiempo", "⏱"
        else:
            titulo, icono = ("Te rendiste" if tablero.rendido else "Fin de la partida"), "✕"
        super().__init__(padre, 500, alto, titulo, icono, resultado_al_cerrar="menu")
        self._dibujar_resumen()
        if self._puede_guardar:
            self._dibujar_nombre()
        y_botones = alto - 76
        self.boton(28, y_botones, 140, "Nueva partida", "nueva", "principal")
        self.boton(178, y_botones, 140, "▶ Repetición", "repeticion")
        self.boton(328, y_botones, 140, "Menú", "menu")

    def _dibujar_resumen(self):
        """
        Escribe la tabla de puntos, bono, puntaje final, tiempo y movimientos.

        Recibe: nada.
        Devuelve: nada.
        """
        t = self.tablero
        segundos = t.segundos()
        filas = (("Puntos de la partida", str(max(0, t.puntos))),)
        if t.gano:
            filas += ((f"Bono por tiempo ({BONO_TIEMPO_MAXIMO} − {segundos} s)",
                       f"+{max(0, BONO_TIEMPO_MAXIMO - segundos)}"),)
        filas += (("Puntaje final", str(self._final)),
                  ("Tiempo  ·  Movimientos",
                   f"{segundos // 60:02d}:{segundos % 60:02d}  ·  {t.movimientos}"))
        cv = self.lienzo
        for i, (etiqueta, valor) in enumerate(filas):
            y = 132 + i * 30
            final = etiqueta == "Puntaje final"
            cv.create_text(56, y, text=etiqueta, anchor="w", fill=COLOR_TEXTO_SECUNDARIO,
                           font=(e.FUENTE_UI, 11, "bold" if final else "normal"))
            cv.create_text(440, y, text=valor, anchor="e",
                           fill=COLOR_DESTACADO if final else e.COLOR_TEXTO_PANEL,
                           font=(e.FUENTE_UI, 12 if final else 11, "bold"))
        self._y_fin_resumen = 132 + len(filas) * 30
        cv.create_line(56, self._y_fin_resumen - 8, 440, self._y_fin_resumen - 8,
                       fill="#d9d2bf")
        if not self._puede_guardar:
            mensaje = ("Este puntaje no alcanza para el top 10." if self._final > 0
                       else "Sin puntos no hay registro en el ranking.")
            self.texto(self._y_fin_resumen + 24, mensaje, estilo="italic")

    def _dibujar_nombre(self):
        """
        Dibuja el aviso de ranking, el campo del nombre y el botón Guardar.

        Recibe: nada.
        Devuelve: nada.
        """
        y = self._y_fin_resumen + 18
        self.texto(y, "¡Este puntaje entra al ranking!", COLOR_DESTACADO, 12, "bold")
        self.lienzo.create_text(56, y + 34, text=f"Tu nombre (máx. {LARGO_MAXIMO_NOMBRE}):",
                                anchor="w", fill=COLOR_TEXTO_SECUNDARIO, font=(e.FUENTE_UI, 10))
        self._entrada = tk.Entry(self.lienzo, font=(e.FUENTE_UI, 12), relief="solid", bd=1)
        self.lienzo.create_window(56, y + 50, window=self._entrada, anchor="nw",
                                  width=260, height=34)
        self._entrada.focus_set()
        self._entrada.bind("<Return>", lambda _e: self._guardar())
        self._boton_guardar = BotonCanvas(self.lienzo, 326, y + 50, 118, 34, "Guardar",
                                          self._guardar, "principal", tamano=11)
        self._mensaje = self.texto(y + 104, "")

    def _guardar(self):
        """
        Valida el nombre y guarda el puntaje en el ranking (Árbol BST).
        Si el nombre no es válido, muestra el error sin cerrar el diálogo.

        Recibe: nada.
        Devuelve: nada.
        """
        if self.puntaje_guardado is not None:
            return
        t = self.tablero
        try:
            puntaje = Puntaje(self._entrada.get(), self._final, t.segundos(), t.movimientos,
                              gano=t.gano)
        except ValueError:
            self.lienzo.itemconfigure(self._mensaje, text="Escribe un nombre para guardar.",
                                      fill=e.COLOR_PELIGRO)
            return
        puesto = self.gestor.agregar(puntaje)
        if puesto == -1:
            self.lienzo.itemconfigure(self._mensaje, text="No se pudo guardar el puntaje.",
                                      fill=e.COLOR_PELIGRO)
            return
        self.puntaje_guardado = puntaje
        self._entrada.configure(state="disabled")
        self._boton_guardar.cambiar_texto("✓ Listo")
        self._boton_guardar.habilitar(False)
        self.lienzo.itemconfigure(self._mensaje, text=f"Guardado: puesto {puesto} del ranking.",
                                  fill="#2f7a4a")
