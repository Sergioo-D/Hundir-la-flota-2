import tkinter
from persistencia import crearBaseDatos
from funciones import registraUsuario,login,primerFrame,segundoFrame



crearBaseDatos()

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

botonCrear = tkinter.Button(ventana,text="Crear Usuario",command=registraUsuario)
botonCrear.pack(side=tkinter.BOTTOM, pady=10)
botonStart = tkinter.Button(ventana,text="Empezar partida",state=tkinter.DISABLED)
botonStart.pack(side=tkinter.BOTTOM)



ventana.mainloop()


