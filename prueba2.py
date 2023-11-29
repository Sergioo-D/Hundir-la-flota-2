from tkinter import *
from tkinter import font
import tkinter.messagebox
from functools import partial
import random
import time
import sys
import os

root = Tk()
root.wm_title("BATTLESHIPS")
root.configure(background='gray19')
font1 = font.Font(family='Helvetica', size=12, weight='bold')
font_big = font.Font(family='Helvetica', size=16, weight='bold')
font_normal = font.Font(family='Helvetica', size=10, weight='normal')

ships = {"Aircraft Carrier": 4, "Battleship": 3, "Submarine": 2, "Destroyer": 1}
AI = False


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def player_board():
    board = []
    t = []
    t += (10 + 2) * ['# ']
    board.append(t)  # Övre ram

    rad = ['# ']  # Vänster ram
    for r in range(0, 10):
        rad.append("~ ")
    rad.append('# ')  # Höger ram
    for k in range(0, 10):
        board.append(list(rad))

    board.append(t)  # Undre ram
    return board


def place_ship(ship, board):
    # w = 0  # Håller igång loopen
    while True:
        checkcoords = []
        x = random.randint(1, 10)  # Genererad x-koordinat
        y = random.randint(1, 10)  # Genererad y-koordinat
        o = random.randint(0, 1)  # Väljer placeringssätt
        if o == 0:
            ori = "v"  # Vertikalt
        else:
            ori = "h"  # Horisontellt
        if ori == "v" and y + ships[ship] > 10:
            pass
            # w = 0  # Säkerställer att båten kan placeras inom spelplanen
        elif ori == "h" and x + ships[ship] > 10:
            pass
            # w = 0
        else:
            if ori == "v":
                for i in range(-1, (ships[ship] + 1)):
                    for j in range(-1, 2):
                        checkcoords.append(board[y + i][x + j])
                if ': ' not in checkcoords:
                    for i in range(ships[ship]):
                        board[y + i][x] = ': '
                    break
            #                else:
            #                    w = 0
            elif ori == "h":
                for i in range(-1, (ships[ship] + 1)):
                    for j in range(-1, 2):
                        checkcoords.append(board[y + j][x + i])
                if ': ' not in checkcoords:
                    for i in range(ships[ship]):
                        board[y][x + i] = ': '
                    break


#                else:
#                    w = 0


def place_all_ships(board):
    for ship in ships:
        for antal in range(0, (5 - ships[ship])):
            place_ship(ship, board)


def popupwindow(msg):
    answer = tkinter.messagebox.askquestion("Game Over", msg + " Would you like to play again?")
    if answer == "yes":
        restart_program()
    elif answer == "no":
        quit()


def nr_players(number):
    global AI
    if number == 1:
        player2_or_AI.set("AI")
        AI = True
    else:
        player2_or_AI.set("Player 2")


info = StringVar()
player2_or_AI = StringVar()


def side_labels():
    # info = StringVar()
    Label(root, text="BATTLESHIPS", fg="white", bg="gray19", font=font_big).grid(row=0, column=10, columnspan=9)
    Label(root, textvariable=info, fg="white", bg="gray19", font=font1).grid(row=12, column=6, columnspan=18)

    for _ in range(10):
        Label(root, text="   ", bg="gray19").grid(row=_, column=0)
    Button(root, width=7, height=1, text="1 Player", font=font1, fg="white", activebackground="gray19",
           bg="gray19", command=lambda: nr_players(1)).grid(row=2, column=1)
    Button(root, width=7, height=1, text="2 Players", font=font1, fg="white", activebackground="gray19",
           bg="gray19", command=lambda: nr_players(2)).grid(row=3, column=1)
    Label(root, text="Get 20 hits to win", font=font_normal, fg="white", bg="gray19").grid(row=5, column=1)
    Label(root, text="1 Battleship 4 units", font=font_normal, fg="white", bg="gray19").grid(row=6, column=1)
    Label(root, text="2 Battleships 3 units", font=font_normal, fg="white", bg="gray19").grid(row=7, column=1)
    Label(root, text="3 Battleships 2 units", font=font_normal, fg="white", bg="gray19").grid(row=8, column=1)
    Label(root, text="4 Battleships 1 unit  ", font=font_normal, fg="white", bg="gray19").grid(row=9, column=1)

    for _ in range(10):
        Label(root, text="   ", bg="gray19").grid(row=_, column=2)

    for _ in range(10):
        Label(root, width=20, text="   ", bg="gray19").grid(row=_, column=25)


