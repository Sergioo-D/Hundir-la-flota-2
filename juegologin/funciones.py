import random
import tkinter
import sqlite3
from tkinter import Tk, filedialog,messagebox
from persistencia import conectarBBDD,obtenerUsuario





fallos = 0
usuariosLogeados= 0
idUserLogeado = id
global label_nickk, label_aavatar,label_imagenAvatar,ventana,window




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



def partidaEmpezada(ventana):
    obtenerUsuario(idUserLogeado)
    elJuego(idUserLogeado)
    


def contadorFallos(ventana):
    global fallos
    fallos += 1
    if fallos >= 3:
        messagebox.showerror("Login", "Tres intentos fallidos, el programa se cerrará")
        ventana.destroy()

def actualizarFrame(frame, nick, avatar, partidas_jugadas, partidas_ganadas):
    # Destruye todos los widgets del frame
    limpiarFrame(frame)

    global label_nickk, label_aavatar
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(6, weight=1)
    
    label_nickk = tkinter.Label(frame, text=nick)
    label_nickk.grid(row=0, column=3, columnspan=2, sticky='nsew')

    label_aavatar = tkinter.Label(frame)
    label_aavatar.avatar_image = tkinter.PhotoImage(file=avatar)  # Asigna la imagen a un atributo del widget
    label_aavatar.config(image=label_aavatar.avatar_image)
    label_aavatar.grid(row=1, column=3, columnspan=2, sticky='nsew')

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

    return label_nickk, label_aavatar
    
    frame.update()

  

def recargaFrame():
    global label_nickk, label_aavatar
    user = obtenerUsuario(idUserLogeado)
    
    label_nickk.config(text=user[1])
    label_aavatar.config(image=tkinter.PhotoImage(file=user[3]))
    nuevaImagen = tkinter.PhotoImage(file=user[3])
    label_aavatar.config(image=nuevaImagen)
    label_aavatar.image = nuevaImagen 
    
  
    
    
     

def EncenderStart(ventana):
    global usuariosLogeados
    usuariosLogeados += 1
    if usuariosLogeados == 1:
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


import tkinter

def modificarDatos():
    global label_imagenAvatar
    ventaModificacion = tkinter.Toplevel()
    ventaModificacion.title("Modificar Usuario")
    ancho = 700
    largo = 300
    ventaModificacion.geometry(f"{ancho}x{largo}")

    # Etiquetas y entradas para modificar el Nick
    label_nick = tkinter.Label(ventaModificacion, text="Nick:")
    entry_nick = tkinter.Entry(ventaModificacion)
    entry_nick.insert(0, obtenerUsuario(idUserLogeado)[1])
    bModificarNick = tkinter.Button(ventaModificacion, text="Modificar Nick", command=lambda: nickUpdade(entry_nick), width=20)

    # Etiquetas y entradas para modificar la contraseña
    label_password = tkinter.Label(ventaModificacion, text="Password:")
    entry_password = tkinter.Entry(ventaModificacion)
    bModificarPass = tkinter.Button(ventaModificacion, text="Modificar Password", command=lambda: passwordUpdate(entry_password), width=20)

    # Mostrar la imagen de Avatar
    avatarUsuario = obtenerUsuario(idUserLogeado)[3]
    avatarDelUsuario = tkinter.PhotoImage(file=avatarUsuario)
    label_imagenAvatar = tkinter.Label(ventaModificacion, image=avatarDelUsuario)
    label_imagenAvatar.image = avatarDelUsuario

    # Etiquetas y entradas para modificar el Avatar
    label_avatar = tkinter.Label(ventaModificacion, text="Avatar (ruta de la imagen):")
    entry_avatar = tkinter.Entry(ventaModificacion)
    boton_SeleccionAvatar = tkinter.Button(ventaModificacion, text="Seleccionar Avatar", command=lambda: seleccionar_avatar(entry_avatar), width=20)
    bModificarAvatar = tkinter.Button(ventaModificacion, text="Modificar Avatar", command=lambda: avatarUpdate(entry_avatar), width=20)

    # Botón para recargar la ventana
    botonReload = tkinter.Button(ventaModificacion, text="Recargar", command=lambda: recargaFrame())

    # Botón para cerrar la ventana de modificación
    botonCerrar = tkinter.Button(ventaModificacion, text="Cerrar", command=ventaModificacion.destroy, width=20)

    # Organización de los widgets en la ventana
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

    # Hacer que la imagen del Avatar y la columna 4 se expandan si la ventana se agranda.
    ventaModificacion.grid_rowconfigure(3, weight=1)
    ventaModificacion.grid_columnconfigure(4, weight=1)
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
    global label_imagenAvatar
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

    nuevoAvatar = obtenerUsuario(idUserLogeado)[3]
    actualizarAvatar = tkinter.PhotoImage(file=nuevoAvatar)
    label_imagenAvatar.config(image=actualizarAvatar)
    label_imagenAvatar.image = actualizarAvatar
             

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

