import tkinter
from persistencia import crearBaseDatos
from funciones import registraUsuario,login,primerFrame,segundoFrame,partidaEmpezada

#------------------------------------------------------------------------------------------
""" Esta es el main donde se ejecuta el programa, se importan las funciones necesarias para su funcionamiento. 
Como podras ver se crea la ventana principal y se le asignan unos frames ademas de los
botones crear usuario y empezar partida. """
#-----------------------------------------------------------------------------------------

# Esta funcion crea la base de datos si no existe
crearBaseDatos()

#------------------------------------------------------------------------------------------
# Configuracion de la ventana principal con su titulo y tamaño
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

# Aqui tenemos el primer frame que se muestra en la ventana principal

primerFrame(ventana)
# -------------------------------------------------------------------------------------

# Aqui tenemos el segundo frame que se muestra en la ventana principal

segundoFrame(ventana)

#---------------------------------------------------------------------------------------
""" Aqui estan los botones mencionados arriba donde el boton crear usuario llama a la funcion registraUsuario
que permite crear un usuario nuevo y el boton empezar partida llama a la funcion partidaEmpezada para 
iniciar el juego """
#---------------------------------------------------------------------------------------
botonCrear = tkinter.Button(ventana,text="Crear Usuario",command=registraUsuario, width=20)
botonCrear.pack(side=tkinter.BOTTOM, pady=10)
ventana.botonStart = tkinter.Button(ventana,text="Empezar partida",state=tkinter.DISABLED,command=partidaEmpezada, width=20)
ventana.botonStart.pack(side=tkinter.BOTTOM)


# El mainloop es el que permite que la ventana se mantenga abierta
ventana.mainloop()


