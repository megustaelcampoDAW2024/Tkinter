## Documentación de la Aplicación Buscaminas en Python con Tkinter

### 1. Estructura del Código y Lógica Implementada

El código se estructura en varias funciones que encapsulan la lógica del juego y la interacción con Tkinter. A continuación, se detalla cada parte:

#### 1.1. Variables Globales

Las principales variables globales son:

*   `buttons`: Una lista de listas que representa la cuadrícula de botones (celdas) del juego. Cada elemento es un objeto `tk.Button`.
*   `mines`: Un conjunto (`set`) de tuplas `(r, c)` que almacenan las coordenadas de las celdas que contienen minas.
*   `start_time`:  Almacena el tiempo de inicio del juego para el temporizador.
*   `current_level`:  Índice del nivel de dificultad actual.