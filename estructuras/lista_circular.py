"""
Módulo: lista_circular.py
Clase ListaCircular: lista simplemente enlazada circular (sin listas de Python).

TEORÍA
------
Es una lista enlazada en la que el ÚLTIMO nodo no apunta a None, sino que
vuelve a apuntar a la CABEZA. Así la lista no tiene "fin": al avanzar desde
el último se llega otra vez al primero.

Referencias que guarda:
    - 'cabeza' -> primer nodo (posición 0).
    - 'ultimo' -> último nodo. Permite insertar al final en O(1) y cerrar
                  el círculo (ultimo.siguiente = cabeza).
    - 'actual' -> un CURSOR que recorre la lista dando vueltas.
                  Si vale None, el cursor está "antes de empezar".

Regla que siempre se cumple (invariante):
    si la lista no está vacía  ->  ultimo.siguiente == cabeza

Representación:
     cabeza                         ultimo
       |                              |
       v                              v
    +->[ 5♦ ]--->[ J♠ ]--->[ 2♥ ]--->[ 9♣ ]--+
    |                                         |
    +-----------------------------------------+
                    ^
                  actual (cursor)

USO EN EL JUEGO
---------------
    MAZO DE ROBO: las cartas que quedan después de repartir.
        - Robar una carta = avanzar() el cursor; la carta en el cursor es
          la que se ve en el descarte.
        - Al llegar a la última y volver a robar, el cursor regresa solo a
          la primera: el mazo se recorre "una y otra vez" sin rearmarlo.
        - Jugar la carta visible = eliminar_actual(); el cursor retrocede a
          la carta anterior, que vuelve a quedar visible.

COMPLEJIDAD
-----------
| Operación            | Complejidad | Nota                                  |
|----------------------|-------------|---------------------------------------|
| insertar_inicio      | O(1)        | Gracias a 'ultimo'                    |
| insertar_final       | O(1)        | Gracias a 'ultimo'                    |
| insertar_en_posicion | O(n)        | Hay que llegar al nodo anterior       |
| eliminar_inicio      | O(1)        | 'ultimo' es el anterior de la cabeza  |
| eliminar_en_posicion | O(n)        |                                       |
| eliminar (por dato)  | O(n)        |                                       |
| eliminar_actual      | O(n)        | Lista simple: hay que buscar anterior |
| buscar / obtener     | O(n)        |                                       |
| recorrer             | O(n)        | Una vuelta completa                   |
| avanzar / ver_actual | O(1)        |                                       |
| posicion_cursor      | O(n)        | Cuenta desde la cabeza                |
| mover_cursor_a       | O(n)        | Llega a la posición desde la cabeza   |
| esta_vacia / tamano  | O(1)        |                                       |
"""

from estructuras.nodo import Nodo


