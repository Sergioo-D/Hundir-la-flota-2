import tkinter as tk
import random

class JocBatallaNaval:
    def __init__(self, master):
        self.master = master
        self.master.title("Batalla Naval")

        self.torn = 0
        self.moviments = 0

        self.taulell = [[0] * 7 for _ in range(6)]  # Taulell 6x7 inicialitzat amb zeros

        self.inicialitzar_vaixells()

        self.crear_interfície()

    def inicialitzar_vaixells(self):
        # Omple el taulell amb vaixells
        vaixells = [(2, "A"), (3, "B"), (4, "C")]

        for tamany, etiqueta in vaixells:
            fila, columna = random.randint(0, 5), random.randint(0, 6)
            while not self.es_posicio_valida(fila, columna, tamany):
                fila, columna = random.randint(0, 5), random.randint(0, 6)

            for i in range(tamany):
                if etiqueta == "A":
                    self.taulell[fila][columna + i] = etiqueta
                elif etiqueta == "B":
                    self.taulell[fila + i][columna] = etiqueta
                elif etiqueta == "C":
                    self.taulell[fila + i][columna] = etiqueta

    def es_posicio_valida(self, fila, columna, tamany):
        # Comprova si la posició és vàlida per col·locar un vaixell de la mida especificada
        if columna + tamany > 7:
            return False

        for i in range(tamany):
            if self.taulell[fila][columna + i] != 0:
                return False

        return True

    def crear_interfície(self):
        self.indicador_torn = tk.Label(self.master, text="Torn del Jugador 1", font=("Helvetica", 12))
        self.indicador_torn.grid(row=0, column=0, columnspan=7)

        self.taulell_botons = []
        for fila in range(6):
            fila_botons = []
            for columna in range(7):
                btn = tk.Button(self.master, width=4, height=2, command=lambda f=fila, c=columna: self.disparar(f, c))
                btn.grid(row=fila + 1, column=columna)
                fila_botons.append(btn)
            self.taulell_botons.append(fila_botons)

        self.comptador_torn = tk.Label(self.master, text="Moviments: 0", font=("Helvetica", 10))
        self.comptador_torn.grid(row=7, column=0, columnspan=7)

        self.nova_partida_btn = tk.Button(self.master, text="Nova Partida", command=self.nova_partida)
        self.nova_partida_btn.grid(row=8, column=0, columnspan=3)

        self.tancar_btn = tk.Button(self.master, text="Tancar", command=self.master.destroy)
        self.tancar_btn.grid(row=8, column=4, columnspan=3)

    def disparar(self, fila, columna):
        if self.taulell[fila][columna] == 0:
            self.taulell_botons[fila][columna].config(bg="blue")  # Aigua
        else:
            self.taulell_botons[fila][columna].config(bg="red")   # Vaixell

        self.moviments += 1
        self.comptador_torn.config(text=f"Moviments: {self.moviments}")

        if all(all(cell == 0 or cell == 'X' for cell in row) for row in self.taulell):
            tk.messagebox.showinfo("Victoria", f"Has guanyat en {self.moviments} moviments.")
            self.nova_partida()
            for i in range(len(self.taulell)):
                for j in range(len(self.taulell[i])):
                    if self.taulell[i][j] == 'X':  # Si hay un barco hundido en esta posición
                        self.taulell_botons[i][j].config(bg="black")

    def nova_partida(self):
        self.torn = 0
        self.moviments = 0
        self.taulell = [[0] * 7 for _ in range(6)]

        for fila_botons in self.taulell_botons:
            for btn in fila_botons:
                btn.config(bg="SystemButtonFace")

        self.comptador_torn.config(text="Moviments: 0")
        tk.messagebox.showinfo("Nova Partida", "Nova partida iniciada.")

if __name__ == "__main__":
    root = tk.Tk()
    joc = JocBatallaNaval(root)
    root.mainloop()
