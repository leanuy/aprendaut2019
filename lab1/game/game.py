### DEPENDENCIAS
### ------------------

import sys
import os

import utils.gui as gui 
from utils.const import GameMode, GameTokens, GameTokenMoves

from .board import Board
from .player import Player

### CLASE PRINCIPAL
### ------------------

class Game():

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self, mode, players):
        
        # Modo de juego
        # 1. Entrenamiento
        # 2. Juego
        self.mode = mode

        # Si modo es 1, representa al par de jugadores
        # Si modo es 2, representa al jugador oponente al humano
        self.players = players

        # Historial de tableros por turno
        self.boards = []

        # Opcion de impresión de tablero
        # 1. Hexagonal común
        # 2. Hexagonal con coordenadas
        # 3. Matriz con coordenadas
        self.boardPrint = 1

    # Simulación de un juego
    def play(self):

        if self.mode == GameMode.PLAYING:
            res = self.playUI()

        elif self.mode == GameMode.TRAINING:
            res = self.playTraining()

        return res


    def playUI(self):

        b = Board()
        player = self.players
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

            elif keyboard == 'PASS':
                # El turno pasa al otro jugador, que elige su jugada 
                ((fromX2, fromY2), (toX2, toY2)) = player.chooseMove(b)
                b.moveToken(GameTokens.PLAYER1, fromX2, fromY2, toX2, toY2)

                if b.checkWin(GameTokens.PLAYER1):
                    print("-> Has perdido la partida!")
                    input()
                    return
                    
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
                    elif res == GameTokenMoves.VALID_MOVE:

                        # Checkea si el jugador humano ganó luego de su jugada
                        if b.checkWin(GameTokens.PLAYER2):
                            return True
                        
                        # El turno pasa al otro jugador, que elige su jugada 
                        ((fromX2, fromY2), (toX2, toY2)) = player.chooseMove(b)
                        b.moveToken(GameTokens.PLAYER1, fromX2, fromY2, toX2, toY2)

                        # Checkea si el jugador automatico ganó luego de su jugada
                        if b.checkWin(GameTokens.PLAYER1):
                            return False

                        # Agrega el tablero al tablero de turnos
                        self.boards.append(b)

                except Exception as e:
                    print(e)
                    print("-> La entrada ingresada no sigue el formato adecuado. Intentelo de nuevo")
                    input()
                

    def playTraining(self):

        (player1, player2) = self.players
        b = Board()
        finished = False
        res = False

        while not finished:

            ((fromX2, fromY2), (toX2, toY2)) = player1.chooseMove(b)
            b.moveToken(GameTokens.PLAYER1, fromX2, fromY2, toX2, toY2)

            if b.checkWin(GameTokens.PLAYER1):
                finished = True
                res = True

            ((fromX2, fromY2), (toX2, toY2)) = player2.chooseMove(b)
            b.moveToken(GameTokens.PLAYER2, fromX2, fromY2, toX2, toY2)

            if b.checkWin(GameTokens.PLAYER2):
                finished = True
                res = False

        return res
                