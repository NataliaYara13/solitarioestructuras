"""
Módulo: cola.py
Clase Cola: implementación propia de una cola enlazada (sin listas de Python).

TEORÍA
------
Una cola es una estructura FIFO (First In, First Out): el PRIMERO que entra
es el PRIMERO que sale. Como la fila de un banco: se entra por el FINAL y se
sale por el FRENTE.

Implementación enlazada con DOS referencias:
    - 'frente' apunta al primer nodo (el próximo en salir).
    - 'final'  apunta al último nodo (donde entra el siguiente).
Tener 'final' permite encolar en O(1) sin recorrer toda la cola.

Representación:
    frente                               final
      |                                    |
      v                                    v
    [ J1 | o ]--->[ J2 | o ]--->[ J3 | None ]
    (sale primero)             (entró último)

USO EN EL JUEGO
---------------
    Registro de jugadas para REPETIR la partida: cada jugada se encola en
    orden; al terminar, la repetición las desencola y las reproduce en el
    mismo orden en que ocurrieron (FIFO).

COMPLEJIDAD
-----------
| Operación  | Complejidad | Por qué                          |
|------------|-------------|----------------------------------|
| encolar    | O(1)        | Gracias a la referencia 'final'  |
| desencolar | O(1)        | Solo cambia el frente            |
| ver_frente | O(1)        | Lee el frente                    |
| esta_vacia | O(1)        | Compara el frente con None       |
| tamano     | O(1)        | Se lleva un contador             |
| recorrer   | O(n)        | Visita todos los nodos           |
| vaciar     | O(1)        | Suelta las referencias           |
"""

from estructuras.nodo import Nodo


class Cola:
    """
    Cola enlazada genérica: puede guardar cualquier tipo de dato.

    Atributos:
        frente (Nodo | None): primer nodo (el próximo en salir).
        final (Nodo | None): último nodo (el que entró de último).
        _tamano (int): cantidad de elementos.
    """

    def __init__(self):
        """
        Crea una cola vacía.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.frente = None
        self.final = None
        self._tamano = 0

    def encolar(self, dato):
        """
        Agrega un dato al final de la cola.

        Pasos:
            1. Crear un nodo con el dato.
            2. Si la cola está vacía, frente y final apuntan al nuevo.
            3. Si no, el final actual apunta al nuevo y el final se mueve.

        Recibe:
            dato: el valor a encolar.
        Devuelve:
            Nada.
        Complejidad: O(1).
        """
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.frente = nuevo
        else:
            self.final.siguiente = nuevo
        self.final = nuevo
        self._tamano += 1

    def desencolar(self):
        """
        Saca y devuelve el dato del frente.

        Pasos:
            1. Si está vacía, lanzar error.
            2. Guardar el dato del frente y mover el frente al siguiente.
            3. Si la cola quedó vacía, el final también debe quedar en None
               (si no, apuntaría a un nodo que ya salió).

        Recibe: nada.
        Devuelve:
            El dato que estaba en el frente.
        Lanza:
            IndexError si la cola está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola está vacía")
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self._tamano -= 1
        return dato

    def ver_frente(self):
        """
        Devuelve el dato del frente SIN sacarlo.

        Recibe: nada.
        Devuelve:
            El dato del frente, o None si la cola está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            return None
        return self.frente.dato

    def esta_vacia(self):
        """
        Indica si la cola no tiene elementos.

        Recibe: nada.
        Devuelve:
            True si está vacía, False si no.
        Complejidad: O(1).
        """
        return self.frente is None

    def tamano(self):
        """
        Devuelve la cantidad de elementos.

        Recibe: nada.
        Devuelve:
            int con la cantidad de elementos.
        Complejidad: O(1).
        """
        return self._tamano

    def recorrer(self):
        """
        Recorre la cola del frente al final SIN modificarla (generador).

        Recibe: nada.
        Devuelve:
            Cada dato, uno por uno, del frente hacia el final.
        Complejidad: O(n).
        """
        actual = self.frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def vaciar(self):
        """
        Elimina todos los elementos.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.frente = None
        self.final = None
        self._tamano = 0

    def __len__(self):
        """Permite usar len(cola). Devuelve el tamaño. O(1)."""
        return self._tamano

    def __str__(self):
        """
        Texto de la cola del frente al final, por ejemplo "[1, 2, 3]".

        Recibe: nada.
        Devuelve:
            str.
        """
        return "[" + ", ".join(str(d) for d in self.recorrer()) + "]"
