### DEPENDENCIAS
### ------------------

import sys
import os

import utils.gui as gui 
from utils.const import GameMode

from .board import Board

### CLASE PRINCIPAL
### ------------------

class Game():

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self):
        # Historial de tableros por turno
        self.boards = []
        self.boardPrint = 1

    # Simulación de un juego
    def play(self, mode, players):

        if mode == GameMode.PLAYING:
            self.playUI(players)

        elif mode == GameMode.TRAINING:
            self.playTraining(players)


    def playUI(self, player):

        keyboard = ''
        while keyboard != '0':

            gui.printClear()

            b = Board()

            if self.boardPrint == 1:
                gui.printBoardHex(b.getMatrix(), False, b.inverse1, b.inverse2)
            elif self.boardPrint == 2:
                gui.printBoardHex(b.getMatrix(), True, b.inverse1, b.inverse2)
            elif self.boardPrint == 3:
                gui.printBoardMatrix(b.getMatrix(), b.getLength())

            print("-> Ingrese su jugada o el numero de la opción deseada: ")
            print("---> Para mover la ficha (x,y) a la posicion (w,z) ingrese x,y w,z")
            print("---> 1 - Ver tablero normal")
            print("---> 2 - Ver tablero grilla")
            print("---> 3 - Ver tablero matriz")
            print("---> 0 - Abandonar")
            keyboard = input()

            if keyboard == '1':
                self.boardPrint = 1

            elif keyboard == '2':
                self.boardPrint = 2

            elif keyboard == '3':
                self.boardPrint = 3

    def playTraining(self, players):

        (player1, player2) = players
        