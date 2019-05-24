### DEPENDENCIAS
### ------------------

import sys
import os
import re
import copy
import time

import utils.gui as gui 
from utils.const import GameMode, GameTokens, GameTokenMoves, GameResults, ModelTypes

from .board import Board
from .player import Player

### CLASE PRINCIPAL
### ------------------

class Game():

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self, mode, players, maxRounds = 300):
        
        # Modo de juego
        # 1. Entrenamiento
        # 2. Juego
        # 3. Espectar
        self.mode = mode

        # Si modo es 1 o 3, representa al par de jugadores
        # Si modo es 2, representa al jugador oponente al humano
        self.players = players

        # Historial de tableros por turno
        self.boards = []

        # Cantidad de turnos antes de declarar empate
        self.maxRounds = maxRounds

        # Opcion de impresión de tablero
        # 1. Hexagonal común
        # 2. Hexagonal con coordenadas
        # 3. Matriz con coordenadas
        self.boardPrint = 1

    ### GETTERS y SETTERS
    ### -------------------

    def getBoards(self):
        return self.boards

    # Simulación de un juego
    def play(self, spectate = False):
        if self.mode == GameMode.PLAYING:
            res = self.playUI()
        else:
            res = self.playTraining(spectate)

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

            (keyboard, keyboardToken) = gui.printGameMenuOption()

            if keyboard == '1':
                self.boardPrint = 1

            elif keyboard == '2':
                self.boardPrint = 2

            elif keyboard == '3':
                self.boardPrint = 3

            elif keyboard == '4':
                gui.printFeatures(b.getFeatures(GameTokens.PLAYER2))
                input()

            elif keyboard == '5':
                gui.printFeatures(b.getPlayerFeatures(GameTokens.PLAYER2))
                input()

            elif keyboard == 'PASS':
                ((fromX2, fromY2), (toX2, toY2)) = player.chooseMove(b)
                b.moveToken(GameTokens.PLAYER1, fromX2, fromY2, toX2, toY2)

                if b.checkWin(GameTokens.PLAYER1):
                    print("-> Has perdido la partida!")
                    input()
                    return

            elif keyboardToken is not None:
                coords = keyboard.split(',')
                token = (int(coords[0]), int(coords[1]))
                if token in b.getPlayerSlots(GameTokens.PLAYER2):
                    goal = (b.getRadius(), -(b.getLength()-1))
                    print("Suma cuadrada de distancia al extremo: " + str(b.hexDistance(token, goal)))
                    print("Suma cuadrada de distancia al centro: " + str(b.verticalCenterDistance(token)))
                    print("Suma de maxima cantidad de saltos: " + str(b.maxHopsToGoal(token, GameTokens.PLAYER2, goal)))
                    print()
                    input()

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
                            self.boards.append(copy.deepcopy(b))
                            return GameResults.WIN
                        
                        # El turno pasa al otro jugador, que elige su jugada 
                        ((fromX2, fromY2), (toX2, toY2)) = player.chooseMove(b)
                        b.moveToken(GameTokens.PLAYER1, fromX2, fromY2, toX2, toY2)

                        # Agrega el tablero al tablero de turnos
                        self.boards.append(copy.deepcopy(b))

                        # Checkea si el jugador automatico ganó luego de su jugada
                        if b.checkWin(GameTokens.PLAYER1):
                            return GameResults.LOSE

                except Exception as e:
                    print(e)
                    print("-> La entrada ingresada no sigue el formato adecuado. Intentelo de nuevo")
                    input()
                

    def playTraining(self, spectate = False):

        (player1, player2) = self.players
        b = Board()
        finished = False
        res = False

        while not finished:
            if spectate:
                gui.printClear()
                gui.printBoardHex(b.getMatrix(), False, b.fromVirtual)

            # Jugador 1 elige su movimiento y juega
            ((fromX2, fromY2), (toX2, toY2)) = player1.chooseMove(b)
            b.moveToken(player1.playerNumber, fromX2, fromY2, toX2, toY2)

            # Se checkea si el jugador 1 ganó
            if b.checkWin(player1.playerNumber):
                finished = True
                res = GameResults.WIN
            
            # Si el jugador 1 no ganó, el jugador 2 elige su movimiento y juega
            if not finished:
                # time.sleep(0.5)
                ((fromX2, fromY2), (toX2, toY2)) = player2.chooseMove(b)
                b.moveToken(player2.playerNumber, fromX2, fromY2, toX2, toY2)

                if b.checkWin(player2.playerNumber):
                    finished = True
                    res = GameResults.LOSE

            # Agrega el tablero al tablero de turnos
            self.boards.append(copy.deepcopy(b))

            if len(self.boards) >= self.maxRounds:
                finished = True
                res = GameResults.DRAW
            # time.sleep(0.5)

        print("Partida finalizada con resultado " + str(res))
        return res