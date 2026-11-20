"""
Módulo: pila.py
Clase Pila: implementación propia de una pila enlazada (sin listas de Python).

TEORÍA
------
Una pila es una estructura LIFO (Last In, First Out): el ÚLTIMO elemento
que entra es el PRIMERO que sale. Como una pila de platos: solo se pone y
se quita por arriba (el TOPE).

Implementación enlazada:
    - 'tope' apunta al nodo de arriba.
    - Cada nodo apunta (con 'siguiente') al que está DEBAJO de él.
    - El nodo del fondo apunta a None.
Así, apilar y desapilar solo tocan el tope: no hay que recorrer nada.

Representación:
    tope
     |
     v
    [ 3♠ | o ]--->[ 2♠ | o ]--->[ A♠ | None ]
     (arriba)                     (fondo)

USO EN EL JUEGO
---------------
    - 4 fundaciones: las cartas suben del As al Rey y solo se usa la de arriba.
    - Descarte: la carta robada queda encima y solo esa se puede jugar.
    - Deshacer: cada jugada se apila; deshacer = desapilar la última (LIFO).

COMPLEJIDAD
-----------
| Operación  | Complejidad | Por qué                      |
|------------|-------------|------------------------------|
| apilar     | O(1)        | Solo cambia el tope          |
| desapilar  | O(1)        | Solo cambia el tope          |
| ver_tope   | O(1)        | Lee el tope                  |
| esta_vacia | O(1)        | Compara el tope con None     |
| tamano     | O(1)        | Se lleva un contador         |
| recorrer   | O(n)        | Visita todos los nodos       |
| vaciar     | O(1)        | Suelta la referencia al tope |
"""

from estructuras.nodo import Nodo


class Pila:
    """
    Pila enlazada genérica: puede guardar cualquier tipo de dato.

    Atributos:
        tope (Nodo | None): nodo de arriba, o None si la pila está vacía.
        _tamano (int): cantidad de elementos (contador interno).
    """

    def __init__(self):
        """
        Crea una pila vacía.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.tope = None
        self._tamano = 0

    def apilar(self, dato):
        """
        Pone un dato encima de la pila.

        Pasos:
            1. Crear un nodo con el dato.
            2. El nuevo nodo apunta al tope actual (si está vacía, a None).
            3. El tope pasa a ser el nuevo nodo.

        Recibe:
            dato: el valor a apilar.
        Devuelve:
            Nada.
        Complejidad: O(1).
        """
        nuevo = Nodo(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self._tamano += 1

    def desapilar(self):
        """
        Saca y devuelve el dato del tope.

        Pasos:
            1. Si está vacía, lanzar error.
            2. Guardar el dato del tope.
            3. El tope pasa a ser el nodo de abajo.

        Recibe: nada.
        Devuelve:
            El dato que estaba en el tope.
        Lanza:
            IndexError si la pila está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía")
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self._tamano -= 1
        return dato

    def ver_tope(self):
        """
        Devuelve el dato del tope SIN sacarlo.

        Recibe: nada.
        Devuelve:
            El dato del tope, o None si la pila está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            return None
        return self.tope.dato

    def esta_vacia(self):
        """
        Indica si la pila no tiene elementos.

        Recibe: nada.
        Devuelve:
            True si está vacía, False si no.
        Complejidad: O(1).
        """
        return self.tope is None

    def tamano(self):
        """
        Devuelve la cantidad de elementos.

        Recibe: nada.
        Devuelve:
            int con la cantidad de elementos.
        Complejidad: O(1), porque se lleva un contador.
        """
        return self._tamano

    def recorrer(self):
        """
        Recorre la pila del tope al fondo SIN modificarla.
        Es un generador: se usa como  'for dato in pila.recorrer():'.

        Recibe: nada.
        Devuelve:
            Cada dato, uno por uno, del tope hacia el fondo.
        Complejidad: O(n).
        """
        actual = self.tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def vaciar(self):
        """
        Elimina todos los elementos.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1); el recolector de basura libera los nodos.
        """
        self.tope = None
        self._tamano = 0

    def __len__(self):
        """Permite usar len(pila). Devuelve el tamaño. O(1)."""
        return self._tamano

    def __str__(self):
        """
        Texto de la pila del tope al fondo, por ejemplo "[3, 2, 1]".

        Recibe: nada.
        Devuelve:
            str.
        """
        return "[" + ", ".join(str(d) for d in self.recorrer()) + "]"
