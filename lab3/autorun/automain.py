### README
### ------------------

# Llamar con:
# python automain.py DATASET MODEL EVALUATION ... (Los parámetros subsiguientes dependen del modelo)
# DATASET = { 1: Iris, 2: Covertype }
# MODEL = { 1: Arbol, 2: Bosque, 3: Naive Bayes, 4: KNN }
# EVALUATION = { 1: Normal, 2: Cross }

# Arboles o Bosques:
# python automain.py DATASET MODEL EVALUATION CONTINUOUS MEASURE
# CONTINUOUS = { 1: Fixed, 2: Variable, 3: C4.5 }
# MEASURE = { 1: Gain, 2: Gain Ratio, 3: Impurity Reduction }
#
# python automain.py (1|2) (1|2) (1|2) (1|2|3) (1|2|3)
# EJ: automain.py 2 2 1 2 3

# Bayes:
# python automain.py DATASET MODEL EVALUATION ONEHOT CONTINUOUS mEST
# ONEHOT = { 1: Deshacer Onehot Encoding, 2: Conservar Onehot Encoding }
# CONTINUOUS = { 1: Standarization, 2: Variable }
# mEST = 0..n
#
# python automain.py (1|2) 3 (1|2) (1|2) (1|2) (0..n)
# EJ: automain.py 2 3 1 1 1

# KNN:
# python automain.py DATASET MODEL EVALUATION ONEHOT K MEASURE NORM
# ONEHOT = { 1: Deshacer Onehot Encoding, 2: Conservar Onehot Encoding }
# K = 1..n (Se prefieren impares)
# MEASURE = { 1: Distancia 'Manhattan', 2: Distancia Euclídea, 3: Distancia de Chebychev, 4: Distancia de Mahalanobis }
# NORM = { 1: Norma Euclídea, 2: Norma Min-Max, 3: Norma Z-Score, 4: Ninguna Norma }
#
# python automain.py (1|2) 4 (1|2) (1|2) (1..n) (1|2|3|4) (1|2|3|4)
# EJ: automain.py 2 4 1 3 2 1

### DEPENDENCIAS
### ------------------

import sys
import os
import time

sys.path.append('..')