class ListaCircular:
    """
    Lista circular genérica con un cursor que da vueltas.
    Las posiciones empiezan en 0 (la cabeza).

    Atributos:
        cabeza (Nodo | None): primer nodo.
        ultimo (Nodo | None): último nodo (su siguiente es la cabeza).
        actual (Nodo | None): cursor; None = antes de empezar.
        _tamano (int): cantidad de elementos.
    """

    def __init__(self):
        """
        Crea una lista circular vacía.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.cabeza = None
        self.ultimo = None
        self.actual = None
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

    def _nodo_en(self, posicion):
        """
        Método interno: devuelve el nodo de una posición (desde la cabeza).

        Recibe:
            posicion (int): de 0 a tamaño - 1.
        Devuelve:
            Nodo en esa posición.
        Lanza:
            IndexError si la posición no existe.
        Complejidad: O(n).
        """
        if not isinstance(posicion, int) or posicion < 0 or posicion >= self._tamano:
            raise IndexError(f"Posición fuera de rango: {posicion}")
        nodo = self.cabeza
        for _ in range(posicion):
            nodo = nodo.siguiente
        return nodo

    def obtener(self, posicion):
        """
        Devuelve el dato de una posición sin quitarlo.

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
    def _insertar_en_vacia(self, dato):
        """
        Método interno: inserta el primer nodo. Un único nodo apunta a sí
        mismo, porque es a la vez la cabeza y el último.

        Recibe:
            dato: el valor a insertar.
        Devuelve: nada.
        Complejidad: O(1).
        """
        nuevo = Nodo(dato)
        nuevo.siguiente = nuevo
        self.cabeza = nuevo
        self.ultimo = nuevo
        self._tamano = 1

    def insertar_inicio(self, dato):
        """
        Inserta un dato al principio (nueva cabeza).

        Pasos (lista no vacía):
            nuevo.siguiente = cabeza;  ultimo.siguiente = nuevo;  cabeza = nuevo

        Recibe:
            dato: el valor a insertar.
        Devuelve: nada.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            self._insertar_en_vacia(dato)
            return
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.ultimo.siguiente = nuevo
        self.cabeza = nuevo
        self._tamano += 1

    def insertar_final(self, dato):
        """
        Inserta un dato al final (nuevo último), cerrando el círculo.

        Pasos (lista no vacía):
            nuevo.siguiente = cabeza;  ultimo.siguiente = nuevo;  ultimo = nuevo

        Recibe:
            dato: el valor a insertar.
        Devuelve: nada.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            self._insertar_en_vacia(dato)
            return
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.ultimo.siguiente = nuevo
        self.ultimo = nuevo
        self._tamano += 1

    def insertar_en_posicion(self, posicion, dato):
        """
        Inserta un dato para que quede en la posición indicada.

        Pasos (en medio): llegar al nodo 'previo' (posición - 1) y luego
            nuevo.siguiente = previo.siguiente;  previo.siguiente = nuevo

        Recibe:
            posicion (int): de 0 a tamaño.
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
            previo = self._nodo_en(posicion - 1)
            nuevo = Nodo(dato)
            nuevo.siguiente = previo.siguiente
            previo.siguiente = nuevo
            self._tamano += 1

    # ------------------------------------------------------------------
    # Eliminación
    # ------------------------------------------------------------------
    def _quitar_nodo(self, previo, nodo):
        """
        Método interno: quita 'nodo' sabiendo cuál es su 'previo'.
        Ajusta cabeza, último y el cursor si apuntaban al nodo quitado.
        Si el cursor estaba en el nodo quitado, retrocede al previo
        (o queda en None si el quitado era la cabeza).

        Recibe:
            previo (Nodo): el nodo anterior a 'nodo' en el círculo.
            nodo (Nodo): el nodo a quitar.
        Devuelve:
            El dato del nodo quitado.
        Complejidad: O(1).
        """
        era_cabeza = nodo is self.cabeza
        if self._tamano == 1:
            self.cabeza = None
            self.ultimo = None
            self.actual = None
        else:
            previo.siguiente = nodo.siguiente
            if era_cabeza:
                self.cabeza = nodo.siguiente
            if nodo is self.ultimo:
                self.ultimo = previo
            if self.actual is nodo:
                self.actual = None if era_cabeza else previo
        nodo.siguiente = None
        self._tamano -= 1
        return nodo.dato

    def _previo_de(self, nodo):
        """
        Método interno: encuentra el nodo que apunta a 'nodo'.
        Como la lista es simple, hay que dar la vuelta buscándolo.

        Recibe:
            nodo (Nodo): un nodo de esta lista.
        Devuelve:
            Nodo anterior a 'nodo'.
        Complejidad: O(n).
        """
        previo = self.ultimo
        while previo.siguiente is not nodo:
            previo = previo.siguiente
        return previo

    def eliminar_inicio(self):
        """
        Quita y devuelve el dato de la cabeza.

        Recibe: nada.
        Devuelve:
            El dato que estaba en la cabeza.
        Lanza:
            IndexError si está vacía.
        Complejidad: O(1): el anterior de la cabeza es 'ultimo'.
        """
        if self.esta_vacia():
            raise IndexError("No se puede eliminar: la lista está vacía")
        return self._quitar_nodo(self.ultimo, self.cabeza)

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
        nodo = self._nodo_en(posicion)
        previo = self.ultimo if posicion == 0 else self._nodo_en(posicion - 1)
        return self._quitar_nodo(previo, nodo)

    def eliminar(self, dato):
        """
        Quita el PRIMER nodo (desde la cabeza) cuyo dato sea igual al indicado.

        Recibe:
            dato: el valor a eliminar.
        Devuelve:
            True si lo encontró y eliminó, False si no estaba.
        Complejidad: O(n).
        """
        if self.esta_vacia():
            return False
        previo = self.ultimo
        nodo = self.cabeza
        for _ in range(self._tamano):
            if nodo.dato == dato:
                self._quitar_nodo(previo, nodo)
                return True
            previo = nodo
            nodo = nodo.siguiente
        return False

    def eliminar_actual(self):
        """
        Quita y devuelve el dato donde está el cursor.
        El cursor retrocede al nodo anterior (o queda en None si se quitó
        la cabeza). En el juego: jugar la carta visible del descarte.

        Recibe: nada.
        Devuelve:
            El dato eliminado.
        Lanza:
            IndexError si la lista está vacía o el cursor no está en ningún nodo.
        Complejidad: O(n), por buscar el nodo anterior.
        """
        if self.actual is None:
            raise IndexError("No hay elemento en el cursor para eliminar")
        return self._quitar_nodo(self._previo_de(self.actual), self.actual)

    def vaciar(self):
        """
        Elimina todos los elementos.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1). (Se rompe el círculo para facilitar la
        liberación de memoria.)
        """
        if self.ultimo is not None:
            self.ultimo.siguiente = None
        self.cabeza = None
        self.ultimo = None
        self.actual = None
        self._tamano = 0

    # ------------------------------------------------------------------
    # Búsqueda y recorrido
    # ------------------------------------------------------------------
    def buscar(self, dato):
        """
        Busca un dato desde la cabeza dando como máximo una vuelta.
        (Hay que contar los pasos: en una lista circular nunca se llega a
        None, así que sin contador el ciclo sería infinito.)

        Recibe:
            dato: el valor a buscar.
        Devuelve:
            int con la posición, o -1 si no está.
        Complejidad: O(n).
        """
        nodo = self.cabeza
        for posicion in range(self._tamano):
            if nodo.dato == dato:
                return posicion
            nodo = nodo.siguiente
        return -1

    def recorrer(self):
        """
        Recorre una vuelta completa, de la cabeza al último (generador).

        Recibe: nada.
        Devuelve:
            Cada dato, de la posición 0 a la última.
        Complejidad: O(n).
        """
        nodo = self.cabeza
        for _ in range(self._tamano):
            yield nodo.dato
            nodo = nodo.siguiente

    # ------------------------------------------------------------------
    # Cursor (lo que hace especial a la lista circular en el juego)
    # ------------------------------------------------------------------
    def avanzar(self):
        """
        Mueve el cursor al siguiente nodo y devuelve su dato.
        Si el cursor estaba antes de empezar (None), va a la cabeza.
        Si estaba en el último, vuelve a la cabeza (por ser circular).

        Recibe: nada.
        Devuelve:
            El dato en la nueva posición del cursor.
        Lanza:
            IndexError si la lista está vacía.
        Complejidad: O(1).
        """
        if self.esta_vacia():
            raise IndexError("No se puede avanzar: la lista está vacía")
        self.actual = self.cabeza if self.actual is None else self.actual.siguiente
        return self.actual.dato

    def ver_actual(self):
        """
        Devuelve el dato del cursor sin moverlo.

        Recibe: nada.
        Devuelve:
            El dato del cursor, o None si está antes de empezar o vacía.
        Complejidad: O(1).
        """
        return None if self.actual is None else self.actual.dato

    def cursor_en_ultimo(self):
        """
        Indica si el cursor está en el último nodo (el próximo avance
        dará la vuelta a la cabeza).

        Recibe: nada.
        Devuelve:
            True si el cursor está en el último nodo.
        Complejidad: O(1).
        """
        return self.actual is not None and self.actual is self.ultimo

    def posicion_cursor(self):
        """
        Devuelve la posición en la que está el cursor.
        La guarda el Tablero para poder devolver el cursor al mismo lugar
        al deshacer una jugada.

        Recibe: nada.
        Devuelve:
            int con la posición (0 = cabeza), o -1 si el cursor está antes
            de empezar.
        Complejidad: O(n).
        """
        if self.actual is None:
            return -1
        nodo = self.cabeza
        posicion = 0
        while nodo is not self.actual:
            nodo = nodo.siguiente
            posicion += 1
        return posicion

    def mover_cursor_a(self, posicion):
        """
        Pone el cursor en una posición. Con -1 lo deja antes de empezar.

        Recibe:
            posicion (int): de -1 a tamaño - 1.
        Devuelve: nada.
        Lanza:
            IndexError si la posición no existe.
        Complejidad: O(n).
        """
        if posicion == -1:
            self.actual = None
        else:
            self.actual = self._nodo_en(posicion)

    def reiniciar_cursor(self):
        """
        Deja el cursor antes de empezar (el próximo avance va a la cabeza).

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(1).
        """
        self.actual = None

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def __len__(self):
        """Permite usar len(lista). Devuelve el tamaño. O(1)."""
        return self._tamano

    def __str__(self):
        """
        Texto de una vuelta de la lista; el cursor se marca con < >.
        Ejemplo: "[5, <7>, 9] (circular)".

        Recibe: nada.
        Devuelve:
            str.
        """
        texto = ""
        nodo = self.cabeza
        for i in range(self._tamano):
            dato = str(nodo.dato)
            texto += f"<{dato}>" if nodo is self.actual else dato
            if i < self._tamano - 1:
                texto += ", "
            nodo = nodo.siguiente
        return "[" + texto + "] (circular)"
