# Para importar locales
import time
import copy
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Dependencias locales
import utils.gui as gui
from game.board import Board
from game.player import Player
from model.model_concept import ModelConcept
from game.game import Game
import processing.archiver as archiver
from utils.const import MenuOps, PlayerType, GameMode, GameTokens, GameResults, ModelTypes, PlayerType, ArchiveOps, CompareOps, GameTokenMoves

# Dependencias de IPython
from IPython.display import display, clear_output
from ipywidgets import Text, Label, Button, ToggleButtons, Box, Layout, HBox, VBox


# Cargar players
players = []
filesToLoad = ["jugador_lab1", "random_metrics_2_100_tanh_invscaling", "self_metrics_2_100_logistic_constant"]

for files in filesToLoad:
    p = archiver.loadPlayer(files, True)
    if p != None:
        players.append(p)

# Elegir oponente
playerIndex = gui.pickPlayer(players)
                
player = players[playerIndex-1]['player']

game_ended = False
b = Board()
opts = ['Hexagonal', 'Coordenadas', 'Matriz']

# Linea 1
buttonsText = Label(value='Representación del tablero:',
                    layout=Layout(margin='0px 16px 0px 0px'))
buttons = ToggleButtons(
    options=opts,
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''3
 
)
box0_layout = Layout(display='flex',
                    flex_flow='row',
                    margin='16px 0px 32px 0px',
                    width='100%')
box0 = Box(children=[buttonsText, buttons], layout=box0_layout)

# Linea 3
player2Text = Label(value='Movimiento de jugador 2:',
                    layout=Layout(margin='0px 16px 0px 0px'))
player2TextFrom = Text(
    placeholder='Desde (ej: -4,5)',
    disabled=False,
    layout=Layout(max_width='128px', margin='0px 16px 0px 0px')
)
player2TextTo = Text(
    placeholder='Hacia (ej: -3,4)',
    style={'description_width': 'initial'},
    disabled=False,
    layout=Layout(max_width='128px', margin='0px 16px 0px 0px')
)
player2Button = Button(
    description='Mover',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='80px', margin='0px 16px 0px 0px')
)
player2TextError = Label(value='')
box2_layout = Layout(display='flex',
                    flex_flow='row',
                    margin='8px 0px 8px 0px',
                    width='100%')
box2 = Box(children=[player2Text, player2TextFrom, player2TextTo, player2Button, player2TextError], layout=box2_layout)

# Todo
main_box_layout = Layout(display='flex',
                        flex_flow='column',
                        width='100%')
main_box = Box(children=[box2], layout=main_box_layout)

# Eventos
def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        clear_output()
        display(box0)
        if change['new'] == opts[0]:
            gui.printBoardHex(b.getMatrix(), False, b.fromVirtual)
        elif change['new'] == opts[1]:
            gui.printBoardHex(b.getMatrix(), True, b.fromVirtual)
        elif change['new'] == opts[2]:
           gui.printBoardMatrix(b.getMatrix(), b.getLength())
        display(main_box)
buttons.observe(on_change)

def on_move2(btn):
    if b.checkWin(GameTokens.PLAYER2):
        player2TextError.value = 'Felicidades, ganaste!'
    elif b.checkWin(GameTokens.PLAYER1):
        player2TextError.value = 'Perdiste, intentalo nuevamente!'
    else:
        fromSlot = player2TextFrom.value.split(',')
        toSlot =  player2TextTo.value.split(',')
        (fromX, fromY) = (int(fromSlot[0]), int(fromSlot[1]))
        (toX, toY) = (int(toSlot[0]), int(toSlot[1]))
        res = b.moveToken(GameTokens.PLAYER2, fromX, fromY, toX, toY)
        if res == GameTokenMoves.VALID_MOVE:
            if not b.checkWin(GameTokens.PLAYER2):
                move1()
            player2TextError.value = ""
            clear_output()
            display(box0)
            if buttons.value == opts[0]:
                gui.printBoardHex(b.getMatrix(), False, b.fromVirtual)
            elif buttons.value == opts[1]:
                gui.printBoardHex(b.getMatrix(), True, b.fromVirtual)
            elif buttons.value == opts[2]:
                gui.printBoardMatrix(b.getMatrix(), b.getLength())
            display(main_box)
        elif res == GameTokenMoves.INVALID_MOVE:
            player2TextError.value = "El movimiento es inválido"
        elif res == GameTokenMoves.TOKEN_FROM:
            player2TextError.value = "En la posición desde no hay un token del jugador 2"
        elif res == GameTokenMoves.TOKEN_TO:
            player2TextError.value = "En la posición hacia ya hay un token"
        elif res == GameTokenMoves.INVALID_COORDS:
            player2TextError.value = "Alguna de las coordenadas no existe en el tablero"
player2Button.on_click(on_move2)

def move1():
    ((fromX, fromY), (toX, toY)) = player.chooseMove(b)
    b.moveToken(GameTokens.PLAYER1, fromX, fromY, toX, toY)


# Muestra
display(box0)
gui.printBoardHex(b.getMatrix(), False, b.fromVirtual)
display(main_box)
