import tkinter
import sqlite3
from tkinter import filedialog,messagebox
from persistencia import conectarBBDD


fallos = 0
usuariosLogeados= 0
idUserLogeado = id

def primerFrame(ventana):
    frameJ1 = tkinter.Frame(ventana,bg="blue")
    frameJ1.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    label_nickJ1 = tkinter.Label(frameJ1, text="Nick:")
    label_nickJ1.pack(pady=5)
    entry_nickJ1 = tkinter.Entry(frameJ1)
    entry_nickJ1.pack(pady=5)

    label_passwordJ1 = tkinter.Label(frameJ1, text="Password:")
    label_passwordJ1.pack(pady=5)
    entry_passwordJ1 = tkinter.Entry(frameJ1, show="*")
    entry_passwordJ1.pack(pady=5)

    botonEntrar = tkinter.Button(frameJ1, text="Entrar", command=lambda: login(entry_nickJ1.get(), entry_passwordJ1.get(),ventana,frameJ1))
    botonEntrar.pack(side=tkinter.BOTTOM, pady=10)
    

def segundoFrame(ventana):
    frameJ2 = tkinter.Frame(ventana, bg="red")
    frameJ2.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    label_nickJ2 = tkinter.Label(frameJ2, text="Nick:")
    label_nickJ2.pack(pady=5)
    entry_nickJ2 = tkinter.Entry(frameJ2)
    entry_nickJ2.pack(pady=5)

    label_passwordJ2 = tkinter.Label(frameJ2, text="Password:")
    label_passwordJ2.pack(pady=5)
    entry_passwordJ2 = tkinter.Entry(frameJ2, show="*")  # Show '*' for password
    entry_passwordJ2.pack(pady=5)

    botonEntrar = tkinter.Button(frameJ2, text="Entrar", command=lambda: login(entry_nickJ2.get(), entry_passwordJ2.get(),ventana,
                                                                           frameJ2))
    botonEntrar.pack(side=tkinter.BOTTOM, pady=10)
        

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

    """ def seleccionar_avatar():
        avatar_path = filedialog.askopenfilename(initialdir="./avatar", title="Seleccionar Avatar", filetypes=(
        ("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")))
        entry_avatar.delete(0, tkinter.END)
        entry_avatar.insert(0, avatar_path) """

    boton_SeleccionAvatar = tkinter.Button(ventaRegistro, text="Seleccionar Avatar", command=lambda: seleccionar_avatar(entry_avatar))


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

        except sqlite3.IntegrityError:
            messagebox.showerror("ERROR", "El nombre de usuario ya existe")

    botonRegistro = tkinter.Button(ventaRegistro,text="Registar",command=insertar)
    boton_SeleccionAvatar.pack(pady=10)
    botonRegistro.pack(pady=10)


def seleccionar_avatar(entry):
    avatar_path = filedialog.askopenfilename(initialdir="./avatar", title="Seleccionar Avatar", filetypes=(
    ("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")))
    entry.delete(0, tkinter.END)
    entry.insert(0, avatar_path)

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
            global idUserLogeado
            idUserLogeado = user[0]
            messagebox.showinfo("Login","Login exitoso")
            actualizarFrame(frame, nick, user[3], user[4], user[5])
            EncenderStart(ventana)
        return True
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")
        return False

def partidaEmpezada():
    messagebox.showinfo("Partida","Partida empezada")


def contadorFallos(ventana):
    global fallos
    fallos += 1
    if fallos >= 3:
        messagebox.showerror("Login", "Tres intentos fallidos, el programa se cerrará")
        ventana.destroy()

def actualizarFrame(frame, nick, avatar, partidas_jugadas, partidas_ganadas):
    # Destruye todos los widgets del frame
    limpiarFrame(frame)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(6, weight=1)
    
    label_nick = tkinter.Label(frame, text=nick)
    label_nick.grid(row=0, column=3, columnspan=2, sticky='nsew')

    label_avatar = tkinter.Label(frame)
    label_avatar.avatar_image = tkinter.PhotoImage(file=avatar)  # Asigna la imagen a un atributo del widget
    label_avatar.config(image=label_avatar.avatar_image)
    label_avatar.grid(row=1, column=3, columnspan=2, sticky='nsew')

    label_partidas = tkinter.Label(frame, text=f"Partidas jugadas: {partidas_jugadas}")
    label_partidas.grid(row=2, column=3, columnspan=2, sticky='nsew')

    # Calcular el porcentaje de partidas ganadas
    porcentaje_ganadas = porcentajePartidasGanadas(nick)

    label_ganadas = tkinter.Label(frame, text=f"Partidas ganadas: {porcentaje_ganadas}%")
    label_ganadas.grid(row=3, column=3, columnspan=2, sticky='nsew')

    botonModificar = tkinter.Button(frame, text="Modificar datos", command=modificarDatos)
    botonModificar.grid(row=4, column=3, pady=10, columnspan=2, sticky='nsew')

    botonEliminar = tkinter.Button(frame, text="Eliminar usuario", command=lambda: eliminarUsuario(frame))
    botonEliminar.grid(row=5, column=3, pady=10, columnspan=2, sticky='nsew')

    botonReload = tkinter.Button(frame, text="Recargar", command=lambda: recargaFrame(frame, nick, avatar, partidas_jugadas, partidas_ganadas))
    botonReload.grid(row=1, column=6, pady=10)
    
    frame.update()

