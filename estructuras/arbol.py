"""
Módulo: arbol.py
Clase Arbol: Árbol Binario de Búsqueda (BST) propio, implementado con recursión.

TEORÍA
------
Un árbol binario es una estructura jerárquica: cada nodo tiene como máximo
dos hijos. En un Árbol Binario de BÚSQUEDA se cumple siempre, para cada nodo:
    - todo lo del subárbol IZQUIERDO es MENOR que el nodo, y
    - todo lo del subárbol DERECHO es MAYOR O IGUAL (los empates van a la derecha).

Gracias a esa regla, para buscar no hace falta revisar todo: en cada nodo
se decide ir a la izquierda o a la derecha, descartando la mitad.

¿Con qué se compara? Con una CLAVE. El árbol recibe una función 'clave'
que dice qué parte del dato se usa para ordenar. Ejemplo:
    Arbol(clave=lambda p: p.puntos)  -> ordena objetos Puntaje por sus puntos.
Si no se da función, se compara el dato tal cual (números, textos...).

Recorridos (los tres son en profundidad):
    - Inorden   (izquierdo, RAÍZ, derecho)  -> datos ORDENADOS de menor a mayor.
    - Preorden  (RAÍZ, izquierdo, derecho)  -> sirve para copiar o guardar el
      árbol: al reinsertar en ese orden se obtiene el mismo árbol.
    - Posorden  (izquierdo, derecho, RAÍZ)  -> procesa los hijos antes que el
      padre (por ejemplo, para liberar o contar).

Ejemplo, insertando 500, 320, 780, 150, 410, 900:
                 500
                /    \\
             320      780
            /   \\        \\
          150   410      900
    Inorden:  150 320 410 500 780 900
    Preorden: 500 320 150 410 780 900
    Posorden: 150 410 320 900 780 500

Eliminar un nodo tiene 3 casos:
    1. Es hoja: simplemente se quita.
    2. Tiene un solo hijo: el hijo ocupa su lugar.
    3. Tiene dos hijos: se reemplaza su dato por el del SUCESOR INORDEN
       (el menor del subárbol derecho) y luego se elimina ese sucesor,
       que nunca tiene hijo izquierdo (cae en el caso 1 o 2).

USO EN EL JUEGO
---------------
    RANKING DE MEJORES PUNTAJES: cada partida terminada crea un Puntaje que
    se inserta en el árbol ordenado por puntos. Para mostrar el ranking de
    mayor a menor se usa el inorden inverso (derecho, raíz, izquierdo).
    Para dejar solo los 10 mejores se elimina el mínimo cuando sobran.

COMPLEJIDAD (h = altura del árbol)
----------------------------------
| Operación                 | Promedio  | Peor caso | Nota                     |
|---------------------------|-----------|-----------|--------------------------|
| insertar                  | O(log n)  | O(n)      | Recorre un camino        |
| buscar                    | O(log n)  | O(n)      | Recorre un camino        |
| eliminar                  | O(log n)  | O(n)      | Recorre un camino        |
| minimo / maximo           | O(log n)  | O(n)      | Extremo izq. / der.      |
| inorden/preorden/posorden | O(n)      | O(n)      | Visita todos los nodos   |
| altura                    | O(n)      | O(n)      | Visita todos los nodos   |
| tamano / esta_vacia       | O(1)      | O(1)      | Contador                 |

En realidad todas las operaciones de un camino son O(h). Si el árbol queda
equilibrado, h ≈ log n. El peor caso ocurre si los datos llegan ya ordenados
(por ejemplo 1, 2, 3, 4...): el árbol se vuelve una "línea" y h = n.
"""

from estructuras.nodo_arbol import NodoArbol


def _identidad(dato):
    """
    Función clave por defecto: devuelve el mismo dato.

    Recibe:
        dato: cualquier valor comparable.
    Devuelve:
        El mismo dato.
    """
    return dato


