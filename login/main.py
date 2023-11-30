import tkinter
from persistencia import crearBaseDatos
from funciones import registraUsuario,login,primerFrame,segundoFrame,partidaEmpezada



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

botonCrear = tkinter.Button(ventana,text="Crear Usuario",command=registraUsuario, width=20)
botonCrear.pack(side=tkinter.BOTTOM, pady=10)
ventana.botonStart = tkinter.Button(ventana,text="Empezar partida",state=tkinter.DISABLED,command=partidaEmpezada, width=20)
ventana.botonStart.pack(side=tkinter.BOTTOM)



ventana.mainloop()


