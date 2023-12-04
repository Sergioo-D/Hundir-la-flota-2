import sqlite3
import os
from tkinter import messagebox
#------------------------------------------------------------------------------------------
# Esta funcion crea la base de datos si no existe y crea la tabla usuario con los campos que 
#puedes ver 
def crearBaseDatos():
    try:
        if not os.path.exists("./bbdd/"):
            os.makedirs("./bbdd/")

        conexion = conectarBBDD()
        cur = conexion.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Usuario(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nick TEXT UNIQUE,
                      password TEXT,
                      avatar BLOB,
                      partidas_jugadas INTEGER,
                      partidas_ganadas INTEGER) """)

        conexion.commit()
        conexion.close()
    except:
        messagebox.showerror("ERROR","Error al conectar con la base de datos")


#------------------------------------------------------------------------------------------
# Esta funcion conecta con la base de datos y devuelve la conexion si no hay errores
def conectarBBDD():
    try:
        connection = sqlite3.connect("./bbdd/hundirFlota.db")
        return connection
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")

