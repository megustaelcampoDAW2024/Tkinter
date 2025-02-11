# Buscaminas

## Documentación de la Aplicación Buscaminas en Python con Tkinter

### 1. Estructura del Código y Lógica Implementada

El código se estructura en varias funciones que encapsulan la lógica del juego y la interacción con Tkinter. A continuación, se detalla cada parte:

#### 1.1. Variables Globales

Las principales variables globales son:

*   `buttons`: Una lista de listas que representa la cuadrícula de botones (celdas) del juego. Cada elemento es un objeto `tk.Button`.
*   `mines`: Un conjunto (`set`) de tuplas `(r, c)` que almacenan las coordenadas de las celdas que contienen minas.
*   `start_time`:  Almacena el tiempo de inicio del juego para el temporizador.
*   `current_level`:  Índice del nivel de dificultad actual.

#### 1.2. Funciones Principales y Lógica del Juego

A continuación, se explican las funciones clave y la lógica que implementan, intercalando los trozos de código correspondientes:

*   **`create_buttons(frame, rows, cols)`:**

```python
# Crear botones en la cuadrícula
def create_buttons(frame, rows, cols):
    buttons = []
    for r in range(rows):
        row = []
        for c in range(cols):
            button = tk.Button(frame, width=2, height=1, bg='gray')
            button.grid(row=r, column=c)
            button.bind('<Button-1>', lambda e, r=r, c=c: on_left_click(r, c))
            button.bind('<Button-3>', lambda e, r=r, c=c: on_right_click(r, c))
            row.append(button)
        buttons.append(row)
    return buttons
```
*   **Lógica:** Crea una cuadrícula de botones dentro del `frame` proporcionado, con el número de `rows` y `cols` especificado.
*   **Tkinter:**
    *   Utiliza bucles anidados `for` para iterar sobre filas y columnas.
    *   Crea un objeto `tk.Button` para cada celda.
    *   Configura `width`, `height`, `bg` (color de fondo inicial) del botón.
    *   Utiliza `button.grid(row=r, column=c)` para colocar cada botón en la cuadrícula del `frame`.
    *   **`bind('<Button-1>', ...)` y `bind('<Button-3>', ...)`:** Asocia las funciones `on_left_click` y `on_right_click` a los eventos de clic izquierdo y derecho respectivamente en cada botón. Se utilizan funciones lambda para pasar las coordenadas `(r, c)` a las funciones de manejo de eventos.
    *   Almacena cada fila de botones en una lista y todas las filas en la lista `buttons`.
*   **Retorno:** Devuelve la lista de listas `buttons`.

*   **`place_mines(buttons, num_mines)`:**

```python
# Colocar minas aleatoriamente en la cuadrícula
def place_mines(buttons, num_mines):
    global mines
    rows = len(buttons)
    cols = len(buttons[0])
    mines = set()
    while len(mines) < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        mines.add((r, c))
    for (r, c) in mines:
        buttons[r][c].mine = True
```
*   **Lógica:** Coloca aleatoriamente `num_mines` minas en la cuadrícula de botones.
*   **Variables Globales:**  Modifica la variable global `mines`.
*   **Algoritmo:**
    *   Inicializa `mines` como un conjunto vacío.
    *   Utiliza un bucle `while` para asegurar que se coloquen exactamente `num_mines` minas.
    *   En cada iteración, genera coordenadas aleatorias `(r, c)` dentro de la cuadrícula usando `random.randint()`.
    *   Añade las coordenadas `(r, c)` al conjunto `mines`. Utilizar un conjunto evita colocar minas en la misma celda múltiples veces.
    *   Después de colocar todas las minas, itera sobre el conjunto `mines` y añade un atributo personalizado `mine = True` a cada botón que representa una mina (`buttons[r][c].mine = True`). Este atributo facilita la verificación posterior si una celda tiene una mina.

*   **`count_adjacent_mines(buttons, r, c)`:**

```python
# Contar minas adyacentes a una celda
def count_adjacent_mines(buttons, r, c):
    rows = len(buttons)
    cols = len(buttons[0])
    count = 0
    for i in range(max(0, r-1), min(rows, r+2)):
        for j in range(max(0, c-1), min(cols, c+2)):
            if (i, j) in mines:
                count += 1
    return count
```
*   **Lógica:** Cuenta el número de minas adyacentes a la celda en la posición `(r, c)`.
*   **Algoritmo:**
    *   Itera sobre las celdas vecinas de `(r, c)`, incluyendo las diagonales. Los bucles `for` con `range(max(0, r-1), min(rows, r+2))` y similar para `c` aseguran que se consideren solo las celdas dentro de los límites de la cuadrícula.
    *   Para cada celda vecina `(i, j)`, verifica si `(i, j)` está en el conjunto `mines`.
    *   Incrementa un contador `count` por cada mina adyacente encontrada.
*   **Retorno:** Devuelve el `count` de minas adyacentes.

*   **`update_mine_counter()`:**

```python
# Actualizar contador de minas restantes
def update_mine_counter():
    remaining_mines = len(mines) - sum(button['text'] == '🚩' for row in buttons for button in row)
    mine_counter_label.config(text=f"Mines: {remaining_mines}")
```
*   **Lógica:** Actualiza la etiqueta `mine_counter_label` para mostrar el número de minas restantes (total de minas menos las celdas marcadas con banderas).
*   **Tkinter:**
    *   Calcula `remaining_mines`: Total de minas (`len(mines)`) menos el número de banderas (`'🚩'`) en la cuadrícula.  Utiliza una expresión generadora y `sum()` para contar las banderas de manera eficiente.
    *   Utiliza `mine_counter_label.config(text=f"Mines: {remaining_mines}")` para actualizar el texto de la etiqueta con el nuevo valor.