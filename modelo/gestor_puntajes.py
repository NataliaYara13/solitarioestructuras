"""
Módulo: gestor_puntajes.py
Clase GestorPuntajes: administra el ranking de los mejores puntajes usando
el Árbol BST y lo guarda en un archivo de texto.

DISEÑO
------
    - El ranking vive en un Arbol ordenado por puntos
      (clave = lambda p: p.puntos).
    - Al abrir el juego se CARGA el archivo y cada línea se inserta en el árbol.
    - Al terminar una partida se AGREGA el puntaje; si hay más de 10, se
      ELIMINA el mínimo del árbol (así siempre quedan los 10 mejores).
    - Para mostrar el ranking de mayor a menor se usa el recorrido INORDEN
      INVERSO.
    - Para GUARDAR se escribe el árbol en PREORDEN. ¿Por qué preorden? Porque
      al volver a insertar los datos en ese orden se reconstruye EXACTAMENTE
      el mismo árbol (la raíz entra primero, luego sus subárboles).
      Si se guardara en inorden (ordenado), al recargar el árbol quedaría
      como una línea: el peor caso, O(n) en cada operación.


"""

import os

from estructuras.arbol import Arbol
from modelo.puntaje import Puntaje

MAXIMO_RANKING = 10
ARCHIVO_POR_DEFECTO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   "puntajes.txt")


def _clave_puntos(puntaje):
    """
    Función clave del árbol: ordena los puntajes por sus puntos.

    Recibe:
        puntaje (Puntaje).
    Devuelve:
        int con los puntos.
    """
    return puntaje.puntos


class GestorPuntajes:
    """
    Ranking de mejores puntajes guardado en un Árbol BST y en un archivo.

    Atributos:
        ruta (str): ruta del archivo de texto.
        maximo (int): cuántos puntajes se conservan (10 por defecto).
        arbol (Arbol): BST de Puntaje ordenado por puntos.
    """

    def __init__(self, ruta=ARCHIVO_POR_DEFECTO, maximo=MAXIMO_RANKING):
        """
        Crea el gestor y carga el ranking desde el archivo.

        Recibe:
            ruta (str): archivo donde se guarda el ranking.
            maximo (int): cantidad de puntajes a conservar.
        Devuelve: nada.
        Complejidad: O(n·h).
        """
        self.ruta = ruta
        self.maximo = maximo
        self.arbol = Arbol(clave=_clave_puntos)
        self.cargar()

    def cargar(self):
        """
        Lee el archivo e inserta cada puntaje en el árbol. Las líneas
        dañadas se ignoran. Si el archivo no existe, el ranking queda vacío.

        Recibe: nada.
        Devuelve:
            int con la cantidad de puntajes cargados.
        Complejidad: O(n·h).
        """
        self.arbol.vaciar()
        if not os.path.exists(self.ruta):
            return 0
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if linea.strip():
                        try:
                            self.arbol.insertar(Puntaje.desde_linea(linea))
                        except ValueError:
                            continue          # línea dañada: se ignora
        except OSError:
            return 0
        self._recortar()
        return self.arbol.tamano()

    def guardar(self):
        """
        Escribe el ranking en el archivo recorriendo el árbol en PREORDEN
        (así al cargarlo se reconstruye el mismo árbol).

        Recibe: nada.
        Devuelve:
            True si se guardó, False si hubo un error de escritura.
        Complejidad: O(n).
        """
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                for puntaje in self.arbol.preorden():
                    archivo.write(puntaje.a_linea() + "\n")
            return True
        except OSError:
            return False

    def entra_en_ranking(self, puntos):
        """
        Indica si unos puntos alcanzarían para entrar al ranking.

        Recibe:
            puntos (int).
        Devuelve:
            True si hay cupo o si supera al peor puntaje actual.
        Complejidad: O(h).
        """
        if self.arbol.tamano() < self.maximo:
            return True
        return puntos > self.arbol.minimo().puntos

    def agregar(self, puntaje):
        """
        Agrega un puntaje al ranking, deja solo los mejores y guarda.

        Recibe:
            puntaje (Puntaje).
        Devuelve:
            int con la posición obtenida (1 = el mejor), o -1 si no entró.
        Complejidad: O(h + n).
        """
        if not self.entra_en_ranking(puntaje.puntos):
            return -1
        self.arbol.insertar(puntaje)
        self._recortar()
        self.guardar()
        return self.posicion_de(puntaje)

    def ranking(self):
        """
        Recorre el ranking del mejor al peor (inorden inverso del árbol).

        Recibe: nada.
        Devuelve:
            Generador de Puntaje, de mayor a menor puntaje.
        Complejidad: O(n).
        """
        return self.arbol.inorden_inverso()

    def posicion_de(self, puntaje):
        """
        Busca en qué puesto del ranking quedó un puntaje concreto.

        Recibe:
            puntaje (Puntaje): el objeto a ubicar.
        Devuelve:
            int con el puesto (1 = el mejor), o -1 si no está.
        Complejidad: O(n).
        """
        puesto = 1
        for p in self.ranking():
            if p is puntaje:
                return puesto
            puesto += 1
        return -1

    def mejor(self):
        """
        Devuelve el mejor puntaje del ranking.

        Recibe: nada.
        Devuelve:
            Puntaje, o None si el ranking está vacío.
        Complejidad: O(h).
        """
        return self.arbol.maximo()

    def borrar_todo(self):
        """
        Vacía el ranking y el archivo.

        Recibe: nada.
        Devuelve:
            True si se pudo guardar el archivo vacío.
        Complejidad: O(1).
        """
        self.arbol.vaciar()
        return self.guardar()

    def _recortar(self):
        """
        Elimina los peores puntajes (el mínimo del árbol) hasta que queden
        como máximo 'maximo' puntajes.

        Recibe: nada.
        Devuelve: nada.
        Complejidad: O(h) por cada eliminación.
        """
        while self.arbol.tamano() > self.maximo:
            self.arbol.eliminar(self.arbol.minimo().puntos)
