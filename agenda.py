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
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

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

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title('Gestión de Contactos')
root.geometry('600x400')

ttk.Label(root, text='Nombre:').pack()
entry_nombre = ttk.Entry(root)
entry_nombre.pack()

ttk.Label(root, text='Teléfono:').pack()
entry_telefono = ttk.Entry(root)
entry_telefono.pack()

ttk.Label(root, text='Correo Electrónico:').pack()
entry_email = ttk.Entry(root)
entry_email.pack()

ttk.Button(root, text='Agregar', command=agregar_contacto).pack()
ttk.Button(root, text='Actualizar', command=actualizar_contacto).pack()
ttk.Button(root, text='Eliminar', command=eliminar_contacto).pack()

ttk.Label(root, text='Buscar:').pack()
entry_busqueda = ttk.Entry(root)
entry_busqueda.pack()
entry_busqueda.bind('<KeyRelease>', buscar_contacto)

tree = ttk.Treeview(root, columns=('ID', 'Nombre', 'Teléfono', 'Email'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nombre', text='Nombre')
tree.heading('Teléfono', text='Teléfono')
tree.heading('Email', text='Email')
tree.pack()

cargar_contactos()
root.mainloop()
