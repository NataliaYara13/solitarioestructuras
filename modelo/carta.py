"""
Módulo: carta.py
Clase Carta: una carta de la baraja francesa (52 cartas).

DISEÑO
------
La carta solo guarda DATOS: qué carta es (valor y palo) y si está boca
arriba. NO contiene reglas del juego (eso lo decide la clase Reglas) y NO
sabe dónde está (eso lo saben las estructuras que la contienen: columnas,
mazo de robo, fundaciones).

La baraja francesa tiene:
    - 4 palos: Picas ♠ y Tréboles ♣ (negros), Corazones ♥ y Diamantes ♦ (rojos).
    - 13 valores por palo: As (1), del 2 al 10, Jota (11), Reina (12), Rey (13).
    - 4 x 13 = 52 cartas.

El valor se guarda como NÚMERO (1 a 13) y no como texto, porque las reglas
comparan valores ("¿vale uno menos?") y eso es directo con números.
Para mostrarla se convierte: 1 -> "A", 11 -> "J", 12 -> "Q", 13 -> "K".

"""

# ------------------------------------------------------------------------------
# Constantes de la baraja (las usan también Reglas, Baraja y la vista)
# ------------------------------------------------------------------------------
PICAS = "P"
CORAZONES = "C"
DIAMANTES = "D"
TREBOLES = "T"

PALOS = (PICAS, CORAZONES, DIAMANTES, TREBOLES)
PALOS_ROJOS = (CORAZONES, DIAMANTES)

SIMBOLOS = {PICAS: "♠", CORAZONES: "♥", DIAMANTES: "♦", TREBOLES: "♣"}
NOMBRES_PALO = {PICAS: "Picas", CORAZONES: "Corazones",
                DIAMANTES: "Diamantes", TREBOLES: "Tréboles"}

AS = 1
JOTA = 11
REINA = 12
REY = 13

TEXTO_VALOR = {AS: "A", JOTA: "J", REINA: "Q", REY: "K"}
NOMBRES_VALOR = {AS: "As", JOTA: "Jota", REINA: "Reina", REY: "Rey"}


class Carta:
    """
    Representa una carta de la baraja.

    Atributos:
        valor (int): de 1 (As) a 13 (Rey).
        palo (str): "P", "C", "D" o "T".
        boca_arriba (bool): True si la carta se ve de frente.
    """

    def __init__(self, valor, palo, boca_arriba=False):
        """
        Crea una carta validando sus datos, para que nunca exista una
        carta inválida dentro del juego.

        Recibe:
            valor (int): de 1 a 13.
            palo (str): uno de PALOS ("P", "C", "D", "T").
            boca_arriba (bool): opcional, por defecto False (boca abajo).
        Devuelve:
            Nada (es el constructor).
        Lanza:
            ValueError si el valor o el palo no son válidos.
        """
        if not isinstance(valor, int) or isinstance(valor, bool) or not AS <= valor <= REY:
            raise ValueError(f"Valor de carta inválido: {valor}")
        if palo not in PALOS:
            raise ValueError(f"Palo de carta inválido: {palo}")
        self.valor = valor
        self.palo = palo
        self.boca_arriba = boca_arriba

    # ------------------------------------------------------------------
    # Color
    # ------------------------------------------------------------------
    def es_roja(self):
        """
        Indica si la carta es roja (Corazones o Diamantes).

        Recibe: nada.
        Devuelve:
            True si es roja, False si es negra.
        """
        return self.palo in PALOS_ROJOS

    def color(self):
        """
        Devuelve el color de la carta como texto.

        Recibe: nada.
        Devuelve:
            str: "rojo" o "negro".
        """
        return "rojo" if self.es_roja() else "negro"

    # ------------------------------------------------------------------
    # Estado (boca arriba / boca abajo)
    # ------------------------------------------------------------------
    def voltear(self):
        """
        Cambia la carta de boca abajo a boca arriba, o al revés.

        Recibe: nada.
        Devuelve: nada.
        """
        self.boca_arriba = not self.boca_arriba

    def destapar(self):
        """
        Pone la carta boca arriba (si ya lo estaba, no cambia nada).

        Recibe: nada.
        Devuelve: nada.
        """
        self.boca_arriba = True

    def tapar(self):
        """
        Pone la carta boca abajo (si ya lo estaba, no cambia nada).

        Recibe: nada.
        Devuelve: nada.
        """
        self.boca_arriba = False

    # ------------------------------------------------------------------
    # Textos para mostrar
    # ------------------------------------------------------------------
    def texto_valor(self):
        """
        Devuelve el valor como se escribe en la esquina de la carta.

        Recibe: nada.
        Devuelve:
            str: "A", "2".."10", "J", "Q" o "K".
        """
        return TEXTO_VALOR.get(self.valor, str(self.valor))

    def simbolo(self):
        """
        Devuelve el símbolo del palo.

        Recibe: nada.
        Devuelve:
            str: "♠", "♥", "♦" o "♣".
        """
        return SIMBOLOS[self.palo]

    def nombre(self):
        """
        Devuelve el nombre completo de la carta, útil para mensajes.
        Ejemplo: "Rey de Picas", "7 de Corazones".

        Recibe: nada.
        Devuelve:
            str.
        """
        valor = NOMBRES_VALOR.get(self.valor, str(self.valor))
        return f"{valor} de {NOMBRES_PALO[self.palo]}"

    # ------------------------------------------------------------------
    # Métodos especiales de Python
    # ------------------------------------------------------------------
    def __eq__(self, otra):
        """
        Dos cartas son iguales si tienen el mismo valor y el mismo palo
        (no importa si están boca arriba o boca abajo).
        Lo usan los métodos 'buscar' y 'eliminar' de las estructuras.

        Recibe:
            otra: el objeto a comparar.
        Devuelve:
            True si son la misma carta, False si no.
        """
        return isinstance(otra, Carta) and self.valor == otra.valor and self.palo == otra.palo

    def __hash__(self):
        """
        Necesario en Python cuando se define __eq__.
        Devuelve un número que identifica a la carta por valor y palo.

        Recibe: nada.
        Devuelve:
            int.
        """
        return hash((self.valor, self.palo))

    def __str__(self):
        """
        Texto corto de la carta. Si está boca abajo no revela cuál es.
        Ejemplos: "10♥", "K♠", "[#]".

        Recibe: nada.
        Devuelve:
            str.
        """
        if not self.boca_arriba:
            return "[#]"
        return f"{self.texto_valor()}{self.simbolo()}"

    def __repr__(self):
        """
        Texto para depurar: siempre muestra la carta, aunque esté boca abajo.
        Ejemplo: "Carta(10♥, abajo)".

        Recibe: nada.
        Devuelve:
            str.
        """
        estado = "arriba" if self.boca_arriba else "abajo"
        return f"Carta({self.texto_valor()}{self.simbolo()}, {estado})"
