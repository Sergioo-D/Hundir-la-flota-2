import random
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Hundir la flota")
rows = 6
columns = 7
letters = ['A', 'B', 'C', 'D', 'E', 'F']
tablero = [[0] * 7 for _ in range(6)]
movimientos = 0
barcos = [2, 3, 4]
barcos_posiciones = {size: [] for size in barcos}
barcos_impactados = {size: 0 for size in barcos}

def crear_interfaz():
    global casillas_tablero
    casillas_tablero = []
    for i in range(rows):
        for j in range(columns):
            label_tablero = tk.Label(window, borderwidth=1, relief='ridge', width=4, height=2, bg="light blue")
            label_tablero.grid(row=i + 1, column=j + 1)
            casillas_tablero.append(label_tablero)

    b_dispara = tk.Button(window, text="Dispara", width=10, command=dispara, bg="light green")
    b_dispara.grid(row=8, column=4, columnspan=2)
    b_nueva_partida = tk.Button(window, text="Nueva partida", width=10, command=nueva_partida, bg="light green")
    b_nueva_partida.grid(row=8, column=6, columnspan=2)
    b_cerrar = tk.Button(window, text="Cerrar", width=10, command=window.destroy, bg="salmon")
    b_cerrar.grid(row=9, column=6, columnspan=2)
    l_hint = tk.Label(window, text="Introduce letra:", bg="light grey")
    n_hint = tk.Label(window, text="Introduce número:", bg="light grey")
    l_hint.grid(row=8, column=1, columnspan=2)
    n_hint.grid(row=9, column=1, columnspan=2)
    global l_casilla, n_casilla
    l_casilla = tk.Entry(window, width=6)
    l_casilla.grid(row=8, column=3, columnspan=2)
    n_casilla = tk.Entry(window, width=6)
    n_casilla.grid(row=9, column=3, columnspan=2)
    global contador_movimientos
    contador_movimientos = tk.Label(window, text="Movimientos: 0", bg="light grey")
    contador_movimientos.grid(row=9, column=4, columnspan=2)

def iniciar_barcos():
    for barco in barcos:
        while True:
            orientacion = random.choice(['horizontal', 'vertical'])
            if orientacion == 'horizontal':
                fila = random.randint(0, 5)
                columna = random.randint(0, 6 - barco)
                if all(tablero[fila][columna + i] == 0 for i in range(barco)):
                    for i in range(barco):
                        tablero[fila][columna + i] = 1
                        posicion = [fila, columna + i]
                        casillas_tablero[(fila * columns) + columna + i].config(bg="navy")
                        barcos_posiciones[barco].append(posicion)
                    break
            else:  # orientacion == 'vertical'
                fila = random.randint(0, 5 - barco)
                columna = random.randint(0, 6)
                if all(tablero[fila + i][columna] == 0 for i in range(barco)):
                    for i in range(barco):
                        tablero[fila + i][columna] = 1
                        posicion = [fila + i, columna]
                        casillas_tablero[((fila + i) * columns) + columna].config(bg="navy")
                        barcos_posiciones[barco].append(posicion)
                    break

def dispara():
    global movimientos
    valores = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
    movimientos += 1
    contador_movimientos.config(text=f"Movimientos: {movimientos}")
    letra = l_casilla.get().capitalize()
    num = n_casilla.get()

    if letra != "" and num != "":
        if num.isnumeric():
            if letra in valores:
                if 1 <= int(num) <= 7:
                    fila = valores[letra]
                    columna = int(num) - 1
                    if tablero[fila][columna] == 1:
                        casillas_tablero[(fila * columns) + columna].config(bg="orange")
                        for i in barcos:
                            if [fila, columna] in barcos_posiciones[i]:
                                barcos_impactados[i] += 1
                                if barcos_impactados[i] == i:
                                    for pos in barcos_posiciones[i]:
                                        casillas_tablero[(pos[0] * columns) + pos[1]].config(bg="black")
                    else:
                        casillas_tablero[(fila * columns) + columna].config(bg="blue")
                else:
                    messagebox.showerror("Ventana de error", "El campo número es incorrecto")
            else:
                messagebox.showerror("Ventana de error", "El campo letra es incorrecto")
        else:
            messagebox.showerror("Ventana de error", "El campo número no es un número")
    else:
        messagebox.showerror("Ventana de error", "Debe rellenar los dos campos")

def nueva_partida():
    for widget in window.winfo_children():
        widget.destroy()
    crear_interfaz()
    iniciar_barcos()

crear_interfaz()
iniciar_barcos()

window.mainloop()
