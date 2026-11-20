# Solitario Klondike

Proyecto final de **Estructuras de Datos**: el clásico Solitario Klondike
(robar 1 carta), con interfaz gráfica, construido sobre cinco estructuras de
datos programadas desde cero con nodos y referencias.

| | |
|---|---|
| **Juego** | Solitario Klondike (robar 1 carta) |
| **Integrante** | Carlos Andrés Muñoz Ortega |
| **Programa** | Ingeniería de Software, Corporación Universitaria Autónoma del Cauca |
| **Lenguaje** | Python 3.10 o superior (probado en Python 3.12 y 3.13) |
| **Interfaz** | Tkinter (viene incluida con Python, no hay que instalar nada) |
| **Dependencias externas** | Ninguna |

## Cómo ejecutarlo

1. Instalar Python 3.10 o superior desde <https://www.python.org/downloads/>.
   En Windows, durante la instalación, marcar **"Add python.exe to PATH"**
   (Tkinter se instala junto con Python).
2. Abrir una terminal **dentro de la carpeta `Solitario`**.
3. Ejecutar:

```bash
python main.py
```

## Controles

| Acción | Cómo |
|---|---|
| Robar una carta | Clic en el mazo (o tecla Espacio) |
| Seleccionar una carta o un grupo | Clic en la carta (se seleccionan también las de encima) |
| Mover la selección | Clic en la columna o fundación de destino (los destinos válidos se resaltan en dorado) |
| Subir una carta a su fundación | Doble clic en la carta |
| Cancelar la selección | Clic derecho o Esc |
| Deshacer | Botón **Deshacer** o Ctrl+Z |
| Pista | Botón **Pista** o tecla H |

## Las cinco estructuras y su uso en el juego

| Estructura | Archivo | Uso en el juego |
|---|---|---|
| Pila | `estructuras/pila.py` | Las 4 fundaciones, el mazo al repartir y el historial para **deshacer** |
| Cola | `estructuras/cola.py` | Registro de jugadas para **repetir la partida** en el mismo orden |
| Lista circular | `estructuras/lista_circular.py` | El **mazo de robo**, que se recorre una y otra vez con un cursor |
| Lista doblemente enlazada | `estructuras/lista_doble.py` | Las **7 columnas** (mover grupos de cartas) y el barajado |
| Árbol binario de búsqueda | `estructuras/arbol.py` | **Ranking** de los 10 mejores puntajes |

Ninguna estructura usa las colecciones del lenguaje (`list`, `deque`, etc.):
todas se construyen con las clases `Nodo`, `NodoDoble` y `NodoArbol`.

## Organización del código

```
Solitario/
├── main.py                  Punto de entrada del juego
├── estructuras/             Las 5 estructuras de datos (sin lógica del juego)
│   ├── nodo.py, nodo_doble.py, nodo_arbol.py
│   ├── pila.py, cola.py, lista_doble.py, lista_circular.py, arbol.py
├── modelo/                  Lógica del juego (sin interfaz)
│   ├── carta.py             Datos de una carta
│   ├── reglas.py            Todas las reglas del Klondike
│   ├── baraja.py            Crea y baraja las 52 cartas
│   ├── jugada.py            Registro de cada movimiento (deshacer / repetir)
│   ├── tablero.py           Estado de la partida y ejecución de jugadas
│   ├── puntaje.py           Un resultado del ranking
│   └── gestor_puntajes.py   Ranking en el Árbol BST, guardado en puntajes.txt
├── vista/                   Interfaz gráfica en Tkinter
│   ├── ventana_principal.py, pantalla_menu.py, pantalla_juego.py
│   ├── pantalla_puntajes.py, pantalla_reglas.py, pantalla_repeticion.py
│   ├── mesa.py, dibujo.py, dialogos.py, estilos.py
└── documentacion/           Manual de usuario y manual técnico (PDF)
```

Cada clase y cada método está comentado: qué hace, qué recibe y qué devuelve
(en las estructuras, también su complejidad). Al inicio de cada archivo de
`estructuras/` está la teoría de la estructura. Las tablas de complejidad de las
cinco estructuras están en el manual técnico.

## Documentación

El manual de usuario y el manual técnico están en
`documentacion/Manual_Solitario_Klondike.pdf`.
