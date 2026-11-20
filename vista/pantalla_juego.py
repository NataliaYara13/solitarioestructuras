"""
Módulo: pantalla_juego.py
Clase PantallaJuego: la mesa donde se juega. Conecta la interfaz con el
Tablero (modelo): la pantalla NO decide reglas, solo traduce clics en
llamadas al Tablero y muestra lo que el Tablero responde.

CÓMO SE JUEGA CON EL MOUSE
--------------------------
    - Clic en el mazo ................ roba una carta (o reinicia el mazo).
    - Clic en una carta boca arriba .. la selecciona (con las de encima).
                                       Los destinos válidos se resaltan.
    - Clic en un destino ............. mueve la selección (si es válido).
    - Clic en lo seleccionado ........ cancela la selección.
    - Doble clic en una carta ........ la sube a su fundación.
    - Clic derecho o Esc ............. cancela la selección.

ATAJOS DE TECLADO
-----------------
    Ctrl+Z: deshacer   ·   H: pista   ·   Espacio: robar   ·   Esc: cancelar

FLUJO DE CADA JUGADA
--------------------
    clic -> que_hay_en() -> método del Tablero
        - si funciona: se redibuja la mesa y se actualiza la barra.
        - si lanza MovimientoInvalido: se muestra el mensaje en rojo y
          nada cambia (el juego nunca se cierra).
    Después de cada jugada se revisa si se ganó o si la partida quedó
    bloqueada, para abrir el diálogo correspondiente.
"""

import tkinter as tk

from modelo.tablero import Tablero, MovimientoInvalido
from vista import estilos as e
from vista.dibujo import BotonCanvas, rect_redondeado
from vista.dialogos import confirmar, dialogo_bloqueada, DialogoFin
from vista.mesa import dibujar_mesa, que_hay_en

Y_AVISO = e.ALTO_VENTANA - 40
DURACION_AVISO_MS = 3500


