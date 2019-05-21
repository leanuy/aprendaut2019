# Para importar locales
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Dependencias locales
import utils.gui as gui
from utils.const import GameTokens, GameTokenMoves
from game.board import Board

# Dependencias de IPython
from IPython.display import display, clear_output
from ipywidgets import Text, Label, Button, ToggleButtons, Box, Layout, HBox, VBox

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

# Linea 2
player1Text = Label(value='Movimiento de jugador 1:',
                    layout=Layout(margin='0px 16px 0px 0px'))
player1TextFrom = Text(
    placeholder='Desde (ej: 4,-5)',
    disabled=False,
    layout=Layout(max_width='128px', margin='0px 16px 0px 0px')
)
player1TextTo = Text(
    placeholder='Hacia (ej: 3,-4)',
    style={'description_width': 'initial'},
    disabled=False,
    layout=Layout(max_width='128px', margin='0px 16px 0px 0px')
)
player1Button = Button(
    description='Mover',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='80px', margin='0px 16px 0px 0px')
)
player1TextError = Label(value='')
box1_layout = Layout(display='flex',
                    flex_flow='row',
                    margin='16px 0px 8px 0px',
                    width='100%')
box1 = Box(children=[player1Text, player1TextFrom, player1TextTo, player1Button, player1TextError], layout=box1_layout)

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
main_box = Box(children=[box1, box2], layout=main_box_layout)

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

def on_move1(btn):
    fromSlot = player1TextFrom.value.split(',')
    toSlot =  player1TextTo.value.split(',')
    (fromX, fromY) = (int(fromSlot[0]), int(fromSlot[1]))
    (toX, toY) = (int(toSlot[0]), int(toSlot[1]))
    res = b.moveToken(GameTokens.PLAYER1, fromX, fromY, toX, toY)
    if res == GameTokenMoves.VALID_MOVE:
        player1TextError.value = ""
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
        player1TextError.value = "El movimiento es inválido"
    elif res == GameTokenMoves.TOKEN_FROM:
        player1TextError.value = "En la posición desde no hay un token del jugador 1"
    elif res == GameTokenMoves.TOKEN_TO:
        player1TextError.value = "En la posición hacia ya hay un token"
    elif res == GameTokenMoves.INVALID_COORDS:
        player1TextError.value = "Alguna de las coordenadas no existe en el tablero"
player1Button.on_click(on_move1)

def on_move2(btn):
    fromSlot = player2TextFrom.value.split(',')
    toSlot =  player2TextTo.value.split(',')
    (fromX, fromY) = (int(fromSlot[0]), int(fromSlot[1]))
    (toX, toY) = (int(toSlot[0]), int(toSlot[1]))
    res = b.moveToken(GameTokens.PLAYER2, fromX, fromY, toX, toY)
    if res == GameTokenMoves.VALID_MOVE:
        player1TextError.value = ""
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
        player2TextError.value = "En la posición desde no hay un token del jugador 1"
    elif res == GameTokenMoves.TOKEN_TO:
        player2TextError.value = "En la posición hacia ya hay un token"
    elif res == GameTokenMoves.INVALID_COORDS:
        player2TextError.value = "Alguna de las coordenadas no existe en el tablero"
player2Button.on_click(on_move2)

# Muestra
display(box0)
gui.printBoardHex(b.getMatrix(), False, b.fromVirtual)
display(main_box)
