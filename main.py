"""
Solitario Klondike — Proyecto final de Estructuras de Datos.
Autor: Carlos Andrés Muñoz Ortega.

Punto de entrada del juego. Ejecutar desde la carpeta 'Solitario':
    python main.py
"""

from vista.ventana_principal import VentanaPrincipal


def main():
    """
    Crea la ventana principal y arranca el ciclo de eventos de Tkinter.

    Recibe: nada.
    Devuelve: nada.
    """
    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
