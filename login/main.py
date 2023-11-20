import tkinter
from persistencia import crearBaseDatos
from funciones import registraUsuario,login


crearBaseDatos()

ventana = tkinter.Tk()
ventana.title("Login")
ventana.resizable(False,False)

anchoPantalla = ventana.winfo_screenwidth()
largoPantalla = ventana.winfo_screenheight()
ancho = 800
largo = 600
x = (anchoPantalla - ancho) //2
y = (largoPantalla - largo) //2
ventana.geometry(f"{ancho}x{largo}+{x}+{y}")
#------------------------------------------------------------------------------------------

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
# -------------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------

botonCrear = tkinter.Button(ventana,text="Crear Usuario",command=registraUsuario)
botonCrear.pack(side=tkinter.BOTTOM, pady=10)
botonStart = tkinter.Button(ventana,text="Empezar partida",state=tkinter.DISABLED)
botonStart.pack(side=tkinter.BOTTOM)
botonEntrar = tkinter.Button(frameJ1, text="Entrar", command=lambda: login(entry_nickJ1.get(), entry_passwordJ1.get(),ventana,
                                                                           frameJ1))
botonEntrar.pack(side=tkinter.BOTTOM, pady=10)
botonEntrar = tkinter.Button(frameJ2, text="Entrar", command=lambda: login(entry_nickJ2.get(), entry_passwordJ2.get(),ventana,
                                                                           frameJ2))
botonEntrar.pack(side=tkinter.BOTTOM, pady=10)

ventana.mainloop()


