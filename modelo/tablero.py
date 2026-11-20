"""
Módulo: tablero.py
Clase Tablero: el "director" del juego. Aquí viven TODAS las estructuras.

DISEÑO
------
El Tablero guarda el estado completo de una partida y ejecuta las jugadas.
Antes de cada movimiento le pregunta a Reglas si es válido. Si no lo es,
lanza MovimientoInvalido con un mensaje claro: el estado NO cambia y la
interfaz solo tiene que mostrar el mensaje (el juego nunca se cierra).

DÓNDE SE USA CADA ESTRUCTURA
----------------------------
| Atributo      | Estructura             | Para qué                              |
|---------------|------------------------|---------------------------------------|
| columnas      | 7 x ListaDoble         | Las 7 columnas; mover grupos de cartas |
| fundaciones   | 4 x Pila               | Del As al Rey, solo se usa el tope    |
| mazo          | ListaCircular          | Mazo de robo que da vueltas           |
| historial     | Pila de Jugada         | DESHACER (la última jugada primero)   |
| registro      | Cola de Jugada         | REPETIR la partida en orden           |
| (Baraja)      | ListaDoble -> Pila     | Barajar y repartir                    |
Las 7 columnas y las 4 fundaciones se agrupan en TUPLAS de tamaño fijo solo
para numerarlas (equivale a tener 7 y 4 variables); las estructuras
evaluadas son cada ListaDoble y cada Pila.

REPARTO INICIAL
---------------
    Columna 1: 1 carta, columna 2: 2 cartas, ..., columna 7: 7 cartas
    (28 en total). Solo la última de cada columna queda boca arriba.
    Las 24 restantes van al mazo de robo (ListaCircular).

MAZO DE ROBO
------------
    - robar(): el cursor de la ListaCircular avanza y esa carta queda
      visible (es "la carta del descarte").
    - Si el cursor ya está en la última carta, robar() REINICIA el mazo:
      el cursor vuelve a "antes de empezar" (como voltear el descarte).
    - Al jugar la carta visible, se elimina del mazo y el cursor retrocede
      a la anterior, que vuelve a quedar visible.

FIN DE LA PARTIDA
-----------------
    - VICTORIA: al completar las 4 fundaciones la partida termina sola.
    - DERROTA: si después de una jugada no queda ningún movimiento útil, la
      partida queda BLOQUEADA (atributo 'bloqueada'). La interfaz avisa y
      ofrece: Deshacer (para intentar otro camino) o Terminar (derrota).
      También se puede perder en cualquier momento con rendirse().

PUNTAJE (estilo Windows)
------------------------
    Mazo -> columna: +5    |  Mazo -> fundación: +10   |  Columna -> fundación: +10
    Destapar una carta: +5 |  Fundación -> columna: -15
    Al ganar: bono por tiempo = máximo(0, 600 - segundos).
    Deshacer resta los puntos que había dado la jugada.

                |
"""

import time

from estructuras.cola import Cola
from estructuras.lista_circular import ListaCircular
from estructuras.lista_doble import ListaDoble
from estructuras.pila import Pila
from modelo import jugada as tipos
from modelo.baraja import Baraja
from modelo.jugada import Jugada
from modelo.reglas import Reglas

NUM_COLUMNAS = 7
NUM_FUNDACIONES = 4

PUNTOS_MAZO_A_COLUMNA = 5
PUNTOS_A_FUNDACION = 10
PUNTOS_DESTAPAR = 5
PUNTOS_FUNDACION_A_COLUMNA = -15
BONO_TIEMPO_MAXIMO = 600


class MovimientoInvalido(Exception):
    """
    Error que lanza el Tablero cuando una jugada no se puede hacer.
    Lleva un mensaje pensado para mostrárselo al jugador.
    """


