import tkinter
import sqlite3
from tkinter import filedialog,messagebox
from persistencia import conectarBBDD

#------------------------------------------------------------------------------------------
""" En este archivo se encuentran todas las funciones que se utilizan para el login a excepcion de las
que estan en persistencia.py """
# ------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
"Estas de aqui son variables globales que se utilizan en las funciones y se han considerado necesarias"

fallos = 0
usuariosLogeados= 0
idUserLogeado = None
user_log = {}
global label_nickk, label_aavatar,label_imagenAvatar
#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
"""Los frames dividen la pantalla en dos partes, en la parte de arriba se muestra el frame del jugador 1
y en la parte de abajo el frame del jugador 2. En cada frame se muestra un campo para introducir el nick
y otro para introducir la contraseña. Tambien hay un boton para entrar que llama a la funcion login """

def primerFrame(ventana):
    frameJ1 = tkinter.Frame(ventana, bg="blue")
    frameJ1.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    label_nickJ1 = tkinter.Label(frameJ1, text="Nick:")
    label_nickJ1.pack(pady=5)
    entry_nickJ1 = tkinter.Entry(frameJ1)
    entry_nickJ1.pack(pady=5)

    label_passwordJ1 = tkinter.Label(frameJ1, text="Password:")
    label_passwordJ1.pack(pady=5)
    entry_passwordJ1 = tkinter.Entry(frameJ1, show="*")
    entry_passwordJ1.pack(pady=5)

    botonEntrar = tkinter.Button(frameJ1, text="Entrar", command=lambda: login(entry_nickJ1.get(), entry_passwordJ1.get(), ventana, frameJ1))
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
    entry_passwordJ2 = tkinter.Entry(frameJ2, show="*")
    entry_passwordJ2.pack(pady=5)

    botonEntrar = tkinter.Button(frameJ2, text="Entrar", command=lambda: login(entry_nickJ2.get(), entry_passwordJ2.get(), ventana, frameJ2))
    botonEntrar.pack(side=tkinter.BOTTOM, pady=10)
#------------------------------------------------------------------------------------------        
""" Esta es la funcion que permite crear nuevos usuarios , cuando pulsas el boton registrar se abre una
 ventana Toplevel donde se introducen los datos del usuario y se insertan en la base de datos. Consta de 
 un nick, una contraeña y un avatar, este ultimo se selecciona con un boton que llama a la funcion
seleccionar_avatar y esta abre un filedialog para seleccionar la imagen deseada. Hemos puesto la posibilidad
de seleccionar 5 avatares diferentes. Una vez escrito el nick, la contraseña y la ruta donde se encuentra
el avatar se pulsa el boton registrar y se insertan los datos en la base de datos. Ademas se comprueba que
el nick no este repetido en la base de datos.
 """
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
#------------------------------------------------------------------------------------------
"""Esta funcion es la que permite logearse a los usuarios, cuando se pulsa el boton entrar se llama a esta
funcion que comprueba si el usuario esta en la base de datos y si la contraseña es correcta. Si el usuario
esta en la base de datos se muestra un mensaje de login exitoso y se actualiza el frame con los datos del
usuario. Si el usuario no esta en la base de datos se muestra un mensaje de error y se llama a la funcion
contadorFallos que comprueba si se han introducido 3 usuarios erroneos y si es asi se cierra el programa."""

def login(nick, password, ventana, frame):
    global idUserLogeado, usuariosLogeados

    # aqui comprobamos si el usuario ya esta logeado
    if nick in user_log.get(frame, set()):
        messagebox.showerror("Login", "El usuario ya está logeado")
        return False 

    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()

        cur.execute("SELECT * FROM Usuario WHERE nick = ? AND password = ?", (nick, password))
        user = cur.fetchone()

        conexion.close()

        # si no existe el usuario en la base de datos se muestra un mensaje de error
        if user is None:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")
            contadorFallos(ventana)
            return False
        else:
            # si el usuario existe se muestra un mensaje de login exitoso y se actualiza el frame
            idUserLogeado = user[0]
            user_log[frame] = {'nick': nick, 'avatar': user[3], 'partidas_jugadas': user[4], 'partidas_ganadas': user[5]}
            messagebox.showinfo("Login", "Login exitoso")
            actualizarFrame(frame, nick, user[3], user[4], user[5])
            EncenderStart(ventana)
        return True
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")
        return False
#------------------------------------------------------------------------------------------

# A falta del juego esta funcion muestra un mensaje de partida empezada y ya.
def partidaEmpezada():
    messagebox.showinfo("Partida","Partida empezada")

