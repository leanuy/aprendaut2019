### DEPENDENCIAS
### ------------------

import time
import operator

from game.game import Game
from utils.const import ModelTypes, InputLayerTypes, HiddenLayersOps, ActivationFunctions, LearningRateOps, GameMode, GameResults
from utils.gui import printTrainedPlayer

### METODOS PRINCIPALES
### -------------------

def simulateTourney(players):

    # Variables globales
    table = {}

    # Inicialización de tabla de resultados
    for p in players:
        
        gameResults = {}
        otherPlayers = players.copy()
        otherPlayers.remove(p)
        
        for op in otherPlayers:
            gameResults[op['playerID']] = 0

        table[p['playerID']] = (0, gameResults)

    # Se juegan los partidos de cada jugador
    for p in players:

        playerID = p['playerID']
        print(f"-> Jugando ronda del jugador {playerID}")
        print()

        otherPlayers = players.copy()
        otherPlayers.remove(p)

        # Se juega contra todos los otros jugadores, incluso si ya se jugo
        for op in otherPlayers:

            opponentID = op['playerID']
            print(f"--> Partido: {playerID} VS {opponentID}")
            
            # Se genera la partida y se juega
            g = Game(GameMode.TOURNEY, (p['player'], op['player']))
            res = g.play(True)

            print(f"--> Resultado: {playerID} {res}")
            print()

            # Se actualiza la tabla según el resultado
            if res == GameResults.WIN:
                score, results = table[p['playerID']]
                score += 3
                results[op['playerID']] += 1
                table[p['playerID']] = (score, results)

            elif res == GameResults.LOSE:
                score, results = table[op['playerID']]
                score += 3
                results[p['playerID']] = 1
                table[op['playerID']] = (score, results)

            else:
                score, results = table[p['playerID']]
                score += 1
                table[p['playerID']] = (score, results)

                score, results = table[op['playerID']]
                score += 1
                table[op['playerID']] = (score, results)

        print()
        print('---------------------------------------------------------------')

    # Ordenar tabla según puntaje
    table = sorted(table.items(), key=lambda x: x[1][0], reverse=True)
    print(table)
    return table