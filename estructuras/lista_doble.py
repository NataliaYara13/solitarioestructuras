"""
Módulo: lista_doble.py
Clase ListaDoble: lista doblemente enlazada propia (sin listas de Python).

TEORÍA
------
Es una secuencia de nodos dobles: cada nodo conoce a su anterior y a su
siguiente. La lista guarda referencias a sus dos extremos:
    - 'cabeza' -> primer nodo (posición 0).
    - 'final'  -> último nodo (posición tamaño - 1).
(Se llama 'final' y no 'cola' para no confundirla con la clase Cola.)

A diferencia de la pila y la cola, aquí se puede insertar y eliminar en
CUALQUIER posición y recorrer en AMBOS sentidos.

Representación:
    cabeza                                         final
      |                                              |
      v                                              v
    None<-[ K♠ ]<==>[ Q♥ ]<==>[ J♣ ]<==>[ 10♦ ]->None
           pos 0     pos 1     pos 2     pos 3

USO EN EL JUEGO
---------------
    - Las 7 COLUMNAS: cada una es una ListaDoble de cartas. La cabeza es la
      carta de más atrás y el final es la carta visible que se puede jugar.
      Mover un grupo de cartas = cortar_desde() + concatenar().
    - BARAJADO: la Baraja inserta cada carta en una posición aleatoria con
      insertar_en_posicion(), sin usar random.shuffle.

"""

from estructuras.nodo_doble import NodoDoble


