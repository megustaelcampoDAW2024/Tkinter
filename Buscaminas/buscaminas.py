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
        buttons[r][c]['text'] = ''
        buttons[r][c]['bg'] = 'white'

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

# Configuración de la ventana principal
window = tk.Tk()
window.title("Buscaminas")

frame = tk.Frame(window)
frame.pack()

buttons = create_buttons(frame, 10, 10)
mines = place_mines(buttons, 10)

window.mainloop()