"""
Módulo: reglas.py
Clase Reglas: TODAS las reglas del Solitario Klondike en un solo lugar.

DISEÑO
------
Reglas no guarda estado (no tiene atributos): solo responde preguntas del
tipo "¿esta jugada es válida?". Por eso todos sus métodos son estáticos
(@staticmethod): se llaman directamente como Reglas.metodo(...), sin crear
un objeto.

Ventaja: si en la sustentación preguntan "¿dónde se valida que un 7 negro
vaya sobre un 8 rojo?", la respuesta es un solo lugar: Reglas.

REGLAS DEL KLONDIKE (variante de robar 1 carta)
-----------------------------------------------
1. COLUMNAS (7): las cartas se apilan en orden DESCENDENTE y ALTERNANDO
   COLOR. Ejemplo: 8♥ (rojo) -> 7♣ (negro) -> 6♦ (rojo).
2. COLUMNA VACÍA: solo puede recibir un REY (o un grupo que empiece en Rey).
3. GRUPOS: se puede mover un grupo de cartas boca arriba si forman una
   escalera válida (descendente y alternando color).
4. FUNDACIONES (4): una por palo, en orden ASCENDENTE desde el As hasta el
   Rey. Solo se sube una carta a la vez.
5. VICTORIA: las 4 fundaciones completas (13 cartas cada una = 52).
6. DERROTA: no queda ningún movimiento útil (o el jugador se rinde).

Estructuras que recibe:
    - columna:   ListaDoble de Carta (cabeza = la de atrás, final = la visible).
    - fundacion: Pila de Carta (tope = la última que subió).
    - mazo:      ListaCircular de Carta (mazo de robo).


"""

from modelo.carta import Carta, AS, REY

CARTAS_POR_FUNDACION = 13


