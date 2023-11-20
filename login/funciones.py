import tkinter
import sqlite3
from tkinter import filedialog,messagebox
from persistencia import conectarBBDD

fallos = 0

def registraUsuario():
    ventaRegistro = tkinter.Toplevel()
    ventaRegistro.title("Registar Usuario")
    ancho = 300
    largo = 300
    ventaRegistro.geometry(f"{ancho}x{largo}")

    label_nick = tkinter.Label(ventaRegistro, text="Nick:")
    entry_nick = tkinter.Entry(ventaRegistro)

    label_password = tkinter.Label(ventaRegistro, text="Password:")
    entry_password = tkinter.Entry(ventaRegistro)

    label_avatar = tkinter.Label(ventaRegistro, text="Avatar (ruta de la imagen):")
    entry_avatar = tkinter.Entry(ventaRegistro)

    def seleccionar_avatar():
        avatar_path = filedialog.askopenfilename(initialdir="./avatar", title="Seleccionar Avatar", filetypes=(
        ("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")))
        entry_avatar.delete(0, tkinter.END)
        entry_avatar.insert(0, avatar_path)

    boton_SeleccionAvatar = tkinter.Button(ventaRegistro, text="Seleccionar Avatar", command=seleccionar_avatar)


    label_nick.pack(pady=5)
    entry_nick.pack(pady=5)

    label_password.pack(pady=5)
    entry_password.pack(pady=5)

    label_avatar.pack(pady=5)
    entry_avatar.pack(pady=5)

    def insertar():
        nick = entry_nick.get()
        password = entry_password.get()
        avatar = entry_avatar.get()
        partidas_jugadas = 0
        partidas_ganadas = 0

        try:
            conexion = conectarBBDD()
            cur = conexion.cursor()

            cur.execute(""" INSERT INTO Usuario(nick,password,avatar,partidas_jugadas,partidas_ganadas)
                        VALUES (?,?,?,?,?)""",(nick, password, avatar,partidas_jugadas,partidas_ganadas))

            conexion.commit()
            conexion.close()
            messagebox.showinfo("Exito","Usuario creado exitosamente")
            ventaRegistro.destroy()

        except:
            messagebox.showerror("Error","Error al crear usuario")

    botonRegistro = tkinter.Button(ventaRegistro,text="Registar",command=insertar)
    boton_SeleccionAvatar.pack(pady=10)
    botonRegistro.pack(pady=10)




def login(nick, password,ventana,frame):
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()

        cur.execute("SELECT * FROM Usuario WHERE nick = ? AND password = ?", (nick, password))
        user = cur.fetchone()

        conexion.close()

        if user is None:
            messagebox.showerror("Login","Usuario o contraseña incorrectos")
            contadorFallos(ventana)
            return False
        else:
            messagebox.showinfo("Login","Login exitoso")
            actualizarFrame(frame, nick, user[3], user[4], user[5])
            return True
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")
        return False




def contadorFallos(ventana):
    global fallos
    fallos += 1
    if fallos >= 3:
        messagebox.showerror("Login", "Tres intentos fallidos, el programa se cerrará")
        ventana.destroy()

def actualizarFrame(frame, nick, avatar, partidas_jugadas, partidas_ganadas):
    # Destruye todos los widgets del frame
    for widget in frame.winfo_children():
        widget.destroy()

    label_nick = tkinter.Label(frame, text=nick)
    label_nick.pack()

    label_avatar = tkinter.Label(frame)
    label_avatar.avatar_image = tkinter.PhotoImage(file=avatar)  # Asigna la imagen a un atributo del widget
    label_avatar.config(image=label_avatar.avatar_image)
    label_avatar.pack()

    label_partidas = tkinter.Label(frame, text=f"Partidas jugadas: {partidas_jugadas}")
    label_partidas.pack()

    label_ganadas = tkinter.Label(frame, text=f"Partidas ganadas: {partidas_ganadas}")
    label_ganadas.pack()

    frame.update()

