import tkinter as tk
import random
from tkinter import messagebox
import time

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

# Actualizar contador de minas restantes
def update_mine_counter():
    remaining_mines = len(mines) - sum(button['text'] == '🚩' for row in buttons for button in row)
    mine_counter_label.config(text=f"Mines: {remaining_mines}")

# Reiniciar el programa
def restart_program():
    global start_time
    start_time = time.time()
    update_board()
    update_timer()
    update_mine_counter()

# Revelar todas las minas en la cuadrícula
def reveal_all_mines():
    for (r, c) in mines:
        buttons[r][c]['text'] = 'M'
        buttons[r][c]['bg'] = 'red'

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

# Manejar clic izquierdo en una celda
def on_left_click(r, c):
    reveal(buttons, r, c)

# Verificar si el jugador ha ganado
def check_win():
    if sum(button['text'] == '🚩' for row in buttons for button in row) > len(mines):
        return False
    for (r, c) in mines:
        if buttons[r][c]['text'] != '🚩':
            return False
    return True

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

# Actualizar el temporizador
def update_timer():
    elapsed_time = int(time.time() - start_time)
    timer_label.config(text=f" | Time: {elapsed_time}s")
    window.after(1000, update_timer)

# Niveles de dificultad
difficulty_levels = [
    {"rows": 10, "cols": 10},
    {"rows": 15, "cols": 15},
    {"rows": 20, "cols": 20},
    {"rows": 25, "cols": 25},
    {"rows": 30, "cols": 30},
    {"rows": 31, "cols": 35},
    {"rows": 31, "cols": 40},
    {"rows": 31, "cols": 45},
    {"rows": 31, "cols": 50},
    {"rows": 31, "cols": 60},
    {"rows": 31, "cols": 65}   
]
current_level = 0

# Actualizar el tablero según el nivel de dificultad
def update_board():
    global buttons, current_level
    for row in buttons:
        for button in row:
            button.destroy()
    level = difficulty_levels[current_level]
    rows, cols = level["rows"], level["cols"]
    num_mines = (rows * cols) // 8  # Número reducido de minas
    buttons = create_buttons(frame, rows, cols)
    place_mines(buttons, num_mines)

# Establecer el nivel de dificultad
def set_difficulty(level):
    global current_level, start_time
    current_level = level
    start_time = time.time()  # Reiniciar el temporizador
    update_board()

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