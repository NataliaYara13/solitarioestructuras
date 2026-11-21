"""
Módulo: pantalla_repeticion.py
Clase PantallaRepeticion: vuelve a mostrar una partida jugada por jugada.

CÓMO FUNCIONA (uso de la COLA)
------------------------------
El Tablero de la partida original guarda cada jugada en su Cola 'registro'
(en el orden en que ocurrieron) y también guarda la semilla del barajado.
Para repetir la partida:
    1. Se crea un Tablero NUEVO con la MISMA semilla: el reparto es idéntico.
    2. Se copia la Cola de jugadas.
    3. Cada paso DESENCOLA la siguiente jugada (FIFO: la primera que se hizo
       es la primera que se repite) y se la aplica al tablero nuevo.

Retroceder un paso: la Cola no permite volver atrás, así que se reconstruye
la partida desde el reparto aplicando una jugada menos. Con partidas de
unos cientos de jugadas esto es instantáneo.

CONTROLES
---------
    |◀ inicio   ◀ atrás   ▶ reproducir / ❚❚ pausa   ▶ adelante   ▶| final
    Velocidad: 1x, 2x, 4x.   Teclas: Espacio (reproducir/pausa), ← y →.
"""

import tkinter as tk

from estructuras.cola import Cola
from modelo import jugada as tipos
from modelo.tablero import Tablero, MovimientoInvalido
from vista import estilos as e
from vista.dibujo import BotonCanvas, rect_redondeado
from vista.mesa import dibujar_mesa

PAUSA_BASE_MS = 900
VELOCIDADES = (1, 2, 4)


