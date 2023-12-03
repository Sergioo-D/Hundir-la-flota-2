import sqlite3
import os
from datetime import time
from tkinter import messagebox


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
                      movimientos INTEGER,
                      tiempo TEXT) """)

        conexion.commit()
        conexion.close()
    except Exception as e:
        messagebox.showerror("ERROR", f"Error: {e}")
        return None


def conectarBBDD():
    try:
        connection = sqlite3.connect("./bbdd/hundirFlota.db")
        return connection
    except Exception as e:
        messagebox.showerror("ERROR", f"Error: {e}")
        return None


def obtenerUsuario(id):
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("SELECT * FROM Usuario WHERE id = ?", (id,))
        user = cur.fetchone()
        conexion.close()
        return user
    except Exception as e:
        messagebox.showerror("ERROR", f"Error: {e}")
        return None


def updatePartidasJugadas(id):
    try:
        conexion = conectarBBDD()
        cur = conexion.cursor()
        cur.execute("UPDATE Usuario SET partidas_jugadas = partidas_jugadas + 1 WHERE id = ?", (id,))
        conexion.commit()
        conexion.close()
    except Exception as e:
        messagebox.showerror("ERROR PARTIDASJUG", f"Error: {e}")
        return None


def updateMovimientos(id, movimientos):
    user = obtenerUsuario(id)
    try:
        if int(user[5]) == 0 or movimientos < int(user[5]):
            conexion = conectarBBDD()
            cur = conexion.cursor()
            cur.execute("UPDATE Usuario SET movimientos = ? WHERE id = ?", (movimientos, id))
            conexion.commit()
            conexion.close()
    except Exception as e:
        messagebox.showerror("ERROR movimientos", f"Error: {e}")
        return None

def updateTiempo(id, tiempo):
    user = obtenerUsuario(id)
    try:
        if (user[6]) == "0" or tiempo < user[6]:
            conexion = conectarBBDD()
            cur = conexion.cursor()
            cur.execute("UPDATE Usuario SET tiempo = ? WHERE id = ?", (tiempo, id))
            conexion.commit()
            conexion.close()
    except Exception as e:
        messagebox.showerror("ERROR tiempo", f"Error: {e}")
        return None