def ventanaPrincipal():
    global ventana
    window.destroy()
    ventana = tkinter.Tk()
    ventana.title("Login")
    ventana.resizable(False,False)

    anchoPantalla = ventana.winfo_screenwidth()
    largoPantalla = ventana.winfo_screenheight()
    ancho = 800
    largo = 800
    x = (anchoPantalla - ancho) //2



    y = (largoPantalla - largo) //2
    ventana.geometry(f"{ancho}x{largo}+{x}+{y}")
        #------------------------------------------------------------------------------------------

    primerFrame(ventana)
        # -------------------------------------------------------------------------------------
    segundoFrame(ventana)

        #---------------------------------------------------------------------------------------

    botonCrear = tkinter.Button(ventana,text="Crear Usuario",command=registraUsuario, width=20)
    botonCrear.pack(side=tkinter.BOTTOM, pady=10)
    ventana.botonStart = tkinter.Button(ventana,text="Empezar partida",state=tkinter.DISABLED,command=lambda:elJuego(idUserLogeado), width=20)
    ventana.botonStart.pack(side=tkinter.BOTTOM)

    

    ventana.mainloop()

def elJuego(idUserLogeado):
    ventana.destroy()
    global window
    window = tkinter.Tk()
    window.title("Hundir la flota")
    rows = 6
    columns = 7
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    tablero = [[0] * 7 for _ in range(6)]
    global movimientos
    movimientos = 0
    barcos = [2, 3, 4]
    barcos_posiciones = {size: [] for size in barcos}
    barcos_impactados = {size: 0 for size in barcos}
    acierto = []
    user = obtenerUsuario(idUserLogeado)


    def crear_interfaz():
        global casillas_tablero
        casillas_tablero = []
        for i in range(rows):
            label_letras = tkinter.Label(window, text=letters[i], width=5, height=2, bg="grey")
            label_letras.grid(row=i + 1, column=0)
            filas_tablero = []

            for j in range(columns):
                label_nums = tkinter.Label(window, text=str(j + 1), width=11, height=2, bg="grey")
                label_nums.grid(row=0, column=j + 1)
                global label_tablero
                label_tablero = tkinter.Label(window, borderwidth=1, relief='solid', width=11, height=2)
                label_tablero.grid(row=i + 1, column=j + 1)
                filas_tablero.append(label_tablero)
            casillas_tablero.append(filas_tablero)

        b_dispara = tkinter.Button(window, text="Dispara", width=10, command=dispara)
        b_dispara.grid(row=10, column=4)
        b_nueva_partida = tkinter.Button(window, text="Nueva partida", width=10, command=nueva_partida)
        b_nueva_partida.grid(row=10, column=7)
        b_cerrar = tkinter.Button(window, text="Cerrar", width=10, command=window.destroy)
        b_cerrar.grid(row=11, column=7)
        l_hint = tkinter.Label(window, text="Introduce letra:")
        n_hint = tkinter.Label(window, text="Introduce numero:")
        l_hint.grid(row=10, columnspan=2, column=1)
        n_hint.grid(row=11, columnspan=2, column=1)
        global l_casilla, n_casilla
        l_casilla = tkinter.Entry(window, width=11)
        l_casilla.grid(row=10, column=3)
        n_casilla = tkinter.Entry(window, width=11)
        n_casilla.grid(row=11, column=3)
        global contador_movimientos
        contador_movimientos = tkinter.Label(window, text="Moviments: 0")
        contador_movimientos.grid(row=11, column=4)
        global l_jugador
        l_jugador = tkinter.Label(window, text=f"Turno {user[1]}: 0")
        l_jugador.grid(row=10, column=5, columnspan=2)
        botonCambiarJugador = tkinter.Button(window, text="Cambiar de jugador", width=15, command=ventanaPrincipal)
        botonCambiarJugador.grid(row=10, column=7)

    
        
        
        
        
    def iniciar_barcos():
        for barco in barcos:
            cabe = False
            while not cabe:
                orientacion = random.choice(['horizontal', 'vertical'])
                if orientacion == 'horizontal':
                    fila = random.randint(0, 5)
                    columna = random.randint(0, 6 - barco)
                    if all(tablero[fila][columna + i] == 0 for i in range(barco)):
                        for i in range(barco):
                            tablero[fila][columna + i] = 1
                            posicion = [fila, columna + i]
                            casillas_tablero[fila][columna + i].config(bg="red")
                            barcos_posiciones[barco].append(posicion)
                        cabe = True
                else:  # orientacion == 'vertical'
                    fila = random.randint(0, 5 - barco)
                    columna = random.randint(0, 6)
                    if all(tablero[fila + i][columna] == 0 for i in range(barco)):
                        for i in range(barco):
                            tablero[fila + i][columna] = 1
                            posicion = [fila + i, columna]
                            casillas_tablero[fila + i][columna].config(bg="red")
                            barcos_posiciones[barco].append(posicion)
                        cabe = True

        # Mostrar el tablero en la consola (para verificar)
        for fila in tablero:
            print(fila)


    def dispara():
        global movimientos
        valores = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
        letra = l_casilla.get().capitalize()
        num = n_casilla.get()
        if letra != "" and num != "":
            if num.isnumeric():
                if letra in valores:
                    if 1 <= int(num) <= columns:
                        fila = valores[letra]
                        columna = int(num) - 1
                        if tablero[fila][columna] == 1:  # Si hay un barco en la casilla impactada
                            movimientos += 1
                            contador_movimientos.config(text=f"Moviments: {movimientos}")
                            l_jugador.config(text=f"Turno {user[1]}: {movimientos}")
                            if casillas_tablero[fila][columna] not in acierto:
                                casillas_tablero[fila][columna].config(bg="orange")
                                acierto.append(casillas_tablero[fila][columna])
                                # Buscar el tamaño del barco impactado y actualizar el contador de partes impactadas
                                for size in barcos:
                                    if [fila, columna] in barcos_posiciones[size]:
                                        barcos_impactados[size] += 1
                                        if barcos_impactados[size] == size:
                                            # Cambiar el fondo de todas las partes del barco a negro
                                            for pos in barcos_posiciones[size]:
                                                casillas_tablero[pos[0]][pos[1]].config(bg="black")
                                win()
                            else:
                                movimientos -= 1
                                contador_movimientos.config(text=f"Moviments: {movimientos}")
                                l_jugador.config(text=f"Turno {user[1]}: {movimientos}")
                        else:  # If it's a water cell
                            if casillas_tablero[fila][columna].cget('bg') != 'blue':  # If it hasn't been shot at
                                movimientos += 1
                                contador_movimientos.config(text=f"Moviments: {movimientos}")
                                l_jugador.config(text=f"Turno {user[1]}: {movimientos}")
                                casillas_tablero[fila][columna].config(bg="blue")
                    else:
                        messagebox.showerror("Ventana de error", "El campo número es incorrecto")
                else:
                    messagebox.showerror("Ventana de error", "El campo letra es incorreto")
            else:
                messagebox.showerror("Ventana de error", "El campo número no es un número")
        else:
            messagebox.showerror("ventana de error", "Debe rellenar los dos campos")


    def nueva_partida():
        global movimientos
        movimientos = 0
        crear_interfaz()
        iniciar_barcos()


    def win():
        contador = 0
        for size in barcos:
            if barcos_impactados[size] == size:
                contador += 1
        if contador == len(barcos):
            messagebox.showinfo("Ventana info", "Has ganado en " + str(movimientos) + "movimientos!")


    crear_interfaz()
    iniciar_barcos()

    window.mainloop()