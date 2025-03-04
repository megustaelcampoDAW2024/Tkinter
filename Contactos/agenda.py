import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='contact_db'
)
cursor = conn.cursor()

# Funciones CRUD
def agregar_contacto():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    
    if not re.match(r'^[A-Za-z ]+$', nombre):
        messagebox.showerror('Error', 'El nombre solo debe contener letras y espacios')
        return
    if not re.match(r'^\d{7,15}$', telefono):
        messagebox.showerror('Error', 'El teléfono debe contener entre 7 y 15 números')
        return
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        messagebox.showerror('Error', 'Correo electrónico no válido')
        return
    
    cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)', (nombre, telefono, email))
    conn.commit()
    cargar_contactos()
    limpiar_campos()
    messagebox.showinfo('Éxito', 'Contacto agregado correctamente')

def cargar_contactos():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM contacts')
    for index, row in enumerate(cursor.fetchall()):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=row, tags=(tag,))

def eliminar_contacto():
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning('Advertencia', 'Seleccione un contacto para eliminar')
        return
    id_contacto = tree.item(seleccionado)['values'][0]
    cursor.execute('DELETE FROM contacts WHERE id = %s', (id_contacto,))
    conn.commit()
    cargar_contactos()
    messagebox.showinfo('Éxito', 'Contacto eliminado correctamente')

def actualizar_contacto():
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning('Advertencia', 'Seleccione un contacto para actualizar')
        return
    
    id_contacto = tree.item(seleccionado)['values'][0]
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    
    cursor.execute('UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s', (nombre, telefono, email, id_contacto))
    conn.commit()
    cargar_contactos()
    limpiar_campos()
    messagebox.showinfo('Éxito', 'Contacto actualizado correctamente')

def buscar_contacto(event):
    query = entry_busqueda.get()
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM contacts WHERE name LIKE %s OR phone LIKE %s', (f'%{query}%', f'%{query}%'))
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def seleccionar_contacto(event):
    seleccionado = tree.selection()
    if seleccionado:
        id_contacto = tree.item(seleccionado)['values'][0]
        cursor.execute('SELECT * FROM contacts WHERE id = %s', (id_contacto,))
        contacto = cursor.fetchone()
        if contacto:
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, contacto[1])
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, contacto[2])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, contacto[3])

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title('Gestión de Contactos')
root.geometry('1200x600')

frame_main = ttk.Frame(root, padding=(200, 0))
frame_main.pack(fill=tk.BOTH, expand=False)

frame_top = ttk.Frame(frame_main)
frame_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

frame_left = ttk.Frame(frame_top)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

frame_right = ttk.Frame(frame_top)
frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

frame_search = ttk.Frame(frame_main)
frame_search.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

ttk.Label(frame_left, text='Nombre:').pack(anchor='w')
entry_nombre = ttk.Entry(frame_left)
entry_nombre.pack(fill=tk.X)

ttk.Label(frame_left, text='Teléfono:').pack(anchor='w')
entry_telefono = ttk.Entry(frame_left)
entry_telefono.pack(fill=tk.X)

ttk.Label(frame_left, text='Correo Electrónico:').pack(anchor='w')
entry_email = ttk.Entry(frame_left)
entry_email.pack(fill=tk.X)

ttk.Button(frame_right, text='Agregar', command=agregar_contacto).pack(fill=tk.X, pady=5)
ttk.Button(frame_right, text='Actualizar', command=actualizar_contacto).pack(fill=tk.X, pady=5)
ttk.Button(frame_right, text='Eliminar', command=eliminar_contacto).pack(fill=tk.X, pady=5)
ttk.Button(frame_right, text='Limpiar', command=limpiar_campos).pack(fill=tk.X, pady=5)

ttk.Label(frame_search, text='Buscar:').pack(anchor='w')
entry_busqueda = ttk.Entry(frame_search)
entry_busqueda.pack(fill=tk.X)
entry_busqueda.bind('<KeyRelease>', buscar_contacto)

tree = ttk.Treeview(frame_main, columns=('ID', 'Nombre', 'Teléfono', 'Email'), show='headings', height=15)
tree.heading('ID', text='ID')
tree.heading('Nombre', text='Nombre')
tree.heading('Teléfono', text='Teléfono')
tree.heading('Email', text='Email')
tree.pack(fill=tk.BOTH, expand=True)

# Configurar el color de fondo de los encabezados
style = ttk.Style()
style.configure('Treeview.Heading', background='lightgray')

tree.tag_configure('oddrow', background='white')
tree.tag_configure('evenrow', background='lightgray')

tree.bind('<<TreeviewSelect>>', seleccionar_contacto)

cargar_contactos()
root.mainloop()