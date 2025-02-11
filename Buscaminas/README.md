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

#### 1.3. Configuración de la Ventana Principal y Menús

```python
# Configuración de la ventana principal
window = tk.Tk()
window.state('zoomed')
window.title("Buscaminas")

# Marco del título
title_frame = tk.Frame(window)
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="BUSCAMINAS", font=("Arial Bold", 24))
title_label.pack()

# Marco de información
info_frame = tk.Frame(window)
info_frame.pack(pady=5)

mine_counter_label = tk.Label(info_frame, text="Mines: 0", font=("Arial", 14))
mine_counter_label.pack(side=tk.LEFT)

timer_label = tk.Label(info_frame, text=" | Time: 0s", font=("Arial", 14))
timer_label.pack(side=tk.LEFT)

# Marco de botones
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Crear un menú desplegable para los niveles de dificultad
difficulty_var = tk.StringVar(window)
difficulty_var.set(f"{difficulty_levels[0]['rows']}x{difficulty_levels[0]['cols']}")

difficulty_menu = tk.OptionMenu(button_frame, difficulty_var, *[f"{level['rows']}x{level['cols']}" for level in difficulty_levels], command=lambda value: set_difficulty([f"{level['rows']}x{level['cols']}" for level in difficulty_levels].index(value)))
difficulty_menu.grid(row=0, column=0, padx=5)

restart_button = tk.Button(button_frame, text="Restart", command=restart_program, bg='orange')
restart_button.grid(row=0, column=1, padx=5)

# Marco del tablero de juego
frame = tk.Frame(window, bd=5, relief="solid", bg="gray")
frame.pack(padx=10, pady=10)

buttons = []
start_time = time.time()
update_board()
update_timer()
update_mine_counter()

window.mainloop()
```

*   `window = tk.Tk()`: Crea la ventana principal de la aplicación. Es la base sobre la que se construirá toda la interfaz gráfica.
*   `window.state('zoomed')`: Maximiza la ventana al iniciar. Esto hace que la ventana ocupe toda la pantalla al arrancar el juego, proporcionando una mejor experiencia de usuario, especialmente en pantallas grandes.
*   `window.title("Buscaminas")`: Establece el título que se muestra en la barra de título de la ventana, en este caso, "Buscaminas".

*   **Marcos (`tk.Frame`)**: Se utilizan marcos para organizar la interfaz de manera lógica y visual. Son contenedores para otros widgets.

    *   `title_frame = tk.Frame(window)`:  Crea un marco para el título del juego. Se asocia a la ventana principal (`window`).
    *   `title_frame.pack(pady=10)`:  Empaqueta el `title_frame` dentro de la ventana. `pack` es un gestor de geometría que organiza los widgets. `pady=10` añade un espacio vertical de 10 píxeles alrededor del marco.
    *   `info_frame = tk.Frame(window)`: Crea un marco para contener la información del juego, como el contador de minas y el temporizador.
    *   `info_frame.pack(pady=5)`: Empaqueta el `info_frame`, similar al `title_frame` pero con un espacio vertical menor (`pady=5`).
    *   `button_frame = tk.Frame(window)`:  Crea un marco para agrupar el menú de dificultad y el botón de reinicio.
    *   `button_frame.pack(pady=10)`: Empaqueta el `button_frame`.
    *   `frame = tk.Frame(window, bd=5, relief="solid", bg="gray")`:  Crea el marco principal para el tablero de juego.
        *   `bd=5`:  Establece un borde de 5 píxeles alrededor del marco.
        *   `relief="solid"`:  Define el estilo del borde como "sólido", lo que le da un aspecto visual definido.
        *   `bg="gray"`:  Establece el color de fondo del marco a gris.
    *   `frame.pack(padx=10, pady=10)`: Empaqueta el `frame`, añadiendo espacio horizontal (`padx=10`) y vertical (`pady=10`) a su alrededor.

*   **Etiquetas (`tk.Label`)**: Se utilizan para mostrar texto estático en la interfaz.

    *   `title_label = tk.Label(title_frame, text="BUSCAMINAS", font=("Arial Bold", 24))`: Crea una etiqueta para el título "BUSCAMINAS".
        *   `title_frame`:  Indica que la etiqueta se coloca dentro del marco `title_frame`.
        *   `text="BUSCAMINAS"`:  Establece el texto que se mostrará.
        *   `font=("Arial Bold", 24)`:  Define la fuente como Arial en negrita y tamaño 24.
    *   `title_label.pack()`:  Empaqueta la etiqueta dentro de `title_frame`, haciendo que se muestre.
    *   `mine_counter_label = tk.Label(info_frame, text="Mines: 0", font=("Arial", 14))`: Crea una etiqueta para el contador de minas, inicialmente mostrando "Mines: 0".
        *   `info_frame`:  La etiqueta se coloca en el `info_frame`.
        *   `font=("Arial", 14)`:  Fuente Arial, tamaño 14.
    *   `mine_counter_label.pack(side=tk.LEFT)`:  Empaqueta la etiqueta en `info_frame` y la alinea a la izquierda (`side=tk.LEFT`).
    *   `timer_label = tk.Label(info_frame, text=" | Time: 0s", font=("Arial", 14))`:  Crea una etiqueta para el temporizador, inicialmente mostrando " | Time: 0s".
    *   `timer_label.pack(side=tk.LEFT)`:  Empaqueta la etiqueta en `info_frame` y la alinea a la izquierda, al lado del contador de minas.