def ai_shoots(y_coord, x_coord, all_buttons, player_1_board, ai_score):
    # print("yes")
    if ai_score == 20:
        popupwindow("The computer has won.")
    if player_1_board[y_coord][x_coord] == ': ':
        ai_score += 1
        player_1_board[y_coord][x_coord] = 'X '
        all_buttons[y_coord - 1][x_coord - 1].configure(text="X", fg="black", bg="red3")
        if player_1_board[y_coord - 1][x_coord] == ': ':
            ai_shoots(y_coord - 1, x_coord, all_buttons, player_1_board, ai_score)
        elif player_1_board[y_coord + 1][x_coord] == ': ':
            ai_shoots(y_coord + 1, x_coord, all_buttons, player_1_board, ai_score)
        elif player_1_board[y_coord][x_coord - 1] == ': ':
            ai_shoots(y_coord, x_coord - 1, all_buttons, player_1_board, ai_score)
        elif player_1_board[y_coord][x_coord + 1] == ': ':
            ai_shoots(y_coord, x_coord + 1, all_buttons, player_1_board, ai_score)
        else:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            ai_shoots(y, x, all_buttons, player_1_board, ai_score)
    elif player_1_board[y_coord][x_coord] == 'X ' or player_1_board[y_coord][x_coord] == 'O ':
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        ai_shoots(y, x, all_buttons, player_1_board, ai_score)
    else:
        player_1_board[y_coord][x_coord] = 'O '
        all_buttons[y_coord - 1][x_coord - 1].configure(text="O", fg="white")


def hit_or_miss(a, b, board, all_buttons, info, player, player_1_hits, player_2_hits, ai_score):
    global AI
    # print(player)
    if board[a + 1][b + 1] == 'O ' or board[a + 1][b + 1] == 'X ':  # Redan skjutit
        info.set("You have already fired there, " + player + "!")

    elif board[a + 1][b + 1] == ': ':  # Träff
        info.set("A hit, nice shot " + player + "!")
        board[a + 1][b + 1] = 'X '
        all_buttons[a][b].configure(text="X", fg="black", bg="red3", activebackground="red3")
        if player == "player 1":
            player_1_hits += 1
        else:
            player_2_hits += 1

    else:  # Miss
        info.set("Seems like you missed that one, " + player + "!")
        board[a + 1][b + 1] = 'O '
        all_buttons[a][b].configure(text="O", fg="White", activeforeground="white")
        # print(AI)
        if AI:
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            ai_shoots(y, x, all_buttons, board, ai_score)
    if player_1_hits == 20 or player_2_hits == 20:
        popupwindow(player + " has won!")


def side(player, allbuttons):
    print(player)
    if player == "player 1":
        for row in range(10):
            for column in range(10):
                allbuttons[row][column].grid(row=1 + row, column=4 + column)

        label2 = Label(root, text="Player 1", font=font1, fg="white", bg="gray19")
        label2.grid(row=11, column=4, columnspan=10)
    else:
        for row in range(10):
            for column in range(10):
                allbuttons[row][column].grid(row=1 + row, column=15 + column)

        label3 = Label(root, textvariable=player2_or_AI, font=font1, fg="white", bg="gray19")
        label3.grid(row=11, column=15, columnspan=10)


def board_buttons(board, info, player, player_1_hits, player_2_hits, ai_score):
    allbuttons = []
    a = 0
    print(AI)
    for i in range(10):
        b = 0
        buttons = []
        for j in range(10):
            button = Button(root, width=2, height=1, font=font1, bg="sky blue", activebackground="sky blue",
                            command=partial(hit_or_miss, a, b, board, allbuttons,
                                            info, player, player_1_hits, player_2_hits, ai_score))
            buttons.append(button)
            b += 1
        allbuttons.append(list(buttons))
        a += 1

    side(player, allbuttons)


def middle_board_space():
    for _ in range(10):
        Label(root, text="   ", bg="gray19").grid(row=1 + _, column=14)


def main():
    player_1_hits = 0
    player_2_hits = 0
    ai_hits = 0

    player_1_board = player_board()
    player_2_board = player_board()

    place_all_ships(player_1_board)  # Sätter ut alla skeppen
    place_all_ships(player_2_board)

    info = StringVar()
    side_labels()

    board_buttons(player_1_board, info, "player 1", player_1_hits, player_2_hits, ai_hits)
    middle_board_space()
    board_buttons(player_2_board, info, "player 2", player_1_hits, player_2_hits, ai_hits)


main()
root.mainloop()
############################################