class Tablero:
    """
    Estado y lógica de una partida de Solitario Klondike (robar 1 carta).

    Atributos:
        columnas (tuple de 7 ListaDoble): las columnas del tablero.
        fundaciones (tuple de 4 Pila): las fundaciones.
        mazo (ListaCircular): mazo de robo; su cursor es la carta visible.
        historial (Pila): jugadas para deshacer.
        registro (Cola): jugadas en orden, para repetir la partida.
        semilla (int | None): semilla del barajado (para repetir la partida).
        movimientos (int): cantidad de jugadas hechas.
        puntos (int): puntos acumulados durante la partida.
        vueltas_mazo (int): veces que se reinició el mazo de robo.
        terminada (bool): True si la partida acabó.
        gano (bool): True si terminó con victoria.
        rendido (bool): True si el jugador se rindió (o aceptó la derrota).
        bloqueada (bool): True si no quedan movimientos útiles; la interfaz
            ofrece deshacer o terminar la partida.
        _reloj (función): fuente de tiempo (se puede cambiar en las pruebas).
        _inicio (float): momento en que empezó la partida.
        _segundos_finales (int | None): tiempo congelado al terminar.
    """

    def __init__(self, semilla=None, reloj=time.monotonic):
        """
        Crea un tablero y reparte una partida nueva.

        Recibe:
            semilla (int | None): para repetir un barajado concreto.
            reloj (función): devuelve los segundos actuales (por defecto
                time.monotonic). Las pruebas pasan un reloj falso.
        Devuelve: nada.
        Complejidad: O(n²) por el barajado.
        """
        self._reloj = reloj
        self.nueva_partida(semilla)

    # ======================================================================
    # Partida nueva y reparto
    # ======================================================================
    def nueva_partida(self, semilla=None):
        """
        Reinicia todo el estado y reparte una partida nueva.
        Si no se da semilla, se genera una al azar y se guarda, para poder
        repetir exactamente esta partida después.

        Recibe:
            semilla (int | None).
        Devuelve: nada.
        """
        if semilla is None:
            semilla = int(time.time() * 1000) % 1_000_000_007
        self.semilla = semilla
        self.columnas = tuple(ListaDoble() for _ in range(NUM_COLUMNAS))
        self.fundaciones = tuple(Pila() for _ in range(NUM_FUNDACIONES))
        self.mazo = ListaCircular()
        self.historial = Pila()
        self.registro = Cola()
        self.movimientos = 0
        self.puntos = 0
        self.vueltas_mazo = 0
        self.terminada = False
        self.gano = False
        self.rendido = False
        self.bloqueada = False
        self._inicio = self._reloj()
        self._segundos_finales = None
        self._repartir(Baraja(semilla).generar_mazo())

    def _repartir(self, baraja):
        """
        Reparte desde la Pila de la baraja: la columna i recibe i+1 cartas
        y solo la última queda boca arriba. Lo que sobra va al mazo de robo.

        Recibe:
            baraja (Pila): las 52 cartas barajadas.
        Devuelve: nada.
        """
        for i in range(NUM_COLUMNAS):
            for _ in range(i + 1):
                self.columnas[i].insertar_final(baraja.desapilar())
            self.columnas[i].ver_final().destapar()
        while not baraja.esta_vacia():
            self.mazo.insertar_final(baraja.desapilar())

    # ======================================================================
    # Consultas para la interfaz
    # ======================================================================
    def carta_visible_mazo(self):
        """
        Devuelve la carta visible del descarte (la del cursor del mazo).

        Recibe: nada.
        Devuelve:
            Carta, o None si no hay carta visible.
        """
        return self.mazo.ver_actual()

    def cartas_por_robar(self):
        """
        Cuántas cartas quedan antes de que haya que reiniciar el mazo.

        Recibe: nada.
        Devuelve:
            int.
        """
        return self.mazo.tamano() - 1 - self.mazo.posicion_cursor()

    def segundos(self):
        """
        Tiempo de juego en segundos (se congela al terminar la partida).

        Recibe: nada.
        Devuelve:
            int.
        """
        if self._segundos_finales is not None:
            return self._segundos_finales
        return int(self._reloj() - self._inicio)

    def puntaje_final(self):
        """
        Puntaje para el ranking: los puntos acumulados (nunca negativos)
        más, si ganó, el bono por tiempo.

        Recibe: nada.
        Devuelve:
            int.
        """
        total = max(0, self.puntos)
        if self.gano:
            total += max(0, BONO_TIEMPO_MAXIMO - self.segundos())
        return total

    def buscar_fundacion_para(self, carta):
        """
        Busca una fundación que acepte la carta.

        Recibe:
            carta (Carta).
        Devuelve:
            int con el índice de la fundación (0 a 3), o -1 si ninguna la acepta.
        Complejidad: O(1).
        """
        for i in range(NUM_FUNDACIONES):
            if Reglas.puede_ir_a_fundacion(carta, self.fundaciones[i]):
                return i
        return -1

    # ======================================================================
    # Jugadas
    # ======================================================================
    def robar(self):
        """
        Muestra la siguiente carta del mazo. Si ya se mostró la última,
        reinicia el mazo (el cursor vuelve a antes de empezar).

        Recibe: nada.
        Devuelve:
            Jugada realizada (ROBAR o REINICIAR_MAZO).
        Lanza:
            MovimientoInvalido si el mazo está vacío o la partida terminó.
        Complejidad: O(n).
        """
        self._validar_en_juego()
        if self.mazo.esta_vacia():
            raise MovimientoInvalido("No quedan cartas en el mazo")
        posicion_anterior = self.mazo.posicion_cursor()
        if self.mazo.cursor_en_ultimo():
            self.mazo.reiniciar_cursor()
            self.vueltas_mazo += 1
            jugada = Jugada(tipos.REINICIAR_MAZO, cantidad=0,
                            posicion_mazo=posicion_anterior)
        else:
            carta = self.mazo.avanzar()
            carta.destapar()
            jugada = Jugada(tipos.ROBAR, carta=carta, posicion_mazo=posicion_anterior)
        return self._registrar(jugada)

    def mover_mazo_a_columna(self, destino):
        """
        Lleva la carta visible del mazo al final de una columna.

        Recibe:
            destino (int): índice de la columna (0 a 6).
        Devuelve:
            Jugada realizada.
        Lanza:
            MovimientoInvalido si no hay carta visible o no encaja.
        Complejidad: O(n).
        """
        self._validar_en_juego()
        self._validar_columna(destino)
        carta = self._carta_visible_obligatoria()
        columna = self.columnas[destino]
        if not Reglas.puede_ir_a_columna(carta, columna):
            raise MovimientoInvalido(self._mensaje_columna(carta, columna))
        posicion = self.mazo.posicion_cursor()
        self.mazo.eliminar_actual()
        columna.insertar_final(carta)
        return self._registrar(Jugada(tipos.MAZO_A_COLUMNA, destino=destino, carta=carta,
                                      posicion_mazo=posicion, puntos=PUNTOS_MAZO_A_COLUMNA))

    def mover_mazo_a_fundacion(self, destino=None):
        """
        Sube la carta visible del mazo a una fundación.

        Recibe:
            destino (int | None): índice de la fundación (0 a 3). Si es None,
                se busca automáticamente una que la acepte.
        Devuelve:
            Jugada realizada.
        Lanza:
            MovimientoInvalido si no hay carta visible o no se puede subir.
        Complejidad: O(n).
        """
        self._validar_en_juego()
        carta = self._carta_visible_obligatoria()
        destino = self._resolver_fundacion(carta, destino)
        posicion = self.mazo.posicion_cursor()
        self.mazo.eliminar_actual()
        self.fundaciones[destino].apilar(carta)
        return self._registrar(Jugada(tipos.MAZO_A_FUNDACION, destino=destino, carta=carta,
                                      posicion_mazo=posicion, puntos=PUNTOS_A_FUNDACION))

    def mover_columna_a_columna(self, origen, posicion, destino):
        """
        Mueve la carta (o el grupo de cartas) que empieza en 'posicion' de
        la columna 'origen' al final de la columna 'destino'.
        Usa cortar_desde() y concatenar() de la ListaDoble.
        Si la columna origen queda con una carta boca abajo al final, se destapa.

        Recibe:
            origen (int): columna de donde sale (0 a 6).
            posicion (int): posición de la primera carta del grupo.
            destino (int): columna a donde llega (0 a 6).
        Devuelve:
            Jugada realizada.
        Lanza:
            MovimientoInvalido si el grupo no es válido o no encaja.
        Complejidad: O(n).
        """
        self._validar_en_juego()
        self._validar_columna(origen)
        self._validar_columna(destino)
        col_origen = self.columnas[origen]
        col_destino = self.columnas[destino]
        if origen == destino:
            raise MovimientoInvalido("La carta ya está en esa columna")
        if not Reglas.es_escalera_valida(col_origen, posicion):
            raise MovimientoInvalido("Solo se pueden mover cartas boca arriba que formen "
                                     "una escalera (descendente y alternando color)")
        primera = col_origen.obtener(posicion)
        if not Reglas.puede_ir_a_columna(primera, col_destino):
            raise MovimientoInvalido(self._mensaje_columna(primera, col_destino))
        cantidad = col_origen.tamano() - posicion
        col_destino.concatenar(col_origen.cortar_desde(posicion))
        volteo = self._destapar_final(col_origen)
        return self._registrar(Jugada(tipos.COLUMNA_A_COLUMNA, origen=origen, destino=destino,
                                      cantidad=cantidad, carta=primera, volteo_carta=volteo,
                                      puntos=PUNTOS_DESTAPAR if volteo else 0))

    def mover_columna_a_fundacion(self, origen, destino=None):
        """
        Sube la carta visible (la última) de una columna a una fundación.

        Recibe:
            origen (int): columna (0 a 6).
            destino (int | None): fundación (0 a 3); None = buscarla sola.
        Devuelve:
            Jugada realizada.
        Lanza:
            MovimientoInvalido si la columna está vacía o la carta no puede subir.
        Complejidad: O(1) (más la revisión de fin de partida).
        """
        self._validar_en_juego()
        self._validar_columna(origen)
        columna = self.columnas[origen]
        if columna.esta_vacia():
            raise MovimientoInvalido("Esa columna está vacía")
        carta = columna.ver_final()
        destino = self._resolver_fundacion(carta, destino)
        columna.eliminar_final()
        self.fundaciones[destino].apilar(carta)
        volteo = self._destapar_final(columna)
        puntos = PUNTOS_A_FUNDACION + (PUNTOS_DESTAPAR if volteo else 0)
        return self._registrar(Jugada(tipos.COLUMNA_A_FUNDACION, origen=origen, destino=destino,
                                      carta=carta, volteo_carta=volteo, puntos=puntos))

    def mover_fundacion_a_columna(self, origen, destino):
        """
        Baja la carta del tope de una fundación a una columna (está permitido
        en Klondike, pero resta puntos).

        Recibe:
            origen (int): fundación (0 a 3).
            destino (int): columna (0 a 6).
        Devuelve:
            Jugada realizada.
        Lanza:
            MovimientoInvalido si la fundación está vacía o la carta no encaja.
        Complejidad: O(1).
        """
        self._validar_en_juego()
        self._validar_fundacion(origen)
        self._validar_columna(destino)
        fundacion = self.fundaciones[origen]
        if fundacion.esta_vacia():
            raise MovimientoInvalido("Esa fundación está vacía")
        carta = fundacion.ver_tope()
        columna = self.columnas[destino]
        if not Reglas.puede_ir_a_columna(carta, columna):
            raise MovimientoInvalido(self._mensaje_columna(carta, columna))
        fundacion.desapilar()
        columna.insertar_final(carta)
        return self._registrar(Jugada(tipos.FUNDACION_A_COLUMNA, origen=origen, destino=destino,
                                      carta=carta, puntos=PUNTOS_FUNDACION_A_COLUMNA))

    # ======================================================================
    # Deshacer
    # ======================================================================
    def puede_deshacer(self):
        """
        Indica si hay jugadas para deshacer.

        Recibe: nada.
        Devuelve:
            True si el historial no está vacío y la partida sigue.
        Complejidad: O(1).
        """
        return not self.terminada and not self.historial.esta_vacia()

    def deshacer(self):
        """
        Deshace la última jugada: la DESAPILA del historial (LIFO) y hace el
        movimiento al revés. También resta los puntos que había dado.
        En el registro (Cola) se encola una jugada DESHACER para que la
        repetición de la partida sea fiel.

        Recibe: nada.
        Devuelve:
            La Jugada que se deshizo.
        Lanza:
            MovimientoInvalido si no hay nada que deshacer.
        Complejidad: O(n).
        """
        self._validar_en_juego()
        if self.historial.esta_vacia():
            raise MovimientoInvalido("No hay jugadas para deshacer")
        jugada = self.historial.desapilar()
        self._revertir(jugada)
        self.puntos -= jugada.puntos
        self.movimientos += 1
        self.registro.encolar(Jugada(tipos.DESHACER, cantidad=0))
        self.bloqueada = not self.hay_movimientos()
        return jugada

    def _revertir(self, j):
        """
        Hace el movimiento contrario de una jugada.

        Recibe:
            j (Jugada): la jugada a revertir.
        Devuelve: nada.
        Complejidad: O(n).
        """
        if j.tipo in (tipos.ROBAR, tipos.REINICIAR_MAZO):
            self.mazo.mover_cursor_a(j.posicion_mazo)
            if j.tipo == tipos.REINICIAR_MAZO:
                self.vueltas_mazo -= 1
            return

        if j.tipo == tipos.MAZO_A_COLUMNA:
            carta = self.columnas[j.destino].eliminar_final()
        elif j.tipo == tipos.MAZO_A_FUNDACION:
            carta = self.fundaciones[j.destino].desapilar()
        else:
            carta = None
        if carta is not None:
            # La carta vuelve exactamente a su lugar en el mazo y queda visible
            self.mazo.insertar_en_posicion(j.posicion_mazo, carta)
            self.mazo.mover_cursor_a(j.posicion_mazo)
            return

        if j.tipo == tipos.COLUMNA_A_COLUMNA:
            origen = self.columnas[j.origen]
            destino = self.columnas[j.destino]
            if j.volteo_carta:
                origen.ver_final().tapar()
            origen.concatenar(destino.cortar_desde(destino.tamano() - j.cantidad))
        elif j.tipo == tipos.COLUMNA_A_FUNDACION:
            origen = self.columnas[j.origen]
            if j.volteo_carta:
                origen.ver_final().tapar()
            origen.insertar_final(self.fundaciones[j.destino].desapilar())
        elif j.tipo == tipos.FUNDACION_A_COLUMNA:
            self.fundaciones[j.origen].apilar(self.columnas[j.destino].eliminar_final())

    # ======================================================================
    # Rendirse, fin de partida y pista
    # ======================================================================
    def rendirse(self):
        """
        Termina la partida como derrota por decisión del jugador. También se
        usa cuando la partida está bloqueada y el jugador elige terminar.

        Recibe: nada.
        Devuelve: nada.
        Lanza:
            MovimientoInvalido si la partida ya había terminado.
        Complejidad: O(1).
        """
        self._validar_en_juego()
        self.rendido = True
        self._terminar(gano=False)

    def hay_movimientos(self):
        """
        Indica si queda algún movimiento útil (lo decide Reglas).

        Recibe: nada.
        Devuelve:
            True si queda al menos uno.
        Complejidad: O(N).
        """
        return Reglas.hay_movimientos_posibles(self.columnas, self.fundaciones, self.mazo)

    def pista(self):
        """
        Sugiere un movimiento útil, en este orden de prioridad:
            1. Subir a una fundación una carta visible de columna o del mazo.
            2. Mover un grupo entre columnas, solo si es útil (destapa una
               carta, vacía una columna o libera una carta para la fundación).
            3. Jugar la carta visible del mazo en una columna.
            4. Robar del mazo.

        Recibe: nada.
        Devuelve:
            str con la sugerencia, o None si no hay ninguna.
        Complejidad: O(N).
        """
        if self.terminada:
            return None
        for i in range(NUM_COLUMNAS):
            carta = self.columnas[i].ver_final()
            if carta is not None and self.buscar_fundacion_para(carta) != -1:
                return f"Sube {self._txt(carta)} de la columna {i + 1} a una fundación"
        visible = self.carta_visible_mazo()
        if visible is not None and self.buscar_fundacion_para(visible) != -1:
            return f"Sube {self._txt(visible)} del mazo a una fundación"
        for i in range(NUM_COLUMNAS):
            columna = self.columnas[i]
            posicion = 0
            for carta in columna.recorrer_adelante():
                if carta.boca_arriba and Reglas.es_movimiento_de_grupo_util(
                        columna, posicion, self.fundaciones):
                    for d in range(NUM_COLUMNAS):
                        if Reglas.puede_mover_grupo(columna, posicion, self.columnas[d]):
                            return (f"Mueve {self._txt(carta)} de la columna {i + 1} "
                                    f"a la columna {d + 1}")
                posicion += 1
        if visible is not None:
            for d in range(NUM_COLUMNAS):
                if Reglas.puede_ir_a_columna(visible, self.columnas[d]):
                    return f"Pon {self._txt(visible)} del mazo en la columna {d + 1}"
        if not self.mazo.esta_vacia():
            return "Roba una carta del mazo"
        return None

    # ======================================================================
    # Repetición de la partida
    # ======================================================================
    def copia_registro(self):
        """
        Devuelve una copia de la Cola de registro, para reproducirla
        desencolando sin perder el registro original.

        Recibe: nada.
        Devuelve:
            Cola con las mismas jugadas en el mismo orden.
        Complejidad: O(n).
        """
        copia = Cola()
        for j in self.registro.recorrer():
            copia.encolar(j)
        return copia

    def aplicar(self, j):
        """
        Vuelve a ejecutar una jugada registrada. Se usa para la REPETICIÓN:
        se crea un Tablero con la misma semilla y se le aplican, en orden,
        las jugadas desencoladas del registro.

        Recibe:
            j (Jugada): jugada a ejecutar.
        Devuelve:
            La Jugada resultante.
        Lanza:
            MovimientoInvalido si la jugada no es aplicable en este estado.
        Complejidad: la de la jugada correspondiente.
        """
        if j.tipo in (tipos.ROBAR, tipos.REINICIAR_MAZO):
            return self.robar()
        if j.tipo == tipos.MAZO_A_COLUMNA:
            return self.mover_mazo_a_columna(j.destino)
        if j.tipo == tipos.MAZO_A_FUNDACION:
            return self.mover_mazo_a_fundacion(j.destino)
        if j.tipo == tipos.COLUMNA_A_COLUMNA:
            posicion = self.columnas[j.origen].tamano() - j.cantidad
            return self.mover_columna_a_columna(j.origen, posicion, j.destino)
        if j.tipo == tipos.COLUMNA_A_FUNDACION:
            return self.mover_columna_a_fundacion(j.origen, j.destino)
        if j.tipo == tipos.FUNDACION_A_COLUMNA:
            return self.mover_fundacion_a_columna(j.origen, j.destino)
        return self.deshacer()

    # ======================================================================
    # Métodos internos
    # ======================================================================
    def _registrar(self, jugada):
        """
        Guarda una jugada recién hecha: la APILA en el historial (deshacer),
        la ENCOLA en el registro (repetir), suma puntos y movimientos y
        revisa si la partida terminó.

        Recibe:
            jugada (Jugada).
        Devuelve:
            La misma jugada.
        Complejidad: O(N) por la revisión de fin de partida.
        """
        self.historial.apilar(jugada)
        self.registro.encolar(jugada)
        self.puntos += jugada.puntos
        self.movimientos += 1
        self._revisar_fin()
        return jugada

    def _revisar_fin(self):
        """
        Si hay victoria, termina la partida. Si no quedan movimientos útiles,
        marca la partida como BLOQUEADA: la interfaz le ofrece al jugador
        deshacer (para intentar otro camino) o terminar (derrota).
        No se termina sola para no quitarle la opción de deshacer.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(N).
        """
        if Reglas.es_victoria(self.fundaciones):
            self.bloqueada = False
            self._terminar(gano=True)
        else:
            self.bloqueada = not self.hay_movimientos()

    def _terminar(self, gano):
        """
        Marca la partida como terminada y congela el tiempo.

        Recibe:
            gano (bool).
        Devuelve: nada.
        Complejidad: O(1).
        """
        self._segundos_finales = self.segundos()
        self.terminada = True
        self.gano = gano

    def _destapar_final(self, columna):
        """
        Si la carta del final de la columna está boca abajo, la destapa.

        Recibe:
            columna (ListaDoble).
        Devuelve:
            True si destapó una carta, False si no.
        Complejidad: O(1).
        """
        carta = columna.ver_final()
        if carta is not None and not carta.boca_arriba:
            carta.destapar()
            return True
        return False

    def _carta_visible_obligatoria(self):
        """
        Devuelve la carta visible del mazo o lanza error si no hay.

        Recibe: nada.
        Devuelve:
            Carta.
        Lanza:
            MovimientoInvalido si no hay carta visible.
        """
        carta = self.carta_visible_mazo()
        if carta is None:
            raise MovimientoInvalido("No hay carta visible en el mazo: primero roba una")
        return carta

    def _resolver_fundacion(self, carta, destino):
        """
        Valida (o busca, si destino es None) la fundación para la carta.

        Recibe:
            carta (Carta), destino (int | None).
        Devuelve:
            int con el índice de una fundación válida.
        Lanza:
            MovimientoInvalido si ninguna fundación la acepta.
        """
        if destino is None:
            destino = self.buscar_fundacion_para(carta)
            if destino == -1:
                raise MovimientoInvalido(f"{carta.nombre()} todavía no puede subir a una "
                                         "fundación")
            return destino
        self._validar_fundacion(destino)
        if not Reglas.puede_ir_a_fundacion(carta, self.fundaciones[destino]):
            tope = self.fundaciones[destino].ver_tope()
            if tope is None:
                raise MovimientoInvalido("Una fundación vacía solo acepta un As")
            raise MovimientoInvalido(f"{carta.nombre()} no va sobre {tope.nombre()}: debe ser "
                                     "del mismo palo y valer uno más")
        return destino

    def _mensaje_columna(self, carta, columna):
        """
        Arma el mensaje de error cuando una carta no encaja en una columna.

        Recibe:
            carta (Carta), columna (ListaDoble).
        Devuelve:
            str con la explicación.
        """
        if columna.esta_vacia():
            return "Una columna vacía solo acepta un Rey"
        destino = columna.ver_final()
        return (f"{self._txt(carta)} no va sobre {self._txt(destino)}: debe ser de "
                "distinto color y valer uno menos")

    def _validar_en_juego(self):
        """Lanza MovimientoInvalido si la partida ya terminó."""
        if self.terminada:
            raise MovimientoInvalido("La partida ya terminó")

    def _validar_columna(self, indice):
        """Lanza MovimientoInvalido si el índice de columna no existe (0 a 6)."""
        if not isinstance(indice, int) or not 0 <= indice < NUM_COLUMNAS:
            raise MovimientoInvalido(f"Columna inexistente: {indice}")

    def _validar_fundacion(self, indice):
        """Lanza MovimientoInvalido si el índice de fundación no existe (0 a 3)."""
        if not isinstance(indice, int) or not 0 <= indice < NUM_FUNDACIONES:
            raise MovimientoInvalido(f"Fundación inexistente: {indice}")

    @staticmethod
    def _txt(carta):
        """Texto corto de una carta aunque esté boca abajo, ej. '7♣'."""
        return f"{carta.texto_valor()}{carta.simbolo()}"

    def __str__(self):
        """
        Dibujo en texto del tablero, útil para depurar en consola.

        Recibe: nada.
        Devuelve:
            str con mazo, fundaciones y columnas.
        """
        visible = self.carta_visible_mazo()
        texto = f"Mazo: {self.mazo.tamano()} cartas | Visible: {visible or '--'}\n"
        texto += "Fundaciones: " + "  ".join(
            str(f.ver_tope() or "--") for f in self.fundaciones) + "\n"
        for i in range(NUM_COLUMNAS):
            texto += f"C{i + 1}: {self.columnas[i]}\n"
        texto += (f"Movimientos: {self.movimientos} | Puntos: {self.puntos} | "
                  f"Tiempo: {self.segundos()} s")
        return texto
