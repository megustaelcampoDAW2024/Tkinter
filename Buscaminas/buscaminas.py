import tkinter as tk
import random

# Crear botones en la cuadrícula
def create_buttons(frame, rows, cols):
    buttons = []
    for r in range(rows):
        row = []
        for c in range(cols):
            button = tk.Button(frame, width=2, height=1, bg='gray')
            button.grid(row=r, column=c)
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

# Configuración de la ventana principal
window = tk.Tk()
window.title("Buscaminas")

frame = tk.Frame(window)
frame.pack()

buttons = create_buttons(frame, 10, 10)
mines = place_mines(buttons, 10)

window.mainloop()