*   **Menú Desplegable de Dificultad (`tk.OptionMenu`)**:  Permite al usuario seleccionar el nivel de dificultad.

    *   `difficulty_var = tk.StringVar(window)`: Crea una variable de control de Tkinter (`StringVar`) asociada a la ventana principal. Esta variable almacenará la opción de dificultad seleccionada en el menú.
    *   `difficulty_var.set(f"{difficulty_levels[0]['rows']}x{difficulty_levels[0]['cols']}")`:  Establece el valor inicial de `difficulty_var` con el primer nivel de dificultad de la lista `difficulty_levels`. Esto hace que el menú muestre inicialmente el primer nivel.
    *   `difficulty_menu = tk.OptionMenu(...)`: Crea el menú desplegable (`OptionMenu`).
        *   `button_frame`:  Indica que el menú se coloca en el marco `button_frame`.
        *   `difficulty_var`:  Asocia el menú a la variable de control `difficulty_var`. Los cambios en el menú actualizarán esta variable.
        *   `*[f"{level['rows']}x{level['cols']}" for level in difficulty_levels]`: Genera las opciones que se mostrarán en el menú. Utiliza una lista por comprensión para iterar sobre la lista `difficulty_levels` y formatear cada nivel como una cadena "filas x columnas" (e.g., "10x10", "15x15"). El `*` desempaqueta esta lista para que `OptionMenu` reciba las opciones individualmente.
        *   `command=lambda value: set_difficulty(...)`: Define la función que se ejecutará cuando el usuario seleccione una opción del menú.
            *   `lambda value: set_difficulty(...)`:  Utiliza una función lambda anónima que toma el valor seleccionado (`value`) como argumento y llama a la función `set_difficulty`.
            *   `[f"{level['rows']}x{level['cols']}" for level in difficulty_levels].index(value)`:  Dentro de la función `set_difficulty`, se encuentra el índice del nivel seleccionado en la lista `difficulty_levels` buscando la cadena de formato "filas x columnas" que coincide con el valor seleccionado (`value`).
    *   `difficulty_menu.grid(row=0, column=0, padx=5)`: Coloca el menú en el `button_frame` usando el gestor de geometría `grid`.
        *   `row=0, column=0`:  Lo coloca en la primera fila y primera columna de la cuadrícula del `button_frame`.
        *   `padx=5`:  Añade un espacio horizontal de 5 píxeles a los lados del menú.

*   **Botón de Reinicio (`tk.Button`)**: Permite reiniciar el juego manualmente.

    *   `restart_button = tk.Button(...)`: Crea el botón "Restart".
        *   `button_frame`:  Indica que se coloca en el marco `button_frame`.
        *   `text="Restart"`:  Establece el texto del botón como "Restart".
        *   `command=restart_program`:  Asocia la función `restart_program` a la acción de hacer clic en el botón. Cuando se hace clic, se ejecuta `restart_program`.
        *   `bg='orange'`:  Establece el color de fondo del botón a naranja.
    *   `restart_button.grid(row=0, column=1, padx=5)`:  Coloca el botón en el `button_frame` usando `grid`. Se coloca en la primera fila (`row=0`) y segunda columna (`column=1`), a la derecha del menú de dificultad.

*   **Creación inicial del tablero**:  Configuración inicial al iniciar el juego.

    *   `buttons = []`: Inicializa la lista global `buttons` como una lista vacía. Esta lista almacenará la cuadrícula de botones que representan las celdas del juego.
    *   `start_time = time.time()`:  Establece la variable global `start_time` con el tiempo actual. Esto se utiliza para medir el tiempo de juego.
    *   `update_board()`: Llama a la función `update_board` para crear el tablero de juego inicial. Esto crea los botones, coloca las minas y configura el tablero según el nivel de dificultad predeterminado (el primero de la lista `difficulty_levels`).
    *   `update_timer()`: Inicia el temporizador llamando a `update_timer`. Esta función se encargará de actualizar la etiqueta del temporizador cada segundo.
    *   `update_mine_counter()`:  Actualiza el contador de minas llamando a `update_mine_counter`. Esto asegura que el contador de minas se muestre correctamente al inicio del juego.

*   **`window.mainloop()`**: Inicia el bucle principal de Tkinter.

    *   Esta línea es esencial para que la interfaz gráfica funcione. `mainloop()` entra en un bucle infinito que espera eventos (como clics de botón, pulsaciones de teclado, etc.) y los procesa, actualizando la interfaz según sea necesario.  Sin `mainloop()`, la ventana se mostraría brevemente y luego se cerraría sin ser interactiva.
 