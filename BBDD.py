import os.path
import sqlite3



def crear_tabla():
    if not os.path.exists("./bd_hundir_la_flota"):
        os.mkdir("./bd_hundir_la_flota")
    var_BD = sqlite3.connect("./bd_hundir_la_flota" + "hundir_la_flota.db")
    cursor_BD = var_BD.cursor()
    cursor_BD.execute("""CREATE TABLE IF NOT EXISTS jugadors(nick text, password text, avatar text, partides_jugades integer, partides_guanyades integer)""")
    cursor_BD.execute("INSERT INTO jugadors(nick, password, avatar, partides_jugades, partides_guanyades) VALUES (?,?,?,?,?)")
