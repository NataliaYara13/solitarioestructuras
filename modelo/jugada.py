"""
Módulo: jugada.py
Clase Jugada: la "memoria" de un movimiento del juego.

DISEÑO
------
Cada vez que el jugador hace algo (robar, mover cartas, subir a fundación),
el Tablero crea una Jugada con TODO lo necesario para:
    - DESHACERLA: se apila en la Pila de deshacer. Al deshacer se desapila la
      última y se hace el movimiento al revés.
    - REPETIRLA: se encola en la Cola de registro. Al ver la repetición se
      desencolan en el mismo orden en que ocurrieron.

La Jugada NO ejecuta nada: solo guarda datos. Quien la ejecuta o la revierte
es el Tablero.

TIPOS DE JUGADA
---------------
| Tipo                 | Qué pasa                                      |
|----------------------|-----------------------------------------------|
| ROBAR                | Se muestra la siguiente carta del mazo        |
| REINICIAR_MAZO       | El mazo vuelve a empezar desde la primera     |
| MAZO_A_COLUMNA       | La carta visible del mazo va a una columna    |
| MAZO_A_FUNDACION     | La carta visible del mazo sube a fundación    |
| COLUMNA_A_COLUMNA    | Una carta o grupo pasa de una columna a otra  |
| COLUMNA_A_FUNDACION  | La carta visible de una columna sube          |
| FUNDACION_A_COLUMNA  | Una carta baja de la fundación a una columna  |
| DESHACER             | Se deshizo la jugada anterior (solo se guarda |
|                      | en la Cola, para que la repetición sea fiel)  |

DATOS QUE GUARDA (y para qué sirven al deshacer)
------------------------------------------------
    origen / destino:  índice de la columna (0 a 6) o de la fundación (0 a 3).
                       None cuando el origen es el mazo.
    cantidad:          cuántas cartas se movieron (grupos de columna a columna).
    carta:             la carta principal movida (para mensajes y repetición).
    volteo_carta:      True si al mover se destapó la carta de abajo en la
                       columna origen. Al deshacer hay que volver a taparla.
    posicion_mazo:     posición que tenía la carta en el mazo de robo, para
                       devolverla exactamente al mismo lugar al deshacer.
    puntos:            puntos que dio la jugada; al deshacer se restan.


"""

ROBAR = "ROBAR"
REINICIAR_MAZO = "REINICIAR_MAZO"
MAZO_A_COLUMNA = "MAZO_A_COLUMNA"
MAZO_A_FUNDACION = "MAZO_A_FUNDACION"
COLUMNA_A_COLUMNA = "COLUMNA_A_COLUMNA"
COLUMNA_A_FUNDACION = "COLUMNA_A_FUNDACION"
FUNDACION_A_COLUMNA = "FUNDACION_A_COLUMNA"
DESHACER = "DESHACER"

TIPOS = (ROBAR, REINICIAR_MAZO, MAZO_A_COLUMNA, MAZO_A_FUNDACION,
         COLUMNA_A_COLUMNA, COLUMNA_A_FUNDACION, FUNDACION_A_COLUMNA, DESHACER)


class Jugada:
    """
    Registro de un movimiento.

    Atributos:
        tipo (str): uno de TIPOS.
        origen (int | None): índice de columna/fundación de origen; None si es el mazo.
        destino (int | None): índice de columna/fundación de destino; None si no aplica.
        cantidad (int): número de cartas movidas.
        carta (Carta | None): carta principal involucrada.
        volteo_carta (bool): si se destapó una carta en la columna origen.
        posicion_mazo (int | None): posición de la carta en el mazo de robo.
        puntos (int): puntos ganados (o perdidos) con la jugada.
    """

    def __init__(self, tipo, origen=None, destino=None, cantidad=1, carta=None,
                 volteo_carta=False, posicion_mazo=None, puntos=0):
        """
        Crea el registro de una jugada.

        Recibe:
            tipo (str): uno de TIPOS (obligatorio).
            origen (int | None): de dónde sale.
            destino (int | None): a dónde llega.
            cantidad (int): cuántas cartas se movieron (mínimo 0).
            carta (Carta | None): carta principal.
            volteo_carta (bool): si se destapó una carta en el origen.
            posicion_mazo (int | None): posición de la carta en el mazo.
            puntos (int): puntos de la jugada.
        Devuelve:
            Nada (es el constructor).
        Lanza:
            ValueError si el tipo no existe o la cantidad es negativa.
        Complejidad: O(1).
        """
        if tipo not in TIPOS:
            raise ValueError(f"Tipo de jugada inválido: {tipo}")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError(f"Cantidad inválida: {cantidad}")
        self.tipo = tipo
        self.origen = origen
        self.destino = destino
        self.cantidad = cantidad
        self.carta = carta
        self.volteo_carta = volteo_carta
        self.posicion_mazo = posicion_mazo
        self.puntos = puntos

    def mueve_cartas(self):
        """
        Indica si la jugada cambió cartas de lugar (robar y reiniciar el
        mazo no mueven cartas a columnas ni fundaciones; deshacer depende
        de la jugada deshecha, así que tampoco se cuenta).

        Recibe: nada.
        Devuelve:
            True si movió cartas.
        Complejidad: O(1).
        """
        return self.tipo not in (ROBAR, REINICIAR_MAZO, DESHACER)

    def descripcion(self):
        """
        Texto legible de la jugada, para la repetición y los mensajes.
        Las columnas y fundaciones se muestran contando desde 1.
        Ejemplo: "7♣ de la columna 3 a la columna 5".

        Recibe: nada.
        Devuelve:
            str.
        Complejidad: O(1).
        """
        carta = self._texto_carta()
        o = None if self.origen is None else self.origen + 1
        d = None if self.destino is None else self.destino + 1
        if self.tipo == ROBAR:
            return f"Robó {carta} del mazo" if self.carta else "Robó del mazo"
        if self.tipo == REINICIAR_MAZO:
            return "Reinició el mazo de robo"
        if self.tipo == DESHACER:
            return "Deshizo la jugada anterior"
        if self.tipo == MAZO_A_COLUMNA:
            return f"{carta} del mazo a la columna {d}"
        if self.tipo == MAZO_A_FUNDACION:
            return f"{carta} del mazo a la fundación {d}"
        if self.tipo == COLUMNA_A_COLUMNA:
            grupo = f" (grupo de {self.cantidad})" if self.cantidad > 1 else ""
            return f"{carta}{grupo} de la columna {o} a la columna {d}"
        if self.tipo == COLUMNA_A_FUNDACION:
            return f"{carta} de la columna {o} a la fundación {d}"
        return f"{carta} de la fundación {o} a la columna {d}"

    def _texto_carta(self):
        """
        Método interno: texto de la carta aunque esté boca abajo.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "7♣", o "carta" si no hay carta guardada.
        """
        if self.carta is None:
            return "carta"
        return f"{self.carta.texto_valor()}{self.carta.simbolo()}"

    def __str__(self):
        """
        Texto de la jugada (igual a descripcion()).

        Recibe: nada.
        Devuelve:
            str.
        """
        return self.descripcion()

    def __repr__(self):
        """
        Texto para depurar con todos los datos.

        Recibe: nada.
        Devuelve:
            str.
        """
        return (f"Jugada({self.tipo}, origen={self.origen}, destino={self.destino}, "
                f"cantidad={self.cantidad}, volteo={self.volteo_carta}, "
                f"pos_mazo={self.posicion_mazo}, puntos={self.puntos})")