#------------------------------------------------------------------------------------------
# Esta funcion comprueba si has errado 3 veces el login y si es asi cierra el programa
def contadorFallos(ventana):
    global fallos
    fallos += 1
    if fallos >= 3:
        messagebox.showerror("Login", "Tres intentos fallidos, el programa se cerrará")
        ventana.destroy()
#------------------------------------------------------------------------------------------
"""Esta funcion actualiza el frame con los datos del usuario que se ha logeado. Se muestra
el nick, el avatar, las partidas jugadas y las partidas ganadas. Tambien hay dos botones, uno para modificar
los datos del usuario y otro para eliminar el usuario."""

def actualizarFrame(frame, nick, avatar, partidas_jugadas, partidas_ganadas):
    # limpiarFrame limpia como su nombre indica el frame para que no se muestren los datos del usuario
    #  anterior
    limpiarFrame(frame)
    
    global label_nickk, label_aavatar
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(6, weight=1)

    label_nickk = tkinter.Label(frame, text=nick)
    label_nickk.grid(row=0, column=3, columnspan=2, sticky='nsew')

    label_aavatar = tkinter.Label(frame)
    label_aavatar.avatar_image = tkinter.PhotoImage(file=avatar)
    label_aavatar.config(image=label_aavatar.avatar_image)
    label_aavatar.grid(row=1, column=3, columnspan=2, sticky='nsew')

    label_partidas = tkinter.Label(frame, text=f"Partidas jugadas: {partidas_jugadas}")
    label_partidas.grid(row=2, column=3, columnspan=2, sticky='nsew')

    porcentaje_ganadas = porcentajePartidasGanadas(nick)

    label_ganadas = tkinter.Label(frame, text=f"Partidas ganadas: {porcentaje_ganadas}%")
    label_ganadas.grid(row=3, column=3, columnspan=2, sticky='nsew')

    # aqui los botones de modificar y eliminar usuario
    botonModificar = tkinter.Button(frame, text="Modificar datos", command=lambda: modificarDatos(frame))
    botonModificar.grid(row=4, column=3, pady=10, columnspan=2, sticky='nsew')

    botonEliminar = tkinter.Button(frame, text="Eliminar usuario", command=lambda: eliminarUsuario(frame))
    botonEliminar.grid(row=5, column=3, pady=10, columnspan=2, sticky='nsew')


  #------------------------------------------------------------------------------------------
  # Esta funcion recarga el frame con los datos del usuario que se ha modificado
def recargaFrame(frame):
    global label_nickk, label_aavatar
    user = obtenerUsuario(idUserLogeado)

    label_nickk.config(text=user[1])
    label_aavatar.config(image=tkinter.PhotoImage(file=user[3]))
    nuevaImagen = tkinter.PhotoImage(file=user[3])
    label_aavatar.config(image=nuevaImagen)
    label_aavatar.image = nuevaImagen
    
  
   #------------------------------------------------------------------------------------------ 
    # Esta funcion enciende el boton de empezar partida cuando se han logeado dos usuarios, comprueba
    # si hay dos usuarios logeados y si es asi enciende el boton de no haber dos usuarios logeados no 
    #cambia el boton de empezar partida
def EncenderStart(ventana):
    global usuariosLogeados
    usuariosLogeados += 1
    if usuariosLogeados == 2:
        ventana.botonStart.config(state=tkinter.NORMAL)
    
#------------------------------------------------------------------------------------------
# Esta funcion calcula el porcentaje de partidas ganadas del usuario con un pequeño calculo matematico
def porcentajePartidasGanadas(nick):
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()

        cur.execute("SELECT partidas_jugadas, partidas_ganadas FROM Usuario WHERE nick = ?", (nick,))
        user = cur.fetchone()

        conexion.close()

        if user is not None and user[0] != 0:
            return (user[1] / user[0]) * 100
        else:
            return 0
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")
        return 0


#------------------------------------------------------------------------------------------
""" Esta funcion abre una ventana Toplevel donde permite modificar los datos del usuario. Se puede modificar
el nick, la contraseña y el avatar. Para modificar el nick y la contraseña se introduce el nuevo nick o la
nueva contraseña en el campo correspondiente y se pulsa el boton modificar nick o modificar contraseña. Para
modificar el avatar se introduce la ruta donde se encuentra el nuevo avatar en el campo correspondiente y se
pulsa el boton modificar avatar. Ademas hay un boton para recargar el frame y otro boton para cerrar la
ventana."""

