### DEPENDENCIAS
### ------------------

import sys
import os

import utils.gui as gui 
from utils.const import GameMode, GameTokens, GameTokenMoves

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

        b = Board()
        keyboard = ''

        while keyboard != '0':

            gui.printClear()    

            if self.boardPrint == 1:
                gui.printBoardHex(b.getMatrix(), False, b.fromVirtual)
            elif self.boardPrint == 2:
                gui.printBoardHex(b.getMatrix(), True, b.fromVirtual)
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

            elif keyboard != '0':
                try:
                    coords = keyboard.split()
                
                    fromSlot = coords[0].split(',')
                    toSlot = coords[1].split(',')

                    (fromX, fromY) = (int(fromSlot[0]), int(fromSlot[1]))
                    (toX, toY) = (int(toSlot[0]), int(toSlot[1]))

                    res = b.moveToken(GameTokens.PLAYER2, fromX, fromY, toX, toY)
                    if res == GameTokenMoves.INVALID_MOVE:
                        print("-> La ficha en " + str((fromX, fromY)) + " no puede llegar a " + str((toX, toY)) + ". Intentelo de nuevo")
                        input()
                    elif res == GameTokenMoves.TOKEN_FROM:
                        print("-> No hay una ficha suya en " + str((fromX, fromY)) + ". Intentelo de nuevo")
                        input()
                    elif res == GameTokenMoves.TOKEN_TO:
                        print("-> Ya hay una ficha en " + str((toX, toY)) + ". Intentelo de nuevo")
                        input()
                    elif res == GameTokenMoves.INVALID_COORDS:
                        print("-> No existe en el tablero la posición " + str((fromX, fromY)) + " o la posición " + str((toX, toY)) + ". Intentelo de nuevo")
                        input()

                except:
                  print("-> La entrada ingresada no sigue el formato adecuado. Intentelo de nuevo")
                  input()
                

    def playTraining(self, players):

        (player1, player2) = players
        