class Reglas:
    """
    Conjunto de validaciones del juego. No se instancia: todos los métodos
    son estáticos.
    """

    # ------------------------------------------------------------------
    # Regla básica entre dos cartas
    # ------------------------------------------------------------------
    @staticmethod
    def puede_ir_sobre(carta, destino):
        """
        Regla de las columnas entre dos cartas: 'carta' puede ponerse sobre
        'destino' si ambas están boca arriba, son de distinto color y
        'carta' vale exactamente uno menos.
        Ejemplo: 7♣ sobre 8♥ -> True;  7♦ sobre 8♥ -> False (mismo color).

        Recibe:
            carta (Carta): la carta que se quiere mover.
            destino (Carta | None): la carta sobre la que se pondría.
        Devuelve:
            True si es válido, False si no.
        Complejidad: O(1).
        """
        if carta is None or destino is None:
            return False
        if not carta.boca_arriba or not destino.boca_arriba:
            return False
        return carta.es_roja() != destino.es_roja() and carta.valor == destino.valor - 1

    # ------------------------------------------------------------------
    # Columnas
    # ------------------------------------------------------------------
    @staticmethod
    def puede_ir_a_columna(carta, columna):
        """
        Indica si 'carta' puede ponerse al final de 'columna'.
            - Columna vacía: solo un Rey.
            - Columna con cartas: se aplica puede_ir_sobre con la carta visible.

        Recibe:
            carta (Carta): la carta (o la primera carta del grupo) a mover.
            columna (ListaDoble): la columna destino.
        Devuelve:
            True si es válido, False si no.
        Complejidad: O(1).
        """
        if carta is None or not carta.boca_arriba:
            return False
        if columna.esta_vacia():
            return carta.valor == REY
        return Reglas.puede_ir_sobre(carta, columna.ver_final())

    @staticmethod
    def es_escalera_valida(columna, posicion):
        """
        Indica si las cartas desde 'posicion' hasta el final de la columna
        forman un grupo que se puede mover junto: todas boca arriba,
        descendentes y alternando color.

        Ejemplo: columna [##, 9♠, 8♥, 7♣]
            posicion 1 -> True  (9♠ 8♥ 7♣ es escalera)
            posicion 0 -> False (la primera está boca abajo)

        Recibe:
            columna (ListaDoble): la columna origen.
            posicion (int): de 0 a tamaño - 1.
        Devuelve:
            True si el grupo es válido, False si no (o si la posición no existe).
        Complejidad: O(n), recorre la columna una vez.
        """
        if not isinstance(posicion, int) or posicion < 0 or posicion >= columna.tamano():
            return False
        indice = 0
        anterior = None
        for carta in columna.recorrer_adelante():
            if indice >= posicion:
                if not carta.boca_arriba:
                    return False
                if anterior is not None and not Reglas.puede_ir_sobre(carta, anterior):
                    return False
                anterior = carta
            indice += 1
        return True

    @staticmethod
    def puede_mover_grupo(origen, posicion, destino):
        """
        Indica si el grupo que empieza en 'posicion' de la columna 'origen'
        se puede mover a la columna 'destino'.
        Condiciones: el grupo es una escalera válida y su primera carta
        puede ir a la columna destino. No se puede mover a la misma columna.

        Recibe:
            origen (ListaDoble): columna de donde sale el grupo.
            posicion (int): posición de la primera carta del grupo.
            destino (ListaDoble): columna a donde llega.
        Devuelve:
            True si es válido, False si no.
        Complejidad: O(n).
        """
        if origen is destino:
            return False
        if not Reglas.es_escalera_valida(origen, posicion):
            return False
        return Reglas.puede_ir_a_columna(origen.obtener(posicion), destino)

    # ------------------------------------------------------------------
    # Fundaciones
    # ------------------------------------------------------------------
    @staticmethod
    def puede_ir_a_fundacion(carta, fundacion):
        """
        Indica si 'carta' puede subir a 'fundacion'.
            - Fundación vacía: solo un As.
            - Fundación con cartas: mismo palo y exactamente uno más.

        Recibe:
            carta (Carta): la carta a subir.
            fundacion (Pila): la fundación destino.
        Devuelve:
            True si es válido, False si no.
        Complejidad: O(1).
        """
        if carta is None or not carta.boca_arriba:
            return False
        tope = fundacion.ver_tope()
        if tope is None:
            return carta.valor == AS
        return carta.palo == tope.palo and carta.valor == tope.valor + 1

    @staticmethod
    def fundacion_completa(fundacion):
        """
        Indica si una fundación ya tiene las 13 cartas de su palo.

        Recibe:
            fundacion (Pila).
        Devuelve:
            True si tiene 13 cartas.
        Complejidad: O(1).
        """
        return fundacion.tamano() == CARTAS_POR_FUNDACION

    # ------------------------------------------------------------------
    # Ganar y perder
    # ------------------------------------------------------------------
    @staticmethod
    def es_victoria(fundaciones):
        """
        Victoria: todas las fundaciones están completas.

        Recibe:
            fundaciones: las 4 fundaciones (Pilas), recorribles con un for.
        Devuelve:
            True si se ganó la partida.
        Complejidad: O(1) (siempre son 4 fundaciones).
        """
        for fundacion in fundaciones:
            if not Reglas.fundacion_completa(fundacion):
                return False
        return True

    @staticmethod
    def _va_a_alguna_fundacion(carta, fundaciones):
        """
        Método interno: indica si la carta puede subir a alguna fundación.

        Recibe:
            carta (Carta), fundaciones (las 4 Pilas).
        Devuelve:
            True si al menos una fundación la acepta.
        Complejidad: O(1).
        """
        for fundacion in fundaciones:
            if Reglas.puede_ir_a_fundacion(carta, fundacion):
                return True
        return False

    @staticmethod
    def _va_a_alguna_columna(carta, columnas, excepto=None):
        """
        Método interno: indica si la carta puede ir a alguna columna.

        Recibe:
            carta (Carta), columnas (las 7 ListaDoble),
            excepto (ListaDoble | None): columna que no se debe revisar
                (la columna de donde sale la carta).
        Devuelve:
            True si al menos una columna la acepta.
        Complejidad: O(1) (siempre son 7 columnas).
        """
        for columna in columnas:
            if columna is not excepto and Reglas.puede_ir_a_columna(carta, columna):
                return True
        return False

    @staticmethod
    def es_movimiento_de_grupo_util(columna, posicion, fundaciones):
        """
        Indica si mover el grupo que empieza en 'posicion' sirve para algo
        (no es solo pasar cartas de un lado a otro). Es útil si:
            a) Es la primera carta boca arriba de la columna y debajo hay una
               carta boca abajo que se destaparía.
            b) Es la primera carta de la columna (la vaciaría) y no es un Rey
               (un Rey en el fondo ya está en el mejor lugar posible).
            c) La carta de encima del grupo quedaría libre y puede subir a una
               fundación.
        No revisa a dónde va el grupo: eso lo hace puede_mover_grupo.

        Recibe:
            columna (ListaDoble), posicion (int), fundaciones (las 4 Pilas).
        Devuelve:
            True si el movimiento es útil.
        Complejidad: O(n).
        """
        if posicion == 0:
            return columna.obtener(0).valor != REY
        de_encima = columna.obtener(posicion - 1)
        if not de_encima.boca_arriba:
            return True
        return Reglas._va_a_alguna_fundacion(de_encima, fundaciones)

    @staticmethod
    def hay_movimientos_posibles(columnas, fundaciones, mazo):
        """
        Revisa si queda al menos un movimiento ÚTIL. Si no queda ninguno,
        el jugador perdió.

        Se considera útil:
            1. Cualquier carta del mazo de robo que pueda ir a una columna o a
               una fundación. (Robando de 1 en 1 el mazo da vueltas sin
               límite, así que todas sus cartas se pueden alcanzar.)
            2. La carta visible de una columna que pueda subir a una fundación.
            3. Mover un grupo de una columna a otra cuando el movimiento es
               útil (ver es_movimiento_de_grupo_util): destapa una carta,
               vacía una columna o libera una carta para la fundación. Pasar
               cartas de un lado a otro sin ganar nada NO cuenta.

        Nota: el jugador siempre puede rendirse si ve que no avanza.

        Recibe:
            columnas: las 7 columnas (ListaDoble).
            fundaciones: las 4 fundaciones (Pila).
            mazo (ListaCircular): el mazo de robo.
        Devuelve:
            True si queda algún movimiento útil, False si no (derrota).
        Complejidad: O(N), con N = cartas en juego (máximo 52).
        """
        # 1. Cartas del mazo de robo
        for carta in mazo.recorrer():
            # Se evalúa una copia boca arriba, sin modificar la carta real del mazo
            visible = Carta(carta.valor, carta.palo, boca_arriba=True)
            if (Reglas._va_a_alguna_fundacion(visible, fundaciones)
                    or Reglas._va_a_alguna_columna(visible, columnas)):
                return True

        for columna in columnas:
            if columna.esta_vacia():
                continue
            # 2. Carta visible de la columna hacia una fundación
            if Reglas._va_a_alguna_fundacion(columna.ver_final(), fundaciones):
                return True
            # 3. Grupos útiles hacia otras columnas
            posicion = 0
            for carta in columna.recorrer_adelante():
                if carta.boca_arriba and Reglas.es_escalera_valida(columna, posicion) \
                        and Reglas.es_movimiento_de_grupo_util(columna, posicion, fundaciones) \
                        and Reglas._va_a_alguna_columna(carta, columnas, excepto=columna):
                    return True
                posicion += 1
        return False