def modificarDatos(frame):
    #creación de la ventana
    global label_imagenAvatar
    ventaModificacion = tkinter.Toplevel()
    ventaModificacion.title("Modificar Usuario")
    ancho = 700
    largo = 300
    ventaModificacion.geometry(f"{ancho}x{largo}")
    # añadimos los labels y entrys
    label_nick = tkinter.Label(ventaModificacion, text="Nick:")
    entry_nick = tkinter.Entry(ventaModificacion)
    entry_nick.insert(0, user_log[frame]['nick'])
    bModificarNick = tkinter.Button(ventaModificacion, text="Modificar Nick", command=lambda: nickUpdade(entry_nick, frame), width=20)

    label_password = tkinter.Label(ventaModificacion, text="Password:")
    entry_password = tkinter.Entry(ventaModificacion)
    bModificarPass = tkinter.Button(ventaModificacion, text="Modificar Password", command=lambda: passwordUpdate(entry_password), width=20)

    avatarDelUsuario = tkinter.PhotoImage(file=user_log[frame]['avatar'])
    label_imagenAvatar = tkinter.Label(ventaModificacion, image=avatarDelUsuario)
    label_imagenAvatar.image = avatarDelUsuario

    label_avatar = tkinter.Label(ventaModificacion, text="Avatar (ruta de la imagen):")
    entry_avatar = tkinter.Entry(ventaModificacion)
    boton_SeleccionAvatar = tkinter.Button(ventaModificacion, text="Seleccionar Avatar", command=lambda: seleccionar_avatar(entry_avatar), width=20)
    bModificarAvatar = tkinter.Button(ventaModificacion, text="Modificar Avatar", command=lambda: avatarUpdate(entry_avatar, frame), width=20)

    # añadimos los botones de recargar y cerrar
    botonReload = tkinter.Button(ventaModificacion, text="Recargar", command=lambda: recargaFrame(frame))
    botonCerrar = tkinter.Button(ventaModificacion, text="Cerrar", command=ventaModificacion.destroy, width=20)

    # añadimos los widgets a la ventana
    label_nick.grid(row=0, column=0, pady=5)
    entry_nick.grid(row=0, column=1, pady=5)
    bModificarNick.grid(row=0, column=2, pady=5)

    label_password.grid(row=1, column=0, pady=5)
    entry_password.grid(row=1, column=1, pady=5)
    bModificarPass.grid(row=1, column=2, pady=5)

    label_avatar.grid(row=2, column=0, pady=5)
    entry_avatar.grid(row=2, column=1, pady=5)
    boton_SeleccionAvatar.grid(row=2, column=2, pady=5)
    bModificarAvatar.grid(row=2, column=3, pady=5)

    label_imagenAvatar.grid(row=3, column=0, columnspan=4, pady=10)

    botonReload.grid(row=4, column=0, pady=10)
    botonCerrar.grid(row=4, column=1, pady=10)
    
    ventaModificacion.grid_rowconfigure(3, weight=1)
    ventaModificacion.grid_columnconfigure(4, weight=1)
    ventaModificacion.grid()
#------------------------------------------------------------------------------------------
# Estas funciones permiten modificar los datos del usuario
def nickUpdade(entry_nick, frame):
    nick = entry_nick.get()
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("UPDATE Usuario SET nick = ? WHERE id = ?", (nick, idUserLogeado))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Exito", "Usuario actualizado exitosamente")
        user_log[frame]['nick'] = nick
    except sqlite3.IntegrityError:
        messagebox.showerror("ERROR", "No se puede actualizar el nick, ya existe otro usuario con ese nick")
        

        
        
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

def avatarUpdate(entry_avatar, frame):
    global label_imagenAvatar
    avatar = entry_avatar.get()
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("UPDATE Usuario SET avatar = ? WHERE id = ?", (avatar, idUserLogeado))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Exito", "Usuario actualizado exitosamente")
        user_log[frame]['avatar'] = avatar
    except sqlite3.IntegrityError:
        messagebox.showerror("ERROR", "No se pudo actualizar el avatar")

    nuevoAvatar = user_log[frame]['avatar']
    actualizarAvatar = tkinter.PhotoImage(file=nuevoAvatar)
    label_imagenAvatar.config(image=actualizarAvatar)
    label_imagenAvatar.image = actualizarAvatar
             
#------------------------------------------------------------------------------------------
# Esta funcion elimina el usuario de la base de datos por la id del usuario
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
        messagebox.showinfo("Exito", "Usuario eliminado exitosamente")
        # Dependiendo del frame donde borres el usuario se muestra el frame correspondiente otra vez
        if frame.cget("bg") == "blue":
            primerFrame(frame) 
        else:
            segundoFrame(frame)          
        
        
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")


#------------------------------------------------------------------------------------------
# Esta funcion limpia el frame de todo widget que tenga
def limpiarFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
#------------------------------------------------------------------------------------------
# Esta funcion obtiene el usuario de la base de datos por la id
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