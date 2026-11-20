"""
Módulo: baraja.py
Clase Baraja: crea las 52 cartas, las baraja y las entrega en una Pila.

DISEÑO
------
La baraja es una FÁBRICA: no es una estructura de datos, sino la clase que
produce las cartas para cada partida nueva usando las estructuras propias.


ALGORITMO DE BARAJADO (inserción en posición aleatoria)
-------------------------------------------------------
    1. Se crean las 52 cartas en orden (palo por palo, del As al Rey).
    2. Se van tomando una por una e insertando en una ListaDoble en una
       posición ALEATORIA entre 0 y el tamaño actual de la lista.
       Ejemplo con 3 cartas:
           insertar A en 0      -> [A]
           insertar B en 0 o 1  -> [B, A]      (salió 0)
           insertar C en 0,1,2  -> [B, C, A]   (salió 1)
    3. Se recorre la ListaDoble y se apilan las cartas en una Pila, que es
       el mazo desde donde se reparte.

"""

import random

from estructuras.lista_doble import ListaDoble
from estructuras.pila import Pila
from modelo.carta import Carta, PALOS, AS, REY

TOTAL_CARTAS = 52


class Baraja:
    """
    Fábrica de cartas para una partida.

    Atributos:
        semilla (int | None): semilla del azar; None = barajado distinto cada vez.
        _azar (random.Random): generador de números aleatorios propio.
    """

    def __init__(self, semilla=None):
        """
        Prepara la baraja.

        Recibe:
            semilla (int | None): opcional, para repetir el mismo barajado.
        Devuelve: nada.
        """
        self.semilla = semilla
        self._azar = random.Random(semilla)

    def crear_ordenada(self):
        """
        Crea las 52 cartas boca abajo y en orden: Picas, Corazones,
        Diamantes y Tréboles, cada palo del As al Rey.

        Recibe: nada.
        Devuelve:
            ListaDoble con las 52 cartas ordenadas.
        """
        cartas = ListaDoble()
        for palo in PALOS:
            for valor in range(AS, REY + 1):
                cartas.insertar_final(Carta(valor, palo))
        return cartas

    def barajar(self, cartas):
        """
        Baraja las cartas insertando cada una en una posición aleatoria de
        una ListaDoble nueva. La lista recibida queda vacía.

        Recibe:
            cartas (ListaDoble): las cartas a barajar.
        Devuelve:
            ListaDoble con las mismas cartas en orden aleatorio.
        """
        barajada = ListaDoble()
        while not cartas.esta_vacia():
            carta = cartas.eliminar_inicio()
            posicion = self._azar.randint(0, barajada.tamano())
            barajada.insertar_en_posicion(posicion, carta)
        return barajada

    def generar_mazo(self):
        """
        Crea, baraja y entrega las 52 cartas en una Pila lista para repartir.
        Todas las cartas quedan boca abajo.

        Recibe: nada.
        Devuelve:
            Pila con las 52 cartas barajadas (el tope es la primera en repartirse).
        Complejidad: O(n²).
        """
        barajada = self.barajar(self.crear_ordenada())
        mazo = Pila()
        for carta in barajada.recorrer_adelante():
            mazo.apilar(carta)
        return mazo
