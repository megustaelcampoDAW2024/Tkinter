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

*   **`restart_program()`:**

```python
# Reiniciar el programa
def restart_program():
    global start_time
    start_time = time.time()
    update_board()
    update_timer()
    update_mine_counter()
```
*   **Lógica:** Reinicia el juego completamente, estableciendo un nuevo tablero, reiniciando el temporizador y actualizando el contador de minas.
*   **Variables Globales:** Modifica `start_time`.
*   **Funciones:** Llama a `update_board()`, `update_timer()`, y `update_mine_counter()` para realizar el reinicio.

*   **`reveal_all_mines()`:**

```python
# Revelar todas las minas en la cuadrícula
def reveal_all_mines():
    for (r, c) in mines:
        buttons[r][c]['text'] = 'M'
        buttons[r][c]['bg'] = 'red'
```
*   **Lógica:** Revela la posición de todas las minas en el tablero cuando el jugador pierde.
*   **Tkinter:**
    *   Itera sobre el conjunto `mines`.
    *   Para cada mina `(r, c)`, cambia el texto del botón a 'M' (`buttons[r][c]['text'] = 'M'`) y el color de fondo a rojo (`buttons[r][c]['bg'] = 'red'`).

*   **`reveal(buttons, r, c)`:**

```python
# Revelar una celda y sus adyacentes si no hay minas
def reveal(buttons, r, c):
    if buttons[r][c]['state'] == 'disabled':
        return
    if buttons[r][c]['text'] == '🚩':
        buttons[r][c]['text'] = ''
        buttons[r][c]['bg'] = 'gray'
        update_mine_counter()
    buttons[r][c]['state'] = 'disabled'
    buttons[r][c]['bg'] = 'white'
    if (r, c) in mines:
        buttons[r][c]['text'] = 'M'
        reveal_all_mines()
        messagebox.showinfo("Game Over", "You clicked on a mine!")
        restart_program()
    else:
        count = count_adjacent_mines(buttons, r, c)
        if count > 0:
            buttons[r][c]['text'] = str(count)
            colors = ['blue', 'green', 'red', 'purple', 'maroon', 'turquoise', 'black', 'gray']
            buttons[r][c]['fg'] = colors[count-1]
        else:
            for i in range(max(0, r-1), min(len(buttons), r+2)):
                for j in range(max(0, c-1), min(len(buttons[0]), c+2)):
                    if (i, j) != (r, c):
                        reveal(buttons, i, j)
```
*   **Lógica:** Revela una celda en la posición `(r, c)` y realiza acciones dependiendo de si contiene una mina o no, y del número de minas adyacentes. Es la función central de la lógica del juego.
*   **Tkinter:**
    *   **Verificación de estado deshabilitado:** `if buttons[r][c]['state'] == 'disabled': return`  Si la celda ya está revelada (deshabilitada), no hace nada.
    *   **Desmarcar bandera:** `if buttons[r][c]['text'] == '🚩': ... update_mine_counter()` Si la celda está marcada con una bandera, la desmarca, restaura el color gris original y actualiza el contador de minas.
    *   **Deshabilitar celda:** `buttons[r][c]['state'] = 'disabled'` Deshabilita el botón para que no se pueda volver a clicar.
    *   **Cambiar color de fondo:** `buttons[r][c]['bg'] = 'white'` Cambia el color de fondo a blanco para indicar que está revelada.
    *   **Mina detectada:** `if (r, c) in mines: ... messagebox.showinfo(...) restart_program()` Si la celda contiene una mina, muestra 'M', revela todas las minas con `reveal_all_mines()`, muestra un mensaje "Game Over" en una ventana emergente usando `messagebox.showinfo()`, y reinicia el juego con `restart_program()`.
    *   **Contar minas adyacentes:** `else: count = count_adjacent_mines(buttons, r, c)` Si no es una mina, cuenta las minas adyacentes.
    *   **Mostrar número o expandir:**
        *   Si `count > 0`: Muestra el número de minas adyacentes como texto en el botón (`buttons[r][c]['text'] = str(count)`), y establece el color del texto según el número usando una lista de colores (`buttons[r][c]['fg'] = colors[count-1]`).
        *   Si `count == 0`:  Expande recursivamente a las celdas vecinas vacías.  Utiliza bucles anidados para iterar sobre las celdas vecinas y llama recursivamente a `reveal(buttons, i, j)` para cada vecino que no sea la celda original. La recursión es crucial para la mecánica de expansión del Buscaminas.

*   **`on_left_click(r, c)`:**

```python
# Manejar clic izquierdo en una celda
def on_left_click(r, c):
    reveal(buttons, r, c)
```
*   **Lógica:** Maneja el evento de clic izquierdo en una celda. Simplemente llama a la función `reveal(buttons, r, c)` para revelar la celda clicada.

*   **`check_win()`:**