class Arbol:
    """
    Árbol Binario de Búsqueda genérico.

    Atributos:
        raiz (NodoArbol | None): nodo de arriba, o None si está vacío.
        clave (función): extrae del dato el valor con el que se ordena.
        _tamano (int): cantidad de nodos.
    """

    def __init__(self, clave=None):
        """
        Crea un árbol vacío.

        Recibe:
            clave (función | None): función que recibe un dato y devuelve el
                valor para ordenar. Si es None, se compara el dato tal cual.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.raiz = None
        self.clave = clave if clave is not None else _identidad
        self._tamano = 0

    # ------------------------------------------------------------------
    # Consultas básicas
    # ------------------------------------------------------------------
    def esta_vacio(self):
        """
        Indica si el árbol no tiene nodos.

        Recibe: nada.
        Devuelve:
            True si está vacío, False si no.
        Complejidad: O(1).
        """
        return self.raiz is None

    def tamano(self):
        """
        Devuelve la cantidad de nodos.

        Recibe: nada.
        Devuelve:
            int.
        Complejidad: O(1).
        """
        return self._tamano

    # ------------------------------------------------------------------
    # Insertar
    # ------------------------------------------------------------------
    def insertar(self, dato):
        """
        Inserta un dato respetando la regla del BST.

        Recibe:
            dato: el valor a insertar.
        Devuelve: nada.
        Complejidad: O(h).
        """
        self.raiz = self._insertar(self.raiz, dato)
        self._tamano += 1

    def _insertar(self, nodo, dato):
        """
        Método recursivo de inserción.
        Caso base: si el nodo es None, ahí va el nuevo nodo.
        Caso recursivo: bajar a la izquierda si la clave es menor, si no a la
        derecha; luego devolver el mismo nodo para mantener el enlace.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol actual.
            dato: el valor a insertar.
        Devuelve:
            NodoArbol: la raíz del subárbol ya con el dato insertado.
        Complejidad: O(h).
        """
        if nodo is None:
            return NodoArbol(dato)
        if self.clave(dato) < self.clave(nodo.dato):
            nodo.izquierdo = self._insertar(nodo.izquierdo, dato)
        else:
            nodo.derecho = self._insertar(nodo.derecho, dato)
        return nodo

    # ------------------------------------------------------------------
    # Buscar
    # ------------------------------------------------------------------
    def buscar(self, valor_clave):
        """
        Busca un dato por su clave (por ejemplo, unos puntos).

        Recibe:
            valor_clave: el valor de la clave a buscar.
        Devuelve:
            El primer dato encontrado con esa clave, o None si no existe.
        Complejidad: O(h).
        """
        nodo = self._buscar(self.raiz, valor_clave)
        return None if nodo is None else nodo.dato

    def _buscar(self, nodo, valor_clave):
        """
        Método recursivo de búsqueda.
        Casos base: nodo None (no está) o clave igual (encontrado).
        Caso recursivo: ir a la izquierda si es menor, si no a la derecha.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol actual.
            valor_clave: lo que se busca.
        Devuelve:
            NodoArbol encontrado, o None.
        Complejidad: O(h).
        """
        if nodo is None:
            return None
        clave_nodo = self.clave(nodo.dato)
        if valor_clave == clave_nodo:
            return nodo
        if valor_clave < clave_nodo:
            return self._buscar(nodo.izquierdo, valor_clave)
        return self._buscar(nodo.derecho, valor_clave)

    def contiene(self, valor_clave):
        """
        Indica si existe algún dato con esa clave.

        Recibe:
            valor_clave: el valor de la clave a buscar.
        Devuelve:
            True si existe, False si no.
        Complejidad: O(h).
        """
        return self._buscar(self.raiz, valor_clave) is not None

    # ------------------------------------------------------------------
    # Eliminar
    # ------------------------------------------------------------------
    def eliminar(self, valor_clave):
        """
        Elimina UN dato que tenga esa clave (el primero que se encuentre).

        Recibe:
            valor_clave: el valor de la clave a eliminar.
        Devuelve:
            True si se eliminó, False si no existía.
        Complejidad: O(h).
        """
        if not self.contiene(valor_clave):
            return False
        self.raiz = self._eliminar(self.raiz, valor_clave)
        self._tamano -= 1
        return True

    def _eliminar(self, nodo, valor_clave):
        """
        Método recursivo de eliminación (los 3 casos).

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol actual.
            valor_clave: la clave a eliminar.
        Devuelve:
            NodoArbol | None: la nueva raíz del subárbol.
        Complejidad: O(h).
        """
        if nodo is None:
            return None
        clave_nodo = self.clave(nodo.dato)
        if valor_clave < clave_nodo:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, valor_clave)
            return nodo
        if valor_clave > clave_nodo:
            nodo.derecho = self._eliminar(nodo.derecho, valor_clave)
            return nodo

        # Encontrado: valor_clave == clave_nodo
        # Caso 1 y 2: sin hijo izquierdo o sin hijo derecho
        if nodo.izquierdo is None:
            return nodo.derecho
        if nodo.derecho is None:
            return nodo.izquierdo
        # Caso 3: dos hijos -> copiar el sucesor inorden y quitarlo
        sucesor = self._nodo_minimo(nodo.derecho)
        nodo.dato = sucesor.dato
        nodo.derecho = self._eliminar_minimo(nodo.derecho)
        return nodo

    def _eliminar_minimo(self, nodo):
        """
        Método recursivo: quita el nodo más a la izquierda de un subárbol.
        Ese nodo nunca tiene hijo izquierdo, así que su hijo derecho
        (o None) toma su lugar.

        Recibe:
            nodo (NodoArbol): raíz del subárbol (no vacío).
        Devuelve:
            NodoArbol | None: la nueva raíz del subárbol.
        Complejidad: O(h).
        """
        if nodo.izquierdo is None:
            return nodo.derecho
        nodo.izquierdo = self._eliminar_minimo(nodo.izquierdo)
        return nodo

    # ------------------------------------------------------------------
    # Mínimo y máximo
    # ------------------------------------------------------------------
    def _nodo_minimo(self, nodo):
        """
        Método interno: baja siempre a la izquierda hasta el final.

        Recibe:
            nodo (NodoArbol): raíz de un subárbol no vacío.
        Devuelve:
            NodoArbol con la menor clave del subárbol.
        Complejidad: O(h).
        """
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def minimo(self):
        """
        Devuelve el dato con la menor clave.

        Recibe: nada.
        Devuelve:
            El dato mínimo, o None si el árbol está vacío.
        Complejidad: O(h).
        """
        return None if self.esta_vacio() else self._nodo_minimo(self.raiz).dato

    def maximo(self):
        """
        Devuelve el dato con la mayor clave (bajando siempre a la derecha).

        Recibe: nada.
        Devuelve:
            El dato máximo, o None si el árbol está vacío.
        Complejidad: O(h).
        """
        if self.esta_vacio():
            return None
        nodo = self.raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.dato

    # ------------------------------------------------------------------
    # Recorridos (generadores recursivos)
    # ------------------------------------------------------------------
    def inorden(self):
        """
        Recorrido inorden (izquierdo, raíz, derecho): datos de menor a mayor.

        Recibe: nada.
        Devuelve:
            Generador con los datos en orden ascendente.
        Complejidad: O(n).
        """
        yield from self._inorden(self.raiz)

    def _inorden(self, nodo):
        """
        Método recursivo del inorden.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol.
        Devuelve:
            Generador con los datos del subárbol en inorden.
        """
        if nodo is not None:
            yield from self._inorden(nodo.izquierdo)
            yield nodo.dato
            yield from self._inorden(nodo.derecho)

    def preorden(self):
        """
        Recorrido preorden (raíz, izquierdo, derecho).

        Recibe: nada.
        Devuelve:
            Generador con los datos en preorden.
        Complejidad: O(n).
        """
        yield from self._preorden(self.raiz)

    def _preorden(self, nodo):
        """
        Método recursivo del preorden.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol.
        Devuelve:
            Generador con los datos del subárbol en preorden.
        """
        if nodo is not None:
            yield nodo.dato
            yield from self._preorden(nodo.izquierdo)
            yield from self._preorden(nodo.derecho)

    def posorden(self):
        """
        Recorrido posorden (izquierdo, derecho, raíz).

        Recibe: nada.
        Devuelve:
            Generador con los datos en posorden.
        Complejidad: O(n).
        """
        yield from self._posorden(self.raiz)

    def _posorden(self, nodo):
        """
        Método recursivo del posorden.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol.
        Devuelve:
            Generador con los datos del subárbol en posorden.
        """
        if nodo is not None:
            yield from self._posorden(nodo.izquierdo)
            yield from self._posorden(nodo.derecho)
            yield nodo.dato

    def inorden_inverso(self):
        """
        Recorrido inorden inverso (derecho, raíz, izquierdo): de mayor a menor.
        En el juego: mostrar el ranking empezando por el mejor puntaje.

        Recibe: nada.
        Devuelve:
            Generador con los datos en orden descendente.
        Complejidad: O(n).
        """
        yield from self._inorden_inverso(self.raiz)

    def _inorden_inverso(self, nodo):
        """
        Método recursivo del inorden inverso.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol.
        Devuelve:
            Generador con los datos del subárbol de mayor a menor.
        """
        if nodo is not None:
            yield from self._inorden_inverso(nodo.derecho)
            yield nodo.dato
            yield from self._inorden_inverso(nodo.izquierdo)

    # ------------------------------------------------------------------
    # Altura y utilidades
    # ------------------------------------------------------------------
    def altura(self):
        """
        Devuelve la altura del árbol (cantidad de niveles).
        Árbol vacío = 0; solo la raíz = 1.

        Recibe: nada.
        Devuelve:
            int.
        Complejidad: O(n).
        """
        return self._altura(self.raiz)

    def _altura(self, nodo):
        """
        Método recursivo: 1 + la mayor altura entre los dos hijos.

        Recibe:
            nodo (NodoArbol | None): raíz del subárbol.
        Devuelve:
            int con la altura del subárbol.
        """
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def vaciar(self):
        """
        Elimina todos los nodos.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.raiz = None
        self._tamano = 0

    def __len__(self):
        """Permite usar len(arbol). Devuelve el tamaño. O(1)."""
        return self._tamano

    def __str__(self):
        """
        Texto del árbol en inorden, por ejemplo "[150, 320, 500]".

        Recibe: nada.
        Devuelve:
            str.
        """
        return "[" + ", ".join(str(d) for d in self.inorden()) + "]"
