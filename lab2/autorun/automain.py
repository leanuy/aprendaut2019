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
from utils.const import MenuOps, ModelOps, ContinuousOps, EvaluationOps, MeasureType, IRIS_DATASET, COVERTYPE_DATASET

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':
    
    try:
        if len(sys.argv) != 6:
            raise Exception('Insufficient amount of arguments')
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
            measureType = MeasureType.GAINRATIO
            measureTypeOut = 'GainRatio'
        elif int(sys.argv[4]) == 3:
            measureType = MeasureType.IMPURITYREDUCTION
            measureTypeOut = 'ImpurityReduction'
        else:
            measureType = MeasureType.GAIN
            measureTypeOut = 'Gain'
        
        evalMode = EvaluationOps.CROSS if int(sys.argv[5]) == 2 else EvaluationOps.NORMAL
        evalModeOut = 'Cross' if int(sys.argv[5]) == 2 else 'Normal'
    except Exception as error:
        print('Caught this error: ' + repr(error))
        sys.exit(1)

    print()
    print("-> COMIENZO DE LA LECTURA")

    dataset = reader.readDataset(datasetFile) 
    model = Model(modelType)
    model.setDataset(dataset)
    
    print()
    print("-> FIN DE LA LECTURA")

    classifier = {
        'dataset': dataset,
        'model': model,
        'attributes': model.getModelAttributesNames(),
        'results': model.getModelResults(),
        'type': modelType,
        'name': modelName,
        'continuous': continuous,
        'measureType': measureType,
    }

    resultFileName = "results/" + datasetOut + ", " + modelName + ", " + str(continuousOut) + ", " + str(measureTypeOut) + ", " + str(evalModeOut) + ".dat"
    print()
    print("-> COMIENZO DE LA EVALUACIÓN")
    if evalMode == EvaluationOps.NORMAL:
        (accuracy, eval, confusionMatrix) = normalValidation(dataset, classifier)
        print()
        print("-> FIN DE LA EVALUACIÓN")

        sys.stdout = open(resultFileName, 'w')
        gui.printNormalEvaluation(classifier, eval, accuracy, confusionMatrix, len(dataset))

    elif evalMode == EvaluationOps.CROSS:
        evalK = 10 # Cambiar si se desean menos
        (eval, evalMean) = crossValidation(dataset, classifier, evalK)
        print()
        print("-> FIN DE LA EVALUACIÓN")

        sys.stdout = open(resultFileName, 'w')
        gui.printCrossEvaluation(classifier, eval, evalMean, len(dataset))

    sys.stdout.close()