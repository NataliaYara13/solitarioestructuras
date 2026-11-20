"""
Módulo: nodo_doble.py
Clase NodoDoble: nodo con enlaces hacia atrás y hacia adelante.

TEORÍA
------
Es un nodo con DOS referencias: al nodo anterior y al siguiente.
Gracias a eso, desde cualquier nodo se puede avanzar o retroceder.

Ventajas frente al Nodo simple:
    - Se puede recorrer la lista en ambos sentidos.
    - Si ya se tiene la referencia a un nodo, se puede quitar o cortar la
      lista en ese punto en O(1), porque se conoce su vecino de atrás.
Desventajas:
    - Usa una referencia más por nodo (más memoria).
    - Cada operación actualiza más enlaces (más cuidado al programar).

Regla de oro: para unir A con B (A antes que B) siempre son DOS asignaciones:
    A.siguiente = B   y   B.anterior = A

Representación:
    None <-[ anterior | dato | siguiente ]<==>[ anterior | dato | siguiente ]-> None

Usado por: ListaDoble.

COMPLEJIDAD
-----------
| Operación       | Complejidad |
|-----------------|-------------|
| Crear nodo      | O(1)        |
| Ir al anterior  | O(1)        |
| Ir al siguiente | O(1)        |
"""


class NodoDoble:
    """
    Nodo con un dato y dos referencias: anterior y siguiente.

    Atributos:
        dato: el valor que guarda el nodo.
        anterior (NodoDoble | None): referencia al nodo de atrás.
        siguiente (NodoDoble | None): referencia al nodo de adelante.
    """

    def __init__(self, dato):
        """
        Crea un nodo doble suelto (sin enlazar).

        Recibe:
            dato: el valor a guardar.
        Devuelve:
            Nada (es el constructor).
        Complejidad: O(1).
        """
        self.dato = dato
        self.anterior = None
        self.siguiente = None

    def __repr__(self):
        """
        Representación en texto del nodo, útil para depurar.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "NodoDoble(5)".
        """
        return f"NodoDoble({self.dato!r})"
