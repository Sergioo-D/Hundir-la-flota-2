import sqlite3
import os
from tkinter import messagebox

def crearBaseDatos():
    try:
        if not os.path.exists("./bbdd/"):
            os.makedirs("./bbdd/")

        conexion = conectarBBDD()
        cur = conexion.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Usuario(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nick TEXT,
                      password TEXT,
                      avatar BLOB,
                      partidas_jugadas INTEGER,
                      partidas_ganadas INTEGER) """)

        conexion.commit()
        conexion.close()
    except:
        messagebox.showerror("ERROR","Error al conectar con la base de datos")



def conectarBBDD():
    try:
        connection = sqlite3.connect("./bbdd/hundirFlota.db")
        return connection
    except:
        messagebox.showerror("ERROR", "Error al conectar con la base de datos")