```python
# Verificar si el jugador ha ganado
def check_win():
    if sum(button['text'] == '🚩' for row in buttons for button in row) > len(mines):
        return False
    for (r, c) in mines:
        if buttons[r][c]['text'] != '🚩':
            return False
    return True
```
*   **Lógica:** Verifica si el jugador ha ganado el juego.
*   **Condiciones de victoria:** El jugador gana si todas las minas están marcadas correctamente con banderas y ninguna celda sin mina está marcada.
*   **Algoritmo:**
    *   Verifica que el número de banderas no exceda el número de minas (`if sum(...) > len(mines): return False`).
    *   Itera sobre el conjunto `mines`. Para cada mina `(r, c)`, verifica que el texto del botón correspondiente sea una bandera (`buttons[r][c]['text'] != '🚩'`). Si alguna mina no está marcada, retorna `False`.
    *   Si todas las minas están marcadas correctamente, retorna `True`.

 *   **`on_right_click(r, c)`:**

```python
# Manejar clic derecho en una celda
def on_right_click(r, c):
    button = buttons[r][c]
    if button['state'] == 'disabled':
        return
    if button['text'] == '🚩':
        button['text'] = ''
        button['bg'] = 'gray'
    else:
        button['text'] = '🚩'
        button['bg'] = 'yellow'
    update_mine_counter()
    if check_win():
        elapsed_time = int(time.time() - start_time)
        messagebox.showinfo("Congratulations", f"You have flagged all mines correctly in {elapsed_time} seconds!")
        restart_program()
```
*   **Lógica:** Maneja el evento de clic derecho en una celda. Permite al jugador marcar o desmarcar una celda con una bandera.
*   **Tkinter:**
    *   Obtiene el botón clicado: `button = buttons[r][c]`.
    *   **Verificar estado deshabilitado:** `if button['state'] == 'disabled': return` Si la celda ya está revelada, no hace nada.
    *   **Alternar bandera:**
        *   Si el botón ya tiene una bandera (`button['text'] == '🚩'`), la elimina (`button['text'] = ''`) y restaura el color de fondo gris.
        *   Si no tiene bandera, coloca una bandera (`button['text'] = '🚩'`) y cambia el color de fondo a amarillo.
    *   Llama a `update_mine_counter()` para actualizar el contador de minas restantes.
    *   Llama a `check_win()` para verificar si el jugador ha ganado después de marcar o desmarcar una bandera. Si gana, calcula el tiempo transcurrido, muestra un mensaje "Congratulations" con el tiempo en una ventana emergente usando `messagebox.showinfo()`, y reinicia el juego con `restart_program()`.

 *   **`update_timer()`:**

```python
# Actualizar el temporizador
def update_timer():
    elapsed_time = int(time.time() - start_time)
    timer_label.config(text=f" | Time: {elapsed_time}s")
    window.after(1000, update_timer)
```
*   **Lógica:** Actualiza la etiqueta `timer_label` con el tiempo transcurrido desde el inicio del juego. Se llama recursivamente cada segundo para actualizar el temporizador en tiempo real.
*   **Variables Globales:** Utiliza `start_time`.
*   **Tkinter:**
    *   Calcula el tiempo transcurrido: `elapsed_time = int(time.time() - start_time)`.
    *   Actualiza el texto de la etiqueta: `timer_label.config(text=f" | Time: {elapsed_time}s")`.
    *   **Programación recursiva con `window.after(1000, update_timer)`:**  Programa que la función `update_timer` se vuelva a ejecutar después de 1000 milisegundos (1 segundo), creando un bucle de actualización del temporizador.

 *   **`update_board()`:**

```python
# Actualizar el tablero según el nivel de dificultad
def update_board():
    global buttons, current_level
    for row in buttons:
        for button in row:
            button.destroy()
    level = difficulty_levels[current_level]
    rows, cols = level["rows"], level["cols"]
    num_mines = (rows * cols) // 8   # Número reducido de minas
    buttons = create_buttons(frame, rows, cols)
    place_mines(buttons, num_mines)
```
*   **Lógica:**  Actualiza el tablero de juego para un nuevo juego o para cambiar el nivel de dificultad.  Elimina los botones existentes, crea nuevos botones con las dimensiones del nivel de dificultad actual y coloca las minas.
*   **Variables Globales:** Modifica `buttons` y `current_level`.
*   **Tkinter:**
    *   **Destruir botones existentes:** Itera sobre la lista `buttons` y utiliza `button.destroy()` para eliminar cada botón de la interfaz gráfica antes de crear uno nuevo.
    *   Obtiene el nivel de dificultad actual de la lista `difficulty_levels` usando `current_level`.
    *   Extrae `rows` y `cols` del nivel de dificultad.
    *   Calcula el número de minas `num_mines` en función del tamaño del tablero.
    *   Crea nuevos botones usando `create_buttons(frame, rows, cols)`.
    *   Coloca las minas usando `place_mines(buttons, num_mines)`.
 
*   **`set_difficulty(level)`:**

```python
# Establecer el nivel de dificultad
def set_difficulty(level):
    global current_level, start_time
    current_level = level
    start_time = time.time()  # Reiniciar el temporizador
    update_board()
```
*   **Lógica:** Establece el nivel de dificultad del juego y reinicia el juego con el nuevo nivel.
*   **Variables Globales:** Modifica `current_level` y `start_time`.
*   **Funciones:**
    *   Actualiza `current_level` con el nuevo nivel seleccionado.
    *   Reinicia el temporizador `start_time = time.time()`.
    *   Actualiza el tablero llamando a `update_board()`.