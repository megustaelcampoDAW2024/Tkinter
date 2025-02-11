import tkinter as tk
import random
from tkinter import messagebox

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
    mines = set()
    rows = len(buttons)
    cols = len(buttons[0])
    while len(mines) < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        mines.add((r, c))
    return mines

# Manejar clic izquierdo en una celda
def on_left_click(r, c):
    if (r, c) in mines:
        buttons[r][c]['text'] = 'M'
        buttons[r][c]['bg'] = 'red'
        reveal_all_mines()
        messagebox.showinfo("Game Over", "¡Has perdido!")
    else:
        reveal(buttons, r, c)

# Manejar clic derecho en una celda
def on_right_click(r, c):
    button = buttons[r][c]
    if button['text'] == '🚩':
        button['text'] = ''
        button['bg'] = 'gray'
    else:
        button['text'] = '🚩'
        button['bg'] = 'yellow'

# Revelar todas las minas en la cuadrícula
def reveal_all_mines():
    for (r, c) in mines:
        buttons[r][c]['text'] = 'M'
        buttons[r][c]['bg'] = 'red'

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

# Revelar una celda y sus adyacentes si no hay minas
def reveal(buttons, r, c):
    if buttons[r][c]['state'] == 'disabled':
        return
    buttons[r][c]['state'] = 'disabled'
    buttons[r][c]['bg'] = 'white'
    count = count_adjacent_mines(buttons, r, c)
    if count > 0:
        buttons[r][c]['text'] = str(count)
    else:
        for i in range(max(0, r-1), min(len(buttons), r+2)):
            for j in range(max(0, c-1), min(len(buttons[0]), c+2)):
                if (i, j) != (r, c):
                    reveal(buttons, i, j)

# Configuración de la ventana principal
window = tk.Tk()
window.title("Buscaminas")

frame = tk.Frame(window)
frame.pack()

buttons = create_buttons(frame, 10, 10)
mines = place_mines(buttons, 10)

window.mainloop()