class PantallaJuego(tk.Frame):
    """
    Pantalla de la partida.

    Atributos:
        app (VentanaPrincipal): para volver al menú, ver puntajes, etc.
        tablero (Tablero): la partida en curso (modelo).
        seleccion (tuple | None): lo que el jugador tiene seleccionado:
            ("descarte",), ("col", i, pos) o ("fund", i).
        _ignorar_proximo_clic (bool): evita que el segundo "soltar" de un
            doble clic se tome como un clic normal.
        lienzo (tk.Canvas): donde se dibuja todo.
        _textos (dict): ids de los textos de tiempo, movimientos y puntos.
        _boton_deshacer (BotonCanvas).
        _tarea_aviso, _tarea_reloj: tareas programadas con after().
    """

    def __init__(self, padre, app, semilla=None):
        """
        Crea la pantalla y una partida nueva.

        Recibe:
            padre (tk.Widget), app (VentanaPrincipal).
            semilla (int | None): para repetir un barajado concreto.
        Devuelve: nada.
        """
        super().__init__(padre, bg=e.COLOR_MESA)
        self.app = app
        self.tablero = Tablero(semilla)
        self.seleccion = None
        self._ignorar_proximo_clic = False
        self._tarea_aviso = None
        self._tarea_reloj = None
        self.lienzo = tk.Canvas(self, width=e.ANCHO_VENTANA, height=e.ALTO_VENTANA,
                                bg=e.COLOR_MESA, highlightthickness=0)
        self.lienzo.pack(fill="both", expand=True)
        self._dibujar_barra()
        self.lienzo.bind("<ButtonRelease-1>", self._al_hacer_clic)
        self.lienzo.bind("<Double-Button-1>", self._al_hacer_doble_clic)
        self.lienzo.bind("<Button-3>", lambda _e: self._cancelar_seleccion())
        self.redibujar()
        self._tick_reloj()

    # ======================================================================
    # Barra superior
    # ======================================================================
    def _dibujar_barra(self):
        """
        Dibuja la barra superior: tiempo, movimientos, puntos y botones.

        Recibe: nada.
        Devuelve: nada.
        """
        cv = self.lienzo
        cv.create_rectangle(0, 0, e.ANCHO_VENTANA, e.ALTO_BARRA, fill=e.COLOR_BARRA,
                            outline="", tags=("barra",))
        self._textos = {}
        x = 22
        for clave, etiqueta in (("tiempo", "Tiempo"), ("movimientos", "Movimientos"),
                                ("puntos", "Puntos")):
            cv.create_text(x, 15, text=etiqueta, anchor="w", fill=e.COLOR_TEXTO_SUAVE,
                           font=(e.FUENTE_UI, 9), tags=("barra",))
            self._textos[clave] = cv.create_text(x, 36, text="0", anchor="w",
                                                 fill=e.COLOR_TEXTO,
                                                 font=(e.FUENTE_UI, 14, "bold"),
                                                 tags=("barra",))
            x += 108
        botones = (("↶  Deshacer", self.deshacer, "principal", 112),
                   ("?  Pista", self.mostrar_pista, "normal", 84),
                   ("Rendirse", self.rendirse, "normal", 90),
                   ("Menú", self.volver_al_menu, "normal", 70))
        x = e.ANCHO_VENTANA - 16
        for texto, comando, estilo, ancho in botones:
            x -= ancho
            boton = BotonCanvas(cv, x, 11, ancho, 34, texto, comando, estilo, tamano=10)
            if comando == self.deshacer:
                self._boton_deshacer = boton
            x -= 8

    def _actualizar_barra(self):
        """
        Actualiza tiempo, movimientos, puntos y el estado del botón Deshacer.

        Recibe: nada.
        Devuelve: nada.
        """
        t = self.tablero
        segundos = t.segundos()
        cv = self.lienzo
        cv.itemconfigure(self._textos["tiempo"], text=f"{segundos // 60:02d}:{segundos % 60:02d}")
        cv.itemconfigure(self._textos["movimientos"], text=str(t.movimientos))
        cv.itemconfigure(self._textos["puntos"], text=str(max(0, t.puntos)))
        self._boton_deshacer.habilitar(t.puede_deshacer())

    def _tick_reloj(self):
        """
        Actualiza el reloj cada segundo mientras la partida siga.
        Se reprograma a sí mismo con after().

        Recibe: nada.
        Devuelve: nada.
        """
        if not self.winfo_exists():
            return
        self._actualizar_barra()
        if not self.tablero.terminada:
            self._tarea_reloj = self.after(1000, self._tick_reloj)

    # ======================================================================
    # Dibujo y avisos
    # ======================================================================
    def redibujar(self):
        """
        Vuelve a dibujar la mesa con el estado actual del Tablero.

        Recibe: nada.
        Devuelve: nada.
        """
        dibujar_mesa(self.lienzo, self.tablero, self.seleccion)
        self.lienzo.tag_raise("aviso")
        self._actualizar_barra()

    def aviso(self, texto, tipo="error", fijo=False):
        """
        Muestra un mensaje en la parte de abajo.

        Recibe:
            texto (str).
            tipo (str): "error" (rojo), "info" (azul) o "pista" (verde).
            fijo (bool): si False, desaparece solo después de unos segundos.
        Devuelve: nada.
        """
        self._quitar_aviso()
        color = {"error": e.COLOR_ERROR, "info": e.COLOR_INFO, "pista": e.COLOR_PISTA}[tipo]
        prefijo = "✕  " if tipo == "error" else ""
        ancho = min(e.ANCHO_VENTANA - 40, max(360, len(texto) * 8 + 70))
        cv = self.lienzo
        rect_redondeado(cv, e.ANCHO_VENTANA / 2 - ancho / 2, Y_AVISO - 19,
                        e.ANCHO_VENTANA / 2 + ancho / 2, Y_AVISO + 19, 19, fill=color,
                        outline="", tags=("aviso",))
        cv.create_text(e.ANCHO_VENTANA / 2, Y_AVISO, text=prefijo + texto, fill=e.COLOR_TEXTO,
                       font=(e.FUENTE_UI, 11, "bold"), tags=("aviso",))
        if not fijo:
            self._tarea_aviso = self.after(DURACION_AVISO_MS, self._quitar_aviso)

    def _quitar_aviso(self):
        """Borra el aviso actual y cancela su temporizador."""
        if self._tarea_aviso is not None:
            self.after_cancel(self._tarea_aviso)
            self._tarea_aviso = None
        self.lienzo.delete("aviso")

    # ======================================================================
    # Clics
    # ======================================================================
    def _al_hacer_clic(self, evento):
        """
        Decide qué hacer con un clic en la mesa.

        Recibe:
            evento (tk.Event): trae las coordenadas x, y del clic.
        Devuelve: nada.
        """
        if self._ignorar_proximo_clic:
            # Es el segundo "soltar" de un doble clic: ya se atendió
            self._ignorar_proximo_clic = False
            return
        if evento.y <= e.ALTO_BARRA or self.tablero.terminada:
            return
        lugar = que_hay_en(self.lienzo, evento.x, evento.y)
        if lugar is None:
            self._cancelar_seleccion()
            return
        if lugar[0] == "mazo":
            self.seleccion = None
            self._ejecutar(self.tablero.robar)
        elif self.seleccion is None:
            self._seleccionar(lugar)
        elif self._es_lo_seleccionado(lugar):
            self._cancelar_seleccion()
        else:
            self._mover_a(lugar)

    def _al_hacer_doble_clic(self, evento):
        """
        Doble clic: sube a la fundación la carta del descarte o la última
        carta de una columna.
        Nota: Tkinter avisa el doble clic al PRESIONAR por segunda vez; al
        SOLTAR llega además un clic normal, que se debe ignorar.

        Recibe:
            evento (tk.Event).
        Devuelve: nada.
        """
        if evento.y <= e.ALTO_BARRA or self.tablero.terminada:
            return
        self._ignorar_proximo_clic = True
        lugar = que_hay_en(self.lienzo, evento.x, evento.y)
        self.seleccion = None
        if lugar == ("descarte",) and self.tablero.carta_visible_mazo() is not None:
            self._ejecutar(self.tablero.mover_mazo_a_fundacion)
        elif lugar is not None and lugar[0] == "col":
            columna = self.tablero.columnas[lugar[1]]
            if lugar[2] == columna.tamano() - 1:
                self._ejecutar(self.tablero.mover_columna_a_fundacion, lugar[1])
            else:
                self.aviso("Solo la última carta de una columna puede subir a la fundación")
                self.redibujar()
        else:
            self.redibujar()

    def _seleccionar(self, lugar):
        """
        Selecciona una carta si se puede (boca arriba y existente).

        Recibe:
            lugar (tuple): resultado de que_hay_en().
        Devuelve: nada.
        """
        tipo = lugar[0]
        if tipo == "descarte":
            if self.tablero.carta_visible_mazo() is None:
                self.aviso("No hay carta en el descarte: haz clic en el mazo para robar",
                           "info")
                return
            self.seleccion = ("descarte",)
        elif tipo == "col":
            carta = self.tablero.columnas[lugar[1]].obtener(lugar[2])
            if not carta.boca_arriba:
                self.aviso("Esa carta está boca abajo: se destapa al mover las de encima")
                return
            self.seleccion = lugar
        elif tipo == "fund":
            if self.tablero.fundaciones[lugar[1]].esta_vacia():
                return
            self.seleccion = lugar
        else:
            return
        self._quitar_aviso()
        self.redibujar()

    def _es_lo_seleccionado(self, lugar):
        """
        Indica si el clic fue sobre lo que ya estaba seleccionado.

        Recibe:
            lugar (tuple).
        Devuelve:
            bool.
        """
        s = self.seleccion
        if s[0] == "col" and lugar[0] == "col":
            return s[1] == lugar[1] and lugar[2] >= s[2]
        return s == lugar

    def _mover_a(self, lugar):
        """
        Intenta mover la selección al lugar indicado, llamando al método
        correcto del Tablero según el origen y el destino.

        Recibe:
            lugar (tuple): destino del clic.
        Devuelve: nada.
        """
        origen = self.seleccion
        self.seleccion = None
        t = self.tablero
        if lugar[0] in ("col", "colzona"):
            destino = lugar[1]
            if origen[0] == "descarte":
                self._ejecutar(t.mover_mazo_a_columna, destino)
            elif origen[0] == "col":
                if origen[1] == destino:
                    # Clic en otra carta de la misma columna: se cambia la selección
                    if lugar[0] == "col":
                        self._seleccionar(lugar)
                    else:
                        self.redibujar()
                    return
                self._ejecutar(t.mover_columna_a_columna, origen[1], origen[2], destino)
            else:
                self._ejecutar(t.mover_fundacion_a_columna, origen[1], destino)
        elif lugar[0] == "fund":
            destino = lugar[1]
            if origen[0] == "descarte":
                self._ejecutar(t.mover_mazo_a_fundacion, destino)
            elif origen[0] == "col":
                if origen[2] != t.columnas[origen[1]].tamano() - 1:
                    self.aviso("A la fundación solo se sube una carta a la vez")
                    self.redibujar()
                    return
                self._ejecutar(t.mover_columna_a_fundacion, origen[1], destino)
            else:
                self.redibujar()
        else:                                   # clic en el descarte con otra selección
            self._seleccionar(lugar)

    def _cancelar_seleccion(self):
        """Quita la selección actual y redibuja."""
        if self.seleccion is not None:
            self.seleccion = None
            self.redibujar()

    # ======================================================================
    # Ejecutar jugadas del Tablero
    # ======================================================================
    def _ejecutar(self, metodo, *argumentos):
        """
        Ejecuta una jugada del Tablero. Si es inválida, muestra el mensaje;
        si funciona, redibuja y revisa si la partida terminó o se bloqueó.

        Recibe:
            metodo (función del Tablero), *argumentos: sus parámetros.
        Devuelve:
            True si la jugada se hizo, False si fue inválida.
        """
        try:
            metodo(*argumentos)
        except MovimientoInvalido as error:
            self.redibujar()
            self.aviso(str(error))
            return False
        self._quitar_aviso()
        self.redibujar()
        self.after_idle(self._revisar_estado)
        return True

    def _revisar_estado(self):
        """
        Abre el diálogo de fin si se ganó, o el de bloqueo si no quedan
        movimientos.

        Recibe: nada.
        Devuelve: nada.
        """
        if not self.winfo_exists():
            return
        if self.tablero.terminada:
            self._fin_de_partida()
        elif self.tablero.bloqueada:
            opcion = dialogo_bloqueada(self.app)
            if opcion == "deshacer":
                self.deshacer()
            elif opcion == "terminar":
                self.tablero.rendirse()
                self._fin_de_partida()
            else:
                self.aviso("Sin movimientos útiles: deshaz o ríndete", "info", fijo=True)

    def _fin_de_partida(self):
        """
        Muestra el diálogo de fin y hace lo que el jugador elija.

        Recibe: nada.
        Devuelve: nada.
        """
        self.redibujar()
        dialogo = DialogoFin(self.app, self.tablero, self.app.gestor)
        opcion = dialogo.esperar()
        if dialogo.puntaje_guardado is not None:
            self.app.ultimo_puntaje = dialogo.puntaje_guardado
        if opcion == "nueva":
            self.app.mostrar_juego()
        elif opcion == "repeticion":
            self.app.mostrar_repeticion(self.tablero)
        else:
            self.app.mostrar_menu()

    # ======================================================================
    # Botones de la barra
    # ======================================================================
    def deshacer(self):
        """Deshace la última jugada (Pila del Tablero)."""
        if self.tablero.terminada:
            return
        self.seleccion = None
        if self._ejecutar(self.tablero.deshacer):
            self.aviso("Jugada deshecha", "info")

    def mostrar_pista(self):
        """Muestra la pista que sugiere el Tablero."""
        if self.tablero.terminada:
            return
        pista = self.tablero.pista()
        self.aviso("Pista: " + (pista or "no hay movimientos útiles"), "pista")

    def rendirse(self):
        """Pide confirmación y termina la partida como derrota."""
        if self.tablero.terminada:
            return
        if confirmar(self.app, "Rendirse", "¿Seguro que quieres rendirte?\n"
                                           "La partida terminará como derrota.",
                     "Rendirme", "Seguir jugando", peligro=True):
            self.tablero.rendirse()
            self._fin_de_partida()

    def volver_al_menu(self):
        """Vuelve al menú (pide confirmación si la partida está en curso)."""
        en_curso = not self.tablero.terminada and self.tablero.movimientos > 0
        if not en_curso or confirmar(self.app, "Volver al menú",
                                     "¿Abandonar la partida actual?\nSe perderá el progreso.",
                                     "Abandonar", "Seguir jugando", peligro=True):
            self.app.mostrar_menu()

    def robar(self):
        """Roba una carta (atajo de teclado)."""
        if not self.tablero.terminada:
            self.seleccion = None
            self._ejecutar(self.tablero.robar)

    # ======================================================================
    # Atajos de teclado y limpieza
    # ======================================================================
    def activar_atajos(self):
        """Conecta los atajos de teclado de la partida."""
        a = self.app
        a.bind("<Control-z>", lambda _e: self.deshacer())
        a.bind("<Control-Z>", lambda _e: self.deshacer())
        a.bind("<Escape>", lambda _e: self._cancelar_seleccion())
        a.bind("<space>", lambda _e: self.robar())
        for tecla in ("h", "H"):
            a.bind(tecla, lambda _e: self.mostrar_pista())

    def desactivar_atajos(self):
        """Quita los atajos de teclado y detiene las tareas programadas."""
        for tecla in ("<Control-z>", "<Control-Z>", "<Escape>", "<space>", "h", "H"):
            self.app.unbind(tecla)
        for tarea in (self._tarea_reloj, self._tarea_aviso):
            if tarea is not None:
                self.after_cancel(tarea)
        self._tarea_reloj = self._tarea_aviso = None
