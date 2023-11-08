import tkinter
import tkinter as tk
import sqlite3

def validar_usuario(frame, entry_nick, entry_contraseña, boton_comenzar):
    nick = entry_nick.get()
    contraseña = entry_contraseña.get()

    # Aquí debes agregar la lógica de validación del usuario y contraseña
    # Si los datos son válidos, activa el botón "Comenzar Partida"
    # Ejemplo de validación: (sustituye por tu propia lógica)
    if nick == "usuario1" and contraseña == "contraseña1":
        frame.config(bg="green")  # Cambiar el fondo del frame a verde
        boton_comenzar.config(state="active")

def crear_usuario():
    ventana_registro = tkinter.Toplevel()
    ventana_registro.title("Registrar usuari")
    nick = tkinter.Label(ventana_registro, text="Nick: ")
    nick.grid(row= 2, column=1)
    nick_entry = tkinter.Entry(ventana_registro)
    nick_entry.grid(row=2, column=2)
    password = tkinter.Label(ventana_registro, text="Contrasenya: ")
    password.grid(row=3, column=1)
    password_entry = tkinter.Entry(ventana_registro)
    password_entry.grid(row=3, column=2)
    avatar = tk.Label(ventana_registro, "Imagen avatar: ")
    avatar.grid(row=4, column=1)
    # Aquí debes agregar la lógica para crear un nuevo usuario
    pass

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Juego de dos jugadores")

# Frame para el Jugador 1
frame_jugador1 = tk.Frame(ventana, padx=10, pady=10)
frame_jugador1.grid(row=1, column=1)
frame_jugador1.config(bg="red")  # Cambiar el fondo del frame a rojo

# Frame para el Jugador 2
frame_jugador2 = tk.Frame(ventana, padx=10, pady=10)
frame_jugador2.grid(row=1, column=2)
frame_jugador2.config(bg="blue")  # Cambiar el fondo del frame a azul

# Crear etiquetas de texto en los frames
etiqueta_jugador1 = tk.Label(frame_jugador1, text="Jugador 1")
etiqueta_jugador1.grid(row=1, column=1)

etiqueta_jugador2 = tk.Label(frame_jugador2, text="Jugador 2")
etiqueta_jugador2.grid(row=1, column=1)

# Frame para el botón "Comenzar Partida"
frame_boton = tk.Frame(ventana)
frame_boton.grid(row=2, column=1, columnspan=2)

# Crear el botón "Comenzar Partida" desactivado
boton_comenzar = tk.Button(frame_boton, text="Comenzar Partida", state="disabled")
boton_comenzar.grid(row=1, column=1)

# Botón para crear un nuevo usuario
boton_nuevo_usuario = tk.Button(frame_boton, text="Nuevo Usuario", command=crear_usuario)
boton_nuevo_usuario.grid(row=1, column=2)

# Frame de entrada para usuario y contraseña en el Jugador 1
entry_nick_jugador1 = tk.Entry(frame_jugador1)
entry_contraseña_jugador1 = tk.Entry(frame_jugador1, show="*")  # Contraseña oculta

# Frame de entrada para usuario y contraseña en el Jugador 2
entry_nick_jugador2 = tk.Entry(frame_jugador2)
entry_contraseña_jugador2 = tk.Entry(frame_jugador2, show="*")  # Contraseña oculta

# Etiquetas de texto en los frames de Jugador 1 y Jugador 2
etiqueta_nick_jugador1 = tk.Label(frame_jugador1, text="Nick:")
etiqueta_contraseña_jugador1 = tk.Label(frame_jugador1, text="Contraseña:")

etiqueta_nick_jugador2 = tk.Label(frame_jugador2, text="Nick:")
etiqueta_contraseña_jugador2 = tk.Label(frame_jugador2, text="Contraseña:")

# Botón para entrar con el usuario y contraseña en el Jugador 1
boton_entrar_jugador1 = tk.Button(frame_jugador1, text="Entrar", command=lambda: validar_usuario(frame_jugador1, entry_nick_jugador1, entry_contraseña_jugador1, boton_comenzar))

# Botón para entrar con el usuario y contraseña en el Jugador 2
boton_entrar_jugador2 = tk.Button(frame_jugador2, text="Entrar", command=lambda: validar_usuario(frame_jugador2, entry_nick_jugador2, entry_contraseña_jugador2, boton_comenzar))

# Colocar widgets en la ventana
etiqueta_nick_jugador1.grid(row=2, column=1)
entry_nick_jugador1.grid(row=2, column=2)
etiqueta_contraseña_jugador1.grid(row=3, column=1)
entry_contraseña_jugador1.grid(row=3, column=2)
boton_entrar_jugador1.grid(row=4, column=1, columnspan=2)

etiqueta_nick_jugador2.grid(row=2, column=1)
entry_nick_jugador2.grid(row=2, column=2)
etiqueta_contraseña_jugador2.grid(row=3, column=1)
entry_contraseña_jugador2.grid(row=3, column=2)
boton_entrar_jugador2.grid(row=4, column=1, columnspan=2)

# Iniciar la aplicación
ventana.mainloop()
