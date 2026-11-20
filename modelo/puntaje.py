"""
Módulo: puntaje.py
Clase Puntaje: un registro del ranking de mejores puntajes.

DISEÑO
------
Es el DATO que se guarda en el Árbol BST del ranking. El árbol lo ordena
por sus 'puntos' (con la función clave lambda p: p.puntos).

También sabe convertirse a una línea de texto y reconstruirse desde ella,
para que GestorPuntajes pueda guardar y cargar el ranking en un archivo:

    Formato de una línea:   nombre|puntos|segundos|movimientos|fecha|gano
    Ejemplo:                Carlos|845|312|97|2026-11-18 21:40|1


"""

from datetime import datetime

LARGO_MAXIMO_NOMBRE = 15
SEPARADOR = "|"
FORMATO_FECHA = "%Y-%m-%d %H:%M"


class Puntaje:
    """
    Resultado de una partida para el ranking.

    Atributos:
        nombre (str): nombre del jugador (1 a 15 caracteres, sin '|').
        puntos (int): puntaje final (>= 0). Es la CLAVE del árbol.
        segundos (int): duración de la partida.
        movimientos (int): jugadas realizadas.
        fecha (str): fecha y hora en formato "AAAA-MM-DD HH:MM".
        gano (bool): True si la partida terminó en victoria.
    """

    def __init__(self, nombre, puntos, segundos=0, movimientos=0, fecha=None, gano=False):
        """
        Crea un puntaje validando los datos.

        Recibe:
            nombre (str): nombre del jugador. Se limpian espacios y el '|',
                y se recorta a 15 caracteres.
            puntos (int): mayor o igual a 0.
            segundos (int): mayor o igual a 0.
            movimientos (int): mayor o igual a 0.
            fecha (str | None): si es None se usa la fecha y hora actuales.
            gano (bool).
        Devuelve:
            Nada (es el constructor).
        Lanza:
            ValueError si el nombre queda vacío o algún número no es válido.
        Complejidad: O(1).
        """
        nombre = str(nombre).replace(SEPARADOR, "").strip()[:LARGO_MAXIMO_NOMBRE]
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        for etiqueta, numero in (("puntos", puntos), ("segundos", segundos),
                                 ("movimientos", movimientos)):
            if not isinstance(numero, int) or isinstance(numero, bool) or numero < 0:
                raise ValueError(f"Valor inválido para {etiqueta}: {numero}")
        self.nombre = nombre
        self.puntos = puntos
        self.segundos = segundos
        self.movimientos = movimientos
        self.fecha = fecha if fecha else datetime.now().strftime(FORMATO_FECHA)
        self.gano = bool(gano)

    def tiempo_texto(self):
        """
        Devuelve la duración como "mm:ss".

        Recibe: nada.
        Devuelve:
            str, por ejemplo "05:12".
        Complejidad: O(1).
        """
        return f"{self.segundos // 60:02d}:{self.segundos % 60:02d}"

    def a_linea(self):
        """
        Convierte el puntaje en una línea de texto para guardarlo en archivo.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "Carlos|845|312|97|2026-11-18 21:40|1".
        Complejidad: O(1).
        """
        return SEPARADOR.join((self.nombre, str(self.puntos), str(self.segundos),
                               str(self.movimientos), self.fecha, "1" if self.gano else "0"))

    @staticmethod
    def desde_linea(linea):
        """
        Reconstruye un Puntaje a partir de una línea del archivo.

        Recibe:
            linea (str): una línea con el formato de a_linea().
        Devuelve:
            Puntaje.
        Lanza:
            ValueError si la línea está dañada (faltan campos o hay letras
            donde deberían ir números).
        Complejidad: O(1).
        """
        partes = linea.strip().split(SEPARADOR)
        if len(partes) != 6:
            raise ValueError(f"Línea de puntaje dañada: {linea!r}")
        nombre, puntos, segundos, movimientos, fecha, gano = partes
        return Puntaje(nombre, int(puntos), int(segundos), int(movimientos),
                       fecha, gano == "1")

    def __str__(self):
        """
        Texto del puntaje para mostrar en el ranking.

        Recibe: nada.
        Devuelve:
            str, por ejemplo "Carlos - 845 pts (05:12, 97 mov.)".
        """
        return (f"{self.nombre} - {self.puntos} pts "
                f"({self.tiempo_texto()}, {self.movimientos} mov.)")

    def __repr__(self):
        """Texto para depurar."""
        return f"Puntaje({self.nombre!r}, {self.puntos})"