class ListaDoble:
    """
    Lista doblemente enlazada genérica. Las posiciones empiezan en 0.

    Atributos:
        cabeza (NodoDoble | None): primer nodo.
        final (NodoDoble | None): último nodo.
        _tamano (int): cantidad de elementos.
    """

    def __init__(self):
        """
        Crea una lista vacía.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.cabeza = None
        self.final = None
        self._tamano = 0

    # ------------------------------------------------------------------
    # Consultas básicas
    # ------------------------------------------------------------------
    def esta_vacia(self):
        """
        Indica si la lista no tiene elementos.

        Recibe: nada.
        Devuelve:
            True si está vacía, False si no.
        Complejidad: O(1).
        """
        return self.cabeza is None

    def tamano(self):
        """
        Devuelve la cantidad de elementos.

        Recibe: nada.
        Devuelve:
            int.
        Complejidad: O(1).
        """
        return self._tamano

    def ver_inicio(self):
        """
        Devuelve el dato de la cabeza sin quitarlo.

        Recibe: nada.
        Devuelve:
            El dato de la cabeza, o None si está vacía.
        Complejidad: O(1).
        """
        return None if self.esta_vacia() else self.cabeza.dato

    def ver_final(self):
        """
        Devuelve el dato del final sin quitarlo
        (en una columna: la carta visible que se puede jugar).

        Recibe: nada.
        Devuelve:
            El dato del final, o None si está vacía.
        Complejidad: O(1).
        """
        return None if self.esta_vacia() else self.final.dato

    def _nodo_en(self, posicion):
        """
        Método interno: devuelve el NODO que está en una posición.
        Si la posición está en la primera mitad recorre desde la cabeza;
        si está en la segunda mitad, desde el final hacia atrás
        (aprovecha que la lista es doble: hace como máximo n/2 pasos).

        Recibe:
            posicion (int): de 0 a tamaño - 1.
        Devuelve:
            NodoDoble en esa posición.
        Lanza:
            IndexError si la posición no existe.
        Complejidad: O(n).
        """
        if not isinstance(posicion, int) or posicion < 0 or posicion >= self._tamano:
            raise IndexError(f"Posición fuera de rango: {posicion}")
        if posicion < self._tamano // 2:
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
        else:
            actual = self.final
            for _ in range(self._tamano - 1 - posicion):
                actual = actual.anterior
        return actual

    def obtener(self, posicion):
        """
        Devuelve el dato que está en una posición, sin quitarlo.

        Recibe:
            posicion (int): de 0 a tamaño - 1.
        Devuelve:
            El dato en esa posición.
        Lanza:
            IndexError si la posición no existe.
        Complejidad: O(n).
        """
        return self._nodo_en(posicion).dato

    # ------------------------------------------------------------------
    # Inserción
    # ------------------------------------------------------------------
    def insertar_inicio(self, dato):
        """
        Inserta un dato al principio (nueva cabeza).

        Pasos (lista no vacía):
            nuevo.siguiente = cabeza;  cabeza.anterior = nuevo;  cabeza = nuevo

        Recibe:
            dato: el valor a insertar.
        Devuelve: nada.
        Complejidad: O(1).
        """
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.final = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self._tamano += 1

    def insertar_final(self, dato):
        """
        Inserta un dato al final (nuevo final).

        Pasos (lista no vacía):
            nuevo.anterior = final;  final.siguiente = nuevo;  final = nuevo

        Recibe:
            dato: el valor a insertar.
        Devuelve: nada.
        Complejidad: O(1).
        """
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            self.final = nuevo
        else:
            nuevo.anterior = self.final
            self.final.siguiente = nuevo
            self.final = nuevo
        self._tamano += 1

    def insertar_en_posicion(self, posicion, dato):
        """
        Inserta un dato para que quede en la posición indicada.
        Los elementos desde esa posición se corren una hacia adelante.

        Pasos (inserción en medio, antes del nodo 'actual'):
            nuevo.anterior = actual.anterior
            nuevo.siguiente = actual
            actual.anterior.siguiente = nuevo
            actual.anterior = nuevo
        (Son 4 enlaces y el orden importa.)

        Recibe:
            posicion (int): de 0 a tamaño (tamaño = insertar al final).
            dato: el valor a insertar.
        Devuelve: nada.
        Lanza:
            IndexError si la posición no es válida.
        Complejidad: O(n).
        """
        if not isinstance(posicion, int) or posicion < 0 or posicion > self._tamano:
            raise IndexError(f"Posición fuera de rango para insertar: {posicion}")
        if posicion == 0:
            self.insertar_inicio(dato)
        elif posicion == self._tamano:
            self.insertar_final(dato)
        else:
            actual = self._nodo_en(posicion)
            nuevo = NodoDoble(dato)
            nuevo.anterior = actual.anterior
            nuevo.siguiente = actual
            actual.anterior.siguiente = nuevo
            actual.anterior = nuevo
            self._tamano += 1

    # ------------------------------------------------------------------
    # Eliminación
    # ------------------------------------------------------------------
    def _desenlazar(self, nodo):
        """
        Método interno: quita un nodo de la lista ajustando los enlaces.
        Contempla los 4 casos: único nodo, cabeza, final y nodo en medio.

        Recibe:
            nodo (NodoDoble): un nodo que pertenece a esta lista.
        Devuelve:
            El dato del nodo eliminado.
        Complejidad: O(1).
        """
        if nodo.anterior is None:          # es la cabeza
            self.cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente
        if nodo.siguiente is None:         # es el final
            self.final = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior
        nodo.anterior = None
        nodo.siguiente = None
        self._tamano -= 1
        return nodo.dato

    def eliminar_inicio(self):
        """
        Quita y devuelve el primer dato.

        Recibe: nada.
        Devuelve:
            El dato que estaba en la cabeza.
        Lanza:
            IndexError si la lista está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            raise IndexError("No se puede eliminar: la lista está vacía")
        return self._desenlazar(self.cabeza)

    def eliminar_final(self):
        """
        Quita y devuelve el último dato
        (en una columna: tomar la carta visible).

        Recibe: nada.
        Devuelve:
            El dato que estaba al final.
        Lanza:
            IndexError si la lista está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            raise IndexError("No se puede eliminar: la lista está vacía")
        return self._desenlazar(self.final)

    def eliminar_en_posicion(self, posicion):
        """
        Quita y devuelve el dato de una posición.

        Recibe:
            posicion (int): de 0 a tamaño - 1.
        Devuelve:
            El dato eliminado.
        Lanza:
            IndexError si la posición no existe.
        Complejidad: O(n).
        """
        return self._desenlazar(self._nodo_en(posicion))

    def eliminar(self, dato):
        """
        Quita el PRIMER nodo cuyo dato sea igual al indicado.

        Recibe:
            dato: el valor a eliminar.
        Devuelve:
            True si lo encontró y eliminó, False si no estaba.
        Complejidad: O(n).
        """
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                self._desenlazar(actual)
                return True
            actual = actual.siguiente
        return False

    def vaciar(self):
        """
        Elimina todos los elementos.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.cabeza = None
        self.final = None
        self._tamano = 0

    # ------------------------------------------------------------------
    # Búsqueda y recorridos
    # ------------------------------------------------------------------
    def buscar(self, dato):
        """
        Busca un dato desde la cabeza.

        Recibe:
            dato: el valor a buscar.
        Devuelve:
            int con la posición de la primera coincidencia, o -1 si no está.
        Complejidad: O(n).
        """
        actual = self.cabeza
        posicion = 0
        while actual is not None:
            if actual.dato == dato:
                return posicion
            actual = actual.siguiente
            posicion += 1
        return -1

    def recorrer_adelante(self):
        """
        Recorre de la cabeza al final siguiendo 'siguiente' (generador).

        Recibe: nada.
        Devuelve:
            Cada dato, en orden de la posición 0 a la última.
        Complejidad: O(n).
        """
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def recorrer_atras(self):
        """
        Recorre del final a la cabeza siguiendo 'anterior' (generador).
        Esta operación es la que demuestra que la lista es DOBLE.

        Recibe: nada.
        Devuelve:
            Cada dato, de la última posición a la 0.
        Complejidad: O(n).
        """
        actual = self.final
        while actual is not None:
            yield actual.dato
            actual = actual.anterior

    # ------------------------------------------------------------------
    # Operaciones para mover grupos (Solitario)
    # ------------------------------------------------------------------
    def cortar_desde(self, posicion):
        """
        Separa los nodos desde 'posicion' hasta el final y los devuelve
        como una NUEVA ListaDoble. Esta lista se queda con lo de antes.
        En el juego: TOMAR un grupo de cartas de una columna.

        Ejemplo: [K, Q, J, 10].cortar_desde(1) -> esta queda [K],
                 devuelve [Q, J, 10].

        Recibe:
            posicion (int): de 0 a tamaño - 1.
        Devuelve:
            ListaDoble con los elementos cortados.
        Lanza:
            IndexError si la posición no existe.
        Complejidad: O(n) para llegar al nodo; el corte en sí es O(1).
        """
        nodo_corte = self._nodo_en(posicion)
        cortada = ListaDoble()
        cortada.cabeza = nodo_corte
        cortada.final = self.final
        cortada._tamano = self._tamano - posicion

        if nodo_corte.anterior is None:    # se cortó desde la cabeza
            self.cabeza = None
            self.final = None
        else:
            self.final = nodo_corte.anterior
            self.final.siguiente = None
            nodo_corte.anterior = None
        self._tamano = posicion
        return cortada

    def concatenar(self, otra):
        """
        Pega todos los nodos de 'otra' al final de esta lista.
        'otra' queda vacía (sus nodos ahora pertenecen a esta lista).
        En el juego: SOLTAR un grupo de cartas en una columna.

        Recibe:
            otra (ListaDoble): la lista a pegar.
        Devuelve: nada.
        Complejidad: O(1), solo se unen los extremos.
        """
        if otra is self or otra.esta_vacia():
            return
        if self.esta_vacia():
            self.cabeza = otra.cabeza
        else:
            self.final.siguiente = otra.cabeza
            otra.cabeza.anterior = self.final
        self.final = otra.final
        self._tamano += otra._tamano
        otra.vaciar()

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def __len__(self):
        """Permite usar len(lista). Devuelve el tamaño. O(1)."""
        return self._tamano

    def __str__(self):
        """
        Texto de la lista de la cabeza al final, por ejemplo "[K, Q, J]".

        Recibe: nada.
        Devuelve:
            str.
        """
        return "[" + ", ".join(str(d) for d in self.recorrer_adelante()) + "]"