""" def centrar_widgets_en_frame(frame):
    for child in frame.winfo_children():
        child.grid_configure(padx=10, pady=10, sticky='nsew')  """   

def recargaFrame(frame, nick, avatar, partidas_jugadas, partidas_ganadas):
    limpiarFrame(frame)
    user = obtenerUsuario(idUserLogeado)
    actualizarFrame(frame, user[1], user[3], user[4], user[5])   

def EncenderStart(ventana):
    global usuariosLogeados
    usuariosLogeados += 1
    if usuariosLogeados == 2:
        ventana.botonStart.config(state=tkinter.NORMAL)
    

def porcentajePartidasGanadas(nick):
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()

        # Obtener el número total de partidas jugadas y el número de partidas ganadas
        cur.execute("SELECT partidas_jugadas, partidas_ganadas FROM Usuario WHERE nick = ?", (nick,))
        user = cur.fetchone()

        conexion.close()

        if user is not None and user[0] != 0:
            # Calcular y devolver el porcentaje de partidas ganadas
            return (user[1] / user[0]) * 100
        else:
            # Si no se pueden encontrar partidas, devolver 0
            return 0
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")
        return 0


def modificarDatos():
    ventaModificacion = tkinter.Toplevel()
    ventaModificacion.title("Modificar Usuario")
    ancho = 500
    largo = 100
    ventaModificacion.geometry(f"{ancho}x{largo}")

    label_nick = tkinter.Label(ventaModificacion, text="Nick:")
    entry_nick = tkinter.Entry(ventaModificacion)
    bModificarNick = tkinter.Button(ventaModificacion,text="Modificar Nick",command=lambda:nickUpdade(entry_nick))

    label_password = tkinter.Label(ventaModificacion, text="Password:")
    entry_password = tkinter.Entry(ventaModificacion)
    bModificarPass = tkinter.Button(ventaModificacion,text="Modificar Password",command=lambda:passwordUpdate(entry_password))

    label_avatar = tkinter.Label(ventaModificacion, text="Avatar (ruta de la imagen):")
    entry_avatar = tkinter.Entry(ventaModificacion)
    boton_SeleccionAvatar = tkinter.Button(ventaModificacion, text="Seleccionar Avatar",command=lambda:seleccionar_avatar(entry_avatar))
    bModificarAvatar = tkinter.Button(ventaModificacion,text="Modificar Avatar",command=lambda:avatarUpdate(entry_avatar))

    label_nick.grid(row=0, column=0)
    entry_nick.grid(row=0, column=1)
    bModificarNick.grid(row=0, column=2)

    label_password.grid(row=1, column=0)
    entry_password.grid(row=1, column=1)
    bModificarPass.grid(row=1, column=2)

    label_avatar.grid(row=2, column=0)
    entry_avatar.grid(row=2, column=1)
    boton_SeleccionAvatar.grid(row=2, column=2)
    bModificarAvatar.grid(row=2, column=3)

    ventaModificacion.grid()


def nickUpdade(entry_nick):
    nick = entry_nick.get()
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("UPDATE Usuario SET nick = ? WHERE id = ?", (nick, idUserLogeado))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Exito", "Usuario actualizado exitosamente")
        

        
        
    except sqlite3.IntegrityError:
        messagebox.showerror("ERROR", "No se puede actualizar el nick, ya existe otro usuario con ese nick")


def passwordUpdate(entry_password):
    password = entry_password.get()
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("UPDATE Usuario SET password = ? WHERE id = ?", (password, idUserLogeado))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Exito", "Usuario actualizado exitosamente")
        

    except sqlite3.IntegrityError:
        messagebox.showerror("ERROR", "No se pudo actualizar la contraseña")

def avatarUpdate(entry_avatar):
    avatar = entry_avatar.get()
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("UPDATE Usuario SET avatar = ? WHERE id = ?", (avatar, idUserLogeado))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Exito", "Usuario actualizado exitosamente")
        

    except sqlite3.IntegrityError:
        messagebox.showerror("ERROR", "No se pudo actualizar el avatar")        

def eliminarUsuario(frame):

    global idUserLogeado

    if idUserLogeado is None:
        messagebox.showerror("ERROR", "No hay ningún usuario logeado")
        return
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("DELETE FROM Usuario WHERE id = ?", (idUserLogeado,))
        conexion.commit()
        conexion.close()

        limpiarFrame(frame)

        if frame.cget("bg") == "blue":
            primerFrame(frame) 
        else:
            segundoFrame(frame)          
        
        
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")




def limpiarFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def obtenerUsuario(id):
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("SELECT * FROM Usuario WHERE id = ?", (id,))
        user = cur.fetchone()
        conexion.close()
        return user
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")
        return None       