class PantallaRepeticion(tk.Frame):
    """
    Pantalla que reproduce una partida.

    Atributos:
        app (VentanaPrincipal).
        semilla (int): semilla del barajado de la partida original.
        registro (Cola): copia de la Cola de jugadas de la partida original.
        total (int): cantidad de jugadas.
        tablero (Tablero): tablero donde se reproduce.
        pendientes (Cola): jugadas que faltan por reproducir.
        paso (int): cuántas jugadas se han reproducido.
        reproduciendo (bool): si avanza solo.
        velocidad (int): índice en VELOCIDADES.
    """

    def __init__(self, padre, app, tablero_original):
        """
        Prepara la repetición de la partida del tablero dado.

        Recibe:
            padre (tk.Widget), app (VentanaPrincipal).
            tablero_original (Tablero): la partida terminada.
        Devuelve: nada.
        """
        super().__init__(padre, bg=e.COLOR_MESA)
        self.app = app
        self.semilla = tablero_original.semilla
        self.registro = tablero_original.copia_registro()
        self.total = self.registro.tamano()
        self.reproduciendo = False
        self.velocidad = 0
        self._tarea = None
        self._ultima = None
        self.lienzo = tk.Canvas(self, width=e.ANCHO_VENTANA, height=e.ALTO_VENTANA,
                                bg=e.COLOR_MESA, highlightthickness=0)
        self.lienzo.pack(fill="both", expand=True)
        self._dibujar_barra()
        self._dibujar_controles()
        self.ir_a(0)

    # ======================================================================
    # Interfaz
    # ======================================================================
    def _dibujar_barra(self):
        """Barra superior: progreso, puntos y botón para salir."""
        cv = self.lienzo
        cv.create_rectangle(0, 0, e.ANCHO_VENTANA, e.ALTO_BARRA, fill=e.COLOR_BARRA, outline="")
        cv.create_text(22, 15, text="Jugada", anchor="w", fill=e.COLOR_TEXTO_SUAVE,
                       font=(e.FUENTE_UI, 9))
        self._txt_paso = cv.create_text(22, 36, text="", anchor="w", fill=e.COLOR_TEXTO,
                                        font=(e.FUENTE_UI, 14, "bold"))
        cv.create_text(150, 15, text="Puntos", anchor="w", fill=e.COLOR_TEXTO_SUAVE,
                       font=(e.FUENTE_UI, 9))
        self._txt_puntos = cv.create_text(150, 36, text="", anchor="w", fill=e.COLOR_TEXTO,
                                          font=(e.FUENTE_UI, 14, "bold"))
        cv.create_text(e.ANCHO_VENTANA / 2 - 10, e.ALTO_BARRA / 2, text="REPETICIÓN",
                       fill=e.COLOR_DORADO, font=(e.FUENTE_UI, 12, "bold"))
        BotonCanvas(cv, e.ANCHO_VENTANA - 212, 11, 196, 34, "✕  Salir de la repetición",
                    self.salir, "normal", tamano=10)

    def _dibujar_controles(self):
        """Panel inferior: descripción, barra de progreso y botones."""
        cv = self.lienzo
        y = e.ALTO_VENTANA - 104
        rect_redondeado(cv, 60, y, e.ANCHO_VENTANA - 60, y + 92, 16, fill=e.COLOR_BARRA,
                        outline="", tags=("controles",))
        self._txt_jugada = cv.create_text(e.ANCHO_VENTANA / 2, y + 22, text="",
                                          fill=e.COLOR_TEXTO, font=(e.FUENTE_UI, 11, "bold"),
                                          tags=("controles",))
        cv.create_line(100, y + 46, e.ANCHO_VENTANA - 100, y + 46, fill="#2a4a38", width=6,
                       capstyle="round", tags=("controles",))
        self._linea_progreso = cv.create_line(100, y + 46, 100, y + 46, fill=e.COLOR_DORADO,
                                              width=6, capstyle="round", tags=("controles",))
        botones = (("|◀", self.ir_al_inicio, 56), ("◀", self.retroceder, 56),
                   ("▶  Reproducir", self.alternar_reproduccion, 128),
                   ("▶", self.avanzar, 56), ("▶|", self.ir_al_final, 56))
        total = sum(b[2] for b in botones) + 8 * (len(botones) - 1)
        x = e.ANCHO_VENTANA / 2 - total / 2
        for texto, comando, ancho in botones:
            boton = BotonCanvas(cv, x, y + 58, ancho, 28, texto, comando,
                                "principal" if ancho == 128 else "normal", tamano=10)
            if ancho == 128:
                self._boton_play = boton
            x += ancho + 8
        self._boton_velocidad = BotonCanvas(cv, e.ANCHO_VENTANA - 160, y + 58, 84, 28,
                                            "1x", self.cambiar_velocidad, "normal", tamano=10)

    def _redibujar(self):
        """Dibuja la mesa resaltando la última jugada y actualiza los textos."""
        dibujar_mesa(self.lienzo, self.tablero, self._resaltado(), mostrar_destinos=False)
        self.lienzo.tag_raise("controles")
        self.lienzo.tag_raise("boton")
        cv = self.lienzo
        cv.itemconfigure(self._txt_paso, text=f"{self.paso} / {self.total}")
        cv.itemconfigure(self._txt_puntos, text=str(max(0, self.tablero.puntos)))
        if self._ultima is None:
            texto = "Reparto inicial. Pulsa ▶ para empezar."
        else:
            texto = f"Jugada {self.paso} de {self.total}:  {self._ultima.descripcion()}"
        if self.paso == self.total and self.tablero.gano:
            texto += "   ★ ¡Victoria!"
        cv.itemconfigure(self._txt_jugada, text=texto)
        ancho = (e.ANCHO_VENTANA - 200) * (self.paso / self.total if self.total else 1)
        y = e.ALTO_VENTANA - 104 + 46
        cv.coords(self._linea_progreso, 100, y, 100 + ancho, y)

    def _resaltado(self):
        """
        Calcula qué resaltar según la última jugada aplicada.

        Recibe: nada.
        Devuelve:
            tuple | None con el formato de selección de la mesa.
        """
        j = self._ultima
        if j is None:
            return None
        if j.tipo == tipos.ROBAR:
            return ("descarte",)
        if j.tipo in (tipos.MAZO_A_COLUMNA, tipos.COLUMNA_A_COLUMNA, tipos.FUNDACION_A_COLUMNA):
            columna = self.tablero.columnas[j.destino]
            return ("col", j.destino, max(0, columna.tamano() - j.cantidad))
        if j.tipo in (tipos.MAZO_A_FUNDACION, tipos.COLUMNA_A_FUNDACION):
            return ("fund", j.destino)
        return None

    # ======================================================================
    # Control de la reproducción
    # ======================================================================
    def _copiar_registro(self):
        """
        Crea una copia de la Cola de jugadas para consumirla desencolando.

        Recibe: nada.
        Devuelve:
            Cola.
        """
        copia = Cola()
        for j in self.registro.recorrer():
            copia.encolar(j)
        return copia

    def _aplicar_siguiente(self):
        """
        DESENCOLA la siguiente jugada y la aplica al tablero.

        Recibe: nada.
        Devuelve:
            True si había jugada para aplicar, False si ya terminó.
        """
        if self.pendientes.esta_vacia():
            return False
        jugada = self.pendientes.desencolar()
        try:
            self.tablero.aplicar(jugada)
        except MovimientoInvalido:
            self.pendientes.vaciar()          # registro inconsistente: se detiene
            return False
        self._ultima = jugada
        self.paso += 1
        return True

    def ir_a(self, paso):
        """
        Reconstruye la partida desde el reparto hasta la jugada 'paso'.

        Recibe:
            paso (int): de 0 a total.
        Devuelve: nada.
        """
        paso = max(0, min(self.total, paso))
        self.tablero = Tablero(self.semilla, limite_tiempo=None)   # la repetición no tiene límite
        self.pendientes = self._copiar_registro()
        self.paso = 0
        self._ultima = None
        while self.paso < paso and self._aplicar_siguiente():
            pass
        self._redibujar()

    def avanzar(self):
        """Avanza una jugada (si quedan)."""
        if self._aplicar_siguiente():
            self._redibujar()
        else:
            self._pausar()

    def retroceder(self):
        """Retrocede una jugada (reconstruyendo hasta paso - 1)."""
        self._pausar()
        self.ir_a(self.paso - 1)

    def ir_al_inicio(self):
        """Vuelve al reparto inicial."""
        self._pausar()
        self.ir_a(0)

    def ir_al_final(self):
        """Salta a la última jugada."""
        self._pausar()
        self.ir_a(self.total)

    def alternar_reproduccion(self):
        """Reproduce o pausa."""
        if self.reproduciendo:
            self._pausar()
            return
        if self.paso >= self.total:
            self.ir_a(0)
        self.reproduciendo = True
        self._boton_play.cambiar_texto("❚❚  Pausa")
        self._programar()

    def _programar(self):
        """Programa el siguiente paso automático según la velocidad."""
        espera = PAUSA_BASE_MS // VELOCIDADES[self.velocidad]
        self._tarea = self.after(espera, self._paso_automatico)

    def _paso_automatico(self):
        """Un paso de la reproducción automática."""
        self._tarea = None
        if not self.reproduciendo:
            return
        if self._aplicar_siguiente():
            self._redibujar()
            self._programar()
        else:
            self._pausar()

    def _pausar(self):
        """Detiene la reproducción automática."""
        self.reproduciendo = False
        if self._tarea is not None:
            self.after_cancel(self._tarea)
            self._tarea = None
        self._boton_play.cambiar_texto("▶  Reproducir")

    def cambiar_velocidad(self):
        """Alterna la velocidad entre 1x, 2x y 4x."""
        self.velocidad = (self.velocidad + 1) % len(VELOCIDADES)
        self._boton_velocidad.cambiar_texto(f"{VELOCIDADES[self.velocidad]}x")

    def salir(self):
        """Vuelve al menú."""
        self._pausar()
        self.app.mostrar_menu()

    # ======================================================================
    # Atajos
    # ======================================================================
    def activar_atajos(self):
        """Conecta Espacio, flechas y Esc."""
        a = self.app
        a.bind("<space>", lambda _e: self.alternar_reproduccion())
        a.bind("<Right>", lambda _e: self.avanzar())
        a.bind("<Left>", lambda _e: self.retroceder())
        a.bind("<Escape>", lambda _e: self.salir())

    def desactivar_atajos(self):
        """Quita los atajos y detiene la reproducción."""
        for tecla in ("<space>", "<Right>", "<Left>", "<Escape>"):
            self.app.unbind(tecla)
        self._pausar()
