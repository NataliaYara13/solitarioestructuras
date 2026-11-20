"""
Módulo: nodo.py
Clase Nodo: la unidad básica de las estructuras enlazadas simples.

TEORÍA
------
Un nodo es una "cajita" que guarda dos cosas:
    - un DATO (cualquier valor: una carta, una jugada, un número...), y
    - una REFERENCIA (puntero) al siguiente nodo.

En Python no hay punteros como en C, pero toda variable que guarda un objeto
es una referencia a ese objeto en memoria. Cuando decimos que
"nodo.siguiente apunta a otro nodo", el atributo guarda esa referencia.

Encadenando nodos se construyen la Pila, la Cola y la Lista circular
SIN usar las listas de Python.

Representación:
    [ dato | siguiente ] ---> [ dato | siguiente ] ---> None

'None' significa que no apunta a nada: es el fin de la cadena.

Usado por: Pila, Cola, ListaCircular.

COMPLEJIDAD
-----------
| Operación      | Complejidad |
|----------------|-------------|
| Crear nodo     | O(1)        |
| Leer dato      | O(1)        |
| Cambiar enlace | O(1)        |
"""


class Nodo:
    """
    Nodo simple con un dato y una referencia al siguiente nodo.

    El nodo NO tiene lógica de inserción ni eliminación: solo almacena.
    Quien enlaza y desenlaza nodos es la estructura que los contiene.

    Atributos:
        dato: el valor que guarda el nodo (de cualquier tipo).
        siguiente (Nodo | None): referencia al nodo que sigue, o None.
    """

    def __init__(self, dato):
        """
        Crea un nodo suelto (sin enlazar).

        Recibe:
            dato: el valor a guardar.
        Devuelve:
            Nada (es el constructor).
        Complejidad: O(1).
        """
        self.dato = dato
        self.siguiente = None

    def __repr__(self):
        """
        Representación en texto del nodo, útil para depurar.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "Nodo(5)".
        """
        return f"Nodo({self.dato!r})"
