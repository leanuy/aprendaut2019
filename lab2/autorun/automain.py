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
from utils.const import MenuOps, ModelOps, ContinuousOps, EvaluationOps, MeasureOps, IRIS_DATASET, COVERTYPE_DATASET

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':
    
    try:
        if len(sys.argv) != 6:
            raise Exception('Cantidad de argumentos insuficiente')
        datasetFile = COVERTYPE_DATASET if int(sys.argv[1]) == 2 else IRIS_DATASET
        datasetOut = 'Covertype' if int(sys.argv[1]) == 2 else 'Iris'
        datasetFile = '../' + datasetFile
        (modelType, modelName) = (ModelOps.DECISION_FOREST, 'Bosque') if int(sys.argv[2]) == 2 else (ModelOps.DECISION_TREE, 'Árbol')
        
        if int(sys.argv[3]) == 2:
            continuous = ContinuousOps.VARIABLE
            continuousOut = 'Variable'
        
        elif int(sys.argv[3]) == 3:
            continuous = ContinuousOps.C45
            continuousOut = 'C45'
        else:
            continuous = ContinuousOps.FIXED
            continuousOut = 'Fixed'
        
        if int(sys.argv[4]) == 2:
            measureType = MeasureOps.GAINRATIO
            measureTypeOut = 'GainRatio'
        elif int(sys.argv[4]) == 3:
            measureType = MeasureOps.IMPURITYREDUCTION
            measureTypeOut = 'ImpurityReduction'
        else:
            measureType = MeasureOps.GAIN
            measureTypeOut = 'Gain'
        
        evalMode = EvaluationOps.CROSS if int(sys.argv[5]) == 2 else EvaluationOps.NORMAL
        evalModeOut = 'Cross' if int(sys.argv[5]) == 2 else 'Normal'

    except Exception as error:
        print('Caught this error: ' + repr(error))
        sys.exit(1)

    print()
    print("-> COMIENZO DE LA LECTURA")

    options = {
    'continuous': continuous,
    'measure': measureType
    }

    (dataset, attributes, results) = reader.readDataset(datasetFile, datasetFile == '../' + COVERTYPE_DATASET)
    model = Model(modelType)

    classifier = {
        'model': model,
        'attributes': attributes,
        'results': results,
        'type': modelType,
        'name': modelName,
        'options': options,
    }
    
    print()
    print("-> FIN DE LA LECTURA")

    resultFileName = "results/" + datasetOut + ", " + modelName + ", " + str(continuousOut) + ", " + str(measureTypeOut) + ", " + str(evalModeOut) + ".dat"
    if evalMode == EvaluationOps.NORMAL:
        (trainingTime, accuracy, means, weightedMeans, eval, confusionMatrix) = normalValidation(dataset, classifier)
        sys.stdout = open(resultFileName, 'w')
        gui.printNormalEvaluation(classifier, trainingTime, accuracy, means, weightedMeans, eval, confusionMatrix, len(dataset))

    elif evalMode == EvaluationOps.CROSS:
        evalK = 10 # Cambiar si se desean menos
        (eval, evalMean) = crossValidation(dataset, classifier, evalK)
        sys.stdout = open(resultFileName, 'w')
        gui.printCrossEvaluation(classifier, eval, evalMean, len(dataset))

    sys.stdout.close()