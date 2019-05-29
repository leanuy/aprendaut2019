# Para importar locales
import copy
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Dependencias locales
import evaluation.evaluator as evaluator
import processing.plotter as plotter
import processing.archiver as archiver
import utils.gui as gui
from utils.const import MenuOps, PlayerType, GameMode, GameTokens, GameResults, ModelTypes, PlayerType, ArchiveOps, CompareOps, GameTokenMoves

def plot(compare_op):
    if compare_op == CompareOps.WIN_RATE or compare_op == CompareOps.VICTORY_RATE:

        playerType = PlayerType.TRAINED_SELF

        player_metrics = archiver.loadMassive(f'{playerType.value}_metrics', True)
        players_board = archiver.loadMassive(f'{playerType.value}_board', True)

        player_metrics = evaluator.getRateFromPlayers(player_metrics, compare_op)
        players_board = evaluator.getRateFromPlayers(players_board, compare_op)

        plotter.plotWinRate(compare_op, playerType, player_metrics, players_board)

        playerType = PlayerType.TRAINED_RANDOM

        player_metrics = archiver.loadMassive(f'{playerType.value}_metrics', True)
        players_board = archiver.loadMassive(f'{playerType.value}_board', True)

        player_metrics = evaluator.getRateFromPlayers(player_metrics, compare_op)
        players_board = evaluator.getRateFromPlayers(players_board, compare_op)

        plotter.plotWinRate(compare_op, playerType, player_metrics, players_board)

    else:

        players_random_metrics = archiver.loadMassive(f'random_metrics', True)
        players_random_board = archiver.loadMassive(f'random_board', True)
        players_self_metrics = archiver.loadMassive(f'self_metrics', True)
        players_self_board = archiver.loadMassive(f'self_board', True)

        if compare_op == CompareOps.HIDDEN_LAYERS:

            hiddenLayersData = []
            hiddenLayersData.append(evaluator.getHiddenLayersRateFromPlayers(players_random_metrics))
            hiddenLayersData.append(evaluator.getHiddenLayersRateFromPlayers(players_random_board))
            hiddenLayersData.append(evaluator.getHiddenLayersRateFromPlayers(players_self_metrics))
            hiddenLayersData.append(evaluator.getHiddenLayersRateFromPlayers(players_self_board))

            hiddenNeuronsData = []
            hiddenNeuronsData.append(evaluator.getHiddenNeuronsRateFromPlayers(players_random_metrics))
            hiddenNeuronsData.append(evaluator.getHiddenNeuronsRateFromPlayers(players_random_board))
            hiddenNeuronsData.append(evaluator.getHiddenNeuronsRateFromPlayers(players_self_metrics))
            hiddenNeuronsData.append(evaluator.getHiddenNeuronsRateFromPlayers(players_self_board))

            plotter.plotHiddenLayersWinRate(hiddenLayersData, hiddenNeuronsData)

        elif compare_op == CompareOps.ACTIVATION:

            activationData = []
            activationData.append(evaluator.getActivationRateFromPlayers(players_random_metrics))
            activationData.append(evaluator.getActivationRateFromPlayers(players_random_board))
            activationData.append(evaluator.getActivationRateFromPlayers(players_self_metrics))
            activationData.append(evaluator.getActivationRateFromPlayers(players_self_board))

            plotter.plotActivationWinRate(activationData)

        elif compare_op == CompareOps.LEARNING_RATE:

            learningRateData = []
            learningRateData.append(evaluator.getLearningRatesRateFromPlayers(players_random_metrics))
            learningRateData.append(evaluator.getLearningRatesRateFromPlayers(players_random_board))
            learningRateData.append(evaluator.getLearningRatesRateFromPlayers(players_self_metrics))
            learningRateData.append(evaluator.getLearningRatesRateFromPlayers(players_self_board))

            plotter.plotLearningRateWinRate(learningRateData)
