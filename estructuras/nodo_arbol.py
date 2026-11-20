"""
Módulo: nodo_arbol.py
Clase NodoArbol: nodo de un árbol binario.

TEORÍA
------
Guarda un dato y DOS referencias a sus hijos: izquierdo y derecho.
En un Árbol Binario de Búsqueda (BST):
    - En el subárbol IZQUIERDO van los datos MENORES que el del nodo.
    - En el subárbol DERECHO van los datos MAYORES O IGUALES.

Vocabulario:
    - Raíz: el nodo de arriba, no tiene padre.
    - Hoja: nodo sin hijos (izquierdo y derecho son None).
    - Nodo interno: tiene al menos un hijo.
    - Altura: cantidad de niveles del camino más largo de la raíz a una hoja.
    - Subárbol: un nodo con todos sus descendientes.

Representación:
                 [ 500 ]
                /       \\
           [ 320 ]     [ 780 ]
           /    \\           \\
       [ 150 ] [ 410 ]     [ 900 ]

Diferencia con NodoDoble: ambos tienen dos referencias, pero el doble apunta
a vecinos en una LÍNEA y el de árbol apunta a dos HIJOS (ramas).

Usado por: Arbol (BST de mejores puntajes).

COMPLEJIDAD
-----------
| Operación        | Complejidad |
|------------------|-------------|
| Crear nodo       | O(1)        |
| Ir a un hijo     | O(1)        |
| Saber si es hoja | O(1)        |
"""


class NodoArbol:
    """
    Nodo de árbol binario con un dato y dos hijos.

    Atributos:
        dato: el valor que guarda el nodo (en el juego, un Puntaje).
        izquierdo (NodoArbol | None): hijo con datos menores.
        derecho (NodoArbol | None): hijo con datos mayores o iguales.
    """

    def __init__(self, dato):
        """
        Crea un nodo sin hijos (nace como hoja).

        Recibe:
            dato: el valor a guardar.
        Devuelve:
            Nada (es el constructor).
        Complejidad: O(1).
        """
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

    def es_hoja(self):
        """
        Indica si el nodo no tiene hijos.

        Recibe: nada.
        Devuelve:
            True si izquierdo y derecho son None, False si no.
        Complejidad: O(1).
        """
        return self.izquierdo is None and self.derecho is None

    def __repr__(self):
        """
        Representación en texto del nodo, útil para depurar.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "NodoArbol(500)".
        """
        return f"NodoArbol({self.dato!r})"
