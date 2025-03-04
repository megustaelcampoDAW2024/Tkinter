# Documentación del Programa de Gestión de Contactos

## Descripción General

Este programa es una aplicación de escritorio desarrollada en Python utilizando las bibliotecas `tkinter` y `mysql.connector`. La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) en una base de datos MySQL para gestionar contactos. La interfaz gráfica de usuario (GUI) facilita la interacción del usuario con la base de datos.

## Funcionalidades

- **Agregar Contacto**: Permite añadir un nuevo contacto a la base de datos.
- **Cargar Contactos**: Muestra todos los contactos almacenados en la base de datos.
- **Eliminar Contacto**: Permite eliminar un contacto seleccionado.
- **Actualizar Contacto**: Permite modificar los datos de un contacto existente.
- **Buscar Contacto**: Filtra los contactos en función de una cadena de búsqueda.
- **Limpiar Campos**: Limpia los campos de entrada del formulario.

## Uso de `mysql.connector`

La biblioteca `mysql.connector` se utiliza para conectar la aplicación con la base de datos MySQL. A continuación se describe cómo se establece la conexión y se ejecutan las consultas SQL.

### Conexión a la Base de Datos

```python
import mysql.connector

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='contact_db'
)
cursor = conn.cursor()
```

### Ejecución de Consultas

- **Insertar Contacto**:
  ```python
  cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)', (nombre, telefono, email))
  conn.commit()
  ```

- **Seleccionar Contactos**:
  ```python
  cursor.execute('SELECT * FROM contacts')
  ```

- **Eliminar Contacto**:
  ```python
  cursor.execute('DELETE FROM contacts WHERE id = %s', (id_contacto,))
  conn.commit()
  ```

- **Actualizar Contacto**:
  ```python
  cursor.execute('UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s', (nombre, telefono, email, id_contacto))
  conn.commit()
  ```

## Uso de `tkinter`

La biblioteca `tkinter` se utiliza para crear la interfaz gráfica de usuario (GUI). A continuación se describe la configuración de la ventana principal y los componentes de la interfaz.

### Configuración de la Ventana Principal

```python
root = tk.Tk()
root.title('Gestión de Contactos')
root.geometry('1200x600')
```

### Componentes de la Interfaz

- **Entradas de Texto**:
  ```python
  entry_nombre = ttk.Entry(frame_left)
  entry_telefono = ttk.Entry(frame_left)
  entry_email = ttk.Entry(frame_left)
  ```

- **Botones**:
  ```python
  ttk.Button(frame_right, text='Agregar', command=agregar_contacto).pack(fill=tk.X, pady=5)
  ttk.Button(frame_right, text='Actualizar', command=actualizar_contacto).pack(fill=tk.X, pady=5)
  ttk.Button(frame_right, text='Eliminar', command=eliminar_contacto).pack(fill=tk.X, pady=5)
  ttk.Button(frame_right, text='Limpiar', command=limpiar_campos).pack(fill=tk.X, pady=5)
  ```

- **Tabla de Contactos**:
  ```python
  tree = ttk.Treeview(frame_main, columns=('ID', 'Nombre', 'Teléfono', 'Email'), show='headings', height=15)
  tree.heading('ID', text='ID')
  tree.heading('Nombre', text='Nombre')
  tree.heading('Teléfono', text='Teléfono')
  tree.heading('Email', text='Email')
  tree.pack(fill=tk.BOTH, expand=True)
  ```

## Descripción de las Funciones

### `agregar_contacto()`

Agrega un nuevo contacto a la base de datos después de validar los campos de entrada.

```python
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
```

- **Parámetros de entrada**: Ninguno.
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función obtiene los valores de los campos de entrada (`nombre`, `telefono`, `email`), valida los datos y, si son válidos, inserta un nuevo contacto en la base de datos. Luego, recarga la lista de contactos y limpia los campos de entrada.

### `cargar_contactos()`

Carga todos los contactos desde la base de datos y los muestra en la tabla.

```python
def cargar_contactos():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM contacts')
    for index, row in enumerate(cursor.fetchall()):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=row, tags=(tag,))
```

- **Parámetros de entrada**: Ninguno.
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función elimina todos los elementos actuales de la tabla y luego carga todos los contactos desde la base de datos, insertándolos en la tabla con un estilo alternado para las filas.

### `eliminar_contacto()`

Elimina el contacto seleccionado de la base de datos.

```python
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
```

- **Parámetros de entrada**: Ninguno.
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función obtiene el contacto seleccionado en la tabla, elimina el contacto de la base de datos y recarga la lista de contactos.

### `actualizar_contacto()`

Actualiza los datos del contacto seleccionado en la base de datos.

```python
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
```

- **Parámetros de entrada**: Ninguno.
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función obtiene el contacto seleccionado en la tabla, actualiza los datos del contacto en la base de datos con los valores de los campos de entrada y recarga la lista de contactos.

### `buscar_contacto(event)`

Filtra los contactos en función de la cadena de búsqueda ingresada.

```python
def buscar_contacto(event):
    query = entry_busqueda.get()
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM contacts WHERE name LIKE %s OR phone LIKE %s', (f'%{query}%', f'%{query}%'))
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
```

- **Parámetros de entrada**: `event` (evento de teclado).
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función se activa al escribir en el campo de búsqueda. Filtra los contactos en la base de datos que coinciden con la cadena de búsqueda y los muestra en la tabla.

### `limpiar_campos()`

Limpia los campos de entrada del formulario.

```python
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)
```

- **Parámetros de entrada**: Ninguno.
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función limpia los valores de los campos de entrada del formulario.

### `seleccionar_contacto(event)`

Carga los datos del contacto seleccionado en los campos de entrada para su edición.

```python
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
```

- **Parámetros de entrada**: `event` (evento de selección).
- **Parámetros de salida**: Ninguno.
- **Descripción**: Esta función se activa al seleccionar un contacto en la tabla. Carga los datos del contacto seleccionado en los campos de entrada para su edición.