from model.model import Model
import processing.reader as reader
import processing.parser as parser
from evaluation.evaluate import normalValidation, crossValidation
import utils.gui as gui
from utils.const import MenuOps, ModelOps, ContinuousOps, EvaluationOps, MeasureOps, DistanceOps, NormOps, IRIS_DATASET, COVERTYPE_DATASET

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    ### OPCIONES
    
    # General
    datasetFiles = { 1: (IRIS_DATASET, 'Iris'), 2: (COVERTYPE_DATASET, 'Covertype') }
    models = { 1: (ModelOps.DECISION_TREE, 'Arbol'), 2: (ModelOps.DECISION_FOREST, 'Bosque'), 3: (ModelOps.NAIVE_BAYES, "Bayes"), 4: (ModelOps.KNN, "KNN") }
    evaluationModes = { 1: (EvaluationOps.NORMAL, 'Normal'), 2: (EvaluationOps.CROSS, 'Cross') }

    # Arboles y Bosques
    continuousStrategiesTrees = { 1: (ContinuousOps.FIXED, 'Fixed'), 2: (ContinuousOps.VARIABLE, 'Variable'), 3: (ContinuousOps.C45, 'C45') }
    measureTypesTrees = { 1: (MeasureOps.GAIN, 'Gain'), 2: (MeasureOps.GAINRATIO, 'GainRatio'), 3: (MeasureOps.IMPURITYREDUCTION, 'ImpurityReduction') }

    # Bayes y KNN
    onehotStrategies = { 1: (True, 'No Onehot'), 2: (False, 'Onehot') }

    # Bayes
    continuousStrategiesBayes = { 1: (ContinuousOps.STANDARDIZATION, 'Standarization'), 2: (ContinuousOps.VARIABLE, 'Variable') }

    # KNN
    measureTypesKNN = { 1: (DistanceOps.MANHATTAN, "Distancia 'Manhattan'"), 2: (DistanceOps.EUCLIDEAN, 'Distancia Euclídea'), 3: (DistanceOps.CHEBYCHEV, 'Distancia de Chebychev'), 4: (DistanceOps.MAHALANOBIS, 'Distancia de Mahalanobis') }
    normStrategies = { 1: (NormOps.EUCLIDEAN, 'Norma Euclídea'), 2: (NormOps.MIN_MAX, 'Norma Min-Max'), 3: (NormOps.Z_SCORE, 'Norma Z-Score'), 4: (NormOps.NONE, 'Ninguna Norma') }

    try:
        ### LECTURA DE ENTRADA
        if int(sys.argv[2]) == 1 or int(sys.argv[2]) == 2: # Arbol o Bosque
            lengthOfParams = 6
        elif int(sys.argv[2]) == 3: # Bayes
            lengthOfParams = 7
        elif int(sys.argv[2]) == 4: # KNN
            lengthOfParams = 8
        else:
            raise Exception('Modelo desconocido')

        if len(sys.argv) != lengthOfParams:
            raise Exception('Cantidad de argumentos insuficiente')
        
        # General:
        (datasetFile, datasetOut) = datasetFiles[int(sys.argv[1])]
        datasetFile = '../' + datasetFile
        (modelType, modelName) = models[int(sys.argv[2])]
        (evalMode, evalModeOut) = evaluationModes[int(sys.argv[3])]

        # Arboles y Bosques:
        if modelType == ModelOps.DECISION_TREE or modelType == ModelOps.DECISION_FOREST:
            (continuous, continuousOut) = continuousStrategiesTrees[int(sys.argv[4])]
            (measureType, measureTypeOut) = measureTypesTrees[int(sys.argv[5])]

            # Nombres de archivos
            resultFileName = "results/data/" + datasetOut + ", " + modelName + ", " + str(continuousOut) + ", " + str(measureTypeOut) + ", " + str(evalModeOut) + ".dat"
            resultCSVName = "results/csv/" + datasetOut + ", " + modelName + ", " + str(continuousOut) + ", " + str(measureTypeOut) + ", " + str(evalModeOut) + ".csv"
        else:
            # Bayes y KNN:
            (revertOnehot, onehotOut) = onehotStrategies[int(sys.argv[4])]
        
        # Bayes:
        if modelType == ModelOps.NAIVE_BAYES:
            (continuous, continuousOut) = continuousStrategiesBayes[int(sys.argv[5])]
            mEst = abs(float(sys.argv[6]))

            # Nombres de archivos
            resultFileName = "results/data/" + datasetOut + ", " + modelName + ", " + str(onehotOut) + ", " + str(continuousOut) + ", mEst - " + str(mEst) + ", " + str(evalModeOut) + ".dat"
            resultCSVName = "results/csv/" + datasetOut + ", " + modelName + ", " + str(onehotOut) + ", " + str(continuousOut) + ", mEst - " + str(mEst) + ", " + str(evalModeOut) + ".csv"
            
        if modelType == ModelOps.KNN:
            k = abs(int(sys.argv[5]))
            (measureType, measureTypeOut) = measureTypesKNN[int(sys.argv[6])]
            (norm, normOut) = normStrategies[int(sys.argv[7])]

            # Nombres de archivos
            resultFileName = "results/data/" + datasetOut + ", " + modelName + ", " + str(onehotOut) + ", k - " + str(k) + ", " + str(measureTypeOut) + ', ' + normOut + ", " + str(evalModeOut) + ".dat"
            resultCSVName = "results/csv/" + datasetOut + ", " + modelName + ", " + str(onehotOut) + ", k - " + str(k) + ", " + str(measureTypeOut) + ', ' + normOut + ", " + str(evalModeOut) + ".csv"
        
        print(resultCSVName)

        # Valores por defecto:
        continuous = continuous if 'continuous' in vars() else ContinuousOps.FIXED
        measureType = measureType if 'measureType' in vars() else MeasureOps.GAIN
        revertOnehot = revertOnehot if 'revertOnehot' in vars() else True
        mEst = mEst if 'mEst' in vars() else 1
        k = k if 'k' in vars() else 3
        norm = norm if 'norm' in vars() else NormOps.EUCLIDEAN

    except Exception as error:
        print('Caught this error: ' + repr(error))
        sys.exit(1)

    ### LECTURA
    (dataset, attributes, results) = reader.readDataset(datasetFile, (datasetFile == '../' + COVERTYPE_DATASET), revertOnehot)

    ### CONFIGURACIÓN
    model = Model(modelType)
    options = {
        'k': k,
        'continuous': continuous,
        'measure': measureType,
        'norm': norm,
        'revertOnehot': revertOnehot,
        'mEst': mEst,
        'structure': True,
    }

    classifier = {
        'model': model,
        'attributes': attributes,
        'results': results,
        'type': modelType,
        'name': modelName,
        'options': options,
    }

    ### ENTRENAMIENTO

    if evalMode == EvaluationOps.NORMAL:
        (trainingTime, accuracy, means, weightedMeans, eval, confusionMatrix) = normalValidation(dataset, classifier)
        parser.getEvaluationCSV(resultCSVName, accuracy, means, weightedMeans, eval, confusionMatrix)
        sys.stdout = open(resultFileName, 'w')
        gui.printNormalEvaluation(classifier, trainingTime, accuracy, means, weightedMeans, eval, confusionMatrix, len(dataset))

    elif evalMode == EvaluationOps.CROSS:
        evalK = 10 # Cambiar si se desean menos
        (eval, evalMean) = crossValidation(dataset, classifier, evalK)
        (accuracy, means, weightedMeans, evals) = evalMean
        parser.getEvaluationCSV(resultCSVName, accuracy, means, weightedMeans, evals)
        sys.stdout = open(resultFileName, 'w')
        gui.printCrossEvaluation(classifier, eval, evalMean, len(dataset))

    sys.stdout.close()