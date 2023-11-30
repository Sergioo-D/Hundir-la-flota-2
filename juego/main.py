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
agua = tk.PhotoImage(file="../img_olas.png", )
acierto = []


def crear_interfaz():
    global casillas_tablero
    casillas_tablero = []
    for i in range(rows):
        label_letras = tk.Label(window, text=letters[i], width=5, height=2, bg="grey")
        label_letras.grid(row=i + 1, column=0)
        filas_tablero = []

        for j in range(columns):
            label_nums = tk.Label(window, text=str(j + 1), width=11, height=2, bg="grey")
            label_nums.grid(row=0, column=j + 1)
            global label_tablero
            label_tablero = tk.Label(window, borderwidth=1, relief='solid', width=11, height=2)
            label_tablero.grid(row=i + 1, column=j + 1)
            filas_tablero.append(label_tablero)
        casillas_tablero.append(filas_tablero)

    b_dispara = tk.Button(window, text="Dispara", width=10, command=dispara)
    b_dispara.grid(row=10, column=4)
    b_nueva_partida = tk.Button(window, text="Nueva partida", width=10, command=nueva_partida)
    b_nueva_partida.grid(row=10, column=7)
    b_cerrar = tk.Button(window, text="Cerrar", width=10, command=window.destroy)
    b_cerrar.grid(row=11, column=7)
    l_hint = tk.Label(window, text="Introduce letra:")
    n_hint = tk.Label(window, text="Introduce numero:")
    l_hint.grid(row=10, columnspan=2, column=1)
    n_hint.grid(row=11, columnspan=2, column=1)
    global l_casilla, n_casilla
    l_casilla = tk.Entry(window, width=11)
    l_casilla.grid(row=10, column=3)
    n_casilla = tk.Entry(window, width=11)
    n_casilla.grid(row=11, column=3)
    global contador_movimientos
    contador_movimientos = tk.Label(window, text="Moviments: 0")
    contador_movimientos.grid(row=11, column=4)
    global l_jugador
    l_jugador = tk.Label(window, text="Turno jugador 1: 0")
    l_jugador.grid(row=10, column=5, columnspan=2)


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
                    movimientos += 1
                    contador_movimientos.config(text=f"Moviments: {movimientos}")
                    l_jugador.config(text=f"Turno jugador 1: {movimientos}")
                    if tablero[fila][columna] == 1:  # Si hay un barco en la casilla impactada
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
                            l_jugador.config(text=f"Turno jugador 1: {movimientos}")
                    else:
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
