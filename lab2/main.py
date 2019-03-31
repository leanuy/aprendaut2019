### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model.model import Model

import processing.reader as reader
import processing.parser as parser

from evaluation.evaluate import normalValidation, crossValidation

import utils.gui as gui
from utils.const import MenuOps, ModelOps, ContinuousOps, MeasureOps, EvaluationOps 

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    classifiers = []

    while op == MenuOps.TRAIN or op == MenuOps.CLASSIFY or op == MenuOps.EVALUATE or op == MenuOps.SHOW:

        gui.printMenu(classifiers)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            datasetFile = gui.printDataset()
            (modelType, modelName) = gui.printModelType()
            continuous = gui.printContinuousStrategy()
            measure = gui.printMeasureType()

            model = Model(modelType)
            (dataset, attributes, results) = reader.readDataset(datasetFile)
            options = {
              'continuous': continuous,
              'measure': measure
            }

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            tic = time.time()
            model.train(dataset, attributes, results, options)
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print()

            classifier = {
                'model': model,
                'attributes': attributes,
                'results': results,
                'type': modelType,
                'name': modelName,
                'time': toc-tic,
                'options': options,
            }
            classifiers.append(classifier)

            gui.printTrainedClassifier(classifier)
            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.CLASSIFY:

            if classifiers == []:
                print()
                print ("-> No hay clasificadores, entrene uno para clasificar")
                input("-> Oprima enter para volver al menú")

            else:
                gui.printClear()
                gui.printClassifiers(classifiers)

                c = int( input("-> Elija un clasificador por el índice: ") )
                c -= 1
                print("")

                if c >= 0 and c < len(classifiers):
                    print("-> Ingrese un ejemplo a clasificar:")
                    print("ATRIBUTOS: " + str(classifiers[c]['model'].getModelAttributesNames()))
                    example = input()
                    example = parser.getFormattedExample(example, classifiers[c]['model'].getModelAttributesNames())
                    (classification, probability) = classifiers[c]['model'].classify(example)
                    print()
                    print("El ejemplo fue clasificado como ", end=" ")
                    print(classification, end=" ")
                    print("con probabilidad", end=" ")
                    print(probability)
                    input("-> Oprima enter para volver al menú")
                else:
                    print("-> El índice ingresado no corresponde a ningún clasificador")
                    input("-> Oprima enter para volver al menú")

        elif op == MenuOps.EVALUATE:

            datasetFile = gui.printDataset()
            (modelType, modelName) = gui.printModelType()
            continuous = gui.printContinuousStrategy()
            measure = gui.printMeasureType()
            options = {
              'continuous': continuous,
              'measure': measure
            }

            (dataset, attributes, results) = reader.readDataset(datasetFile)            
            model = Model(modelType)

            classifier = {
                'model': model,
                'attributes': attributes,
                'results': results,
                'type': modelType,
                'name': modelName,
                'options': options,
            }

            evalMode = gui.printEvaluationMode()

            if evalMode == EvaluationOps.NORMAL:
                (accuracy, eval, confusionMatrix) = normalValidation(dataset, classifier)
                gui.printNormalEvaluation(classifier, eval, accuracy, confusionMatrix, len(dataset))

            elif evalMode == EvaluationOps.CROSS:
                evalK = gui.printEvaluationK()
                (eval, evalMean) = crossValidation(dataset, classifier, evalK)
                gui.printCrossEvaluation(classifier, eval, evalMean, len(dataset))

            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.SHOW:

            if classifiers == []:
                print()
                print("-> No hay clasificadores, entrene uno para mostrar")

            else:
                gui.printClear()
                gui.printClassifiers(classifiers)

                c = int( input("-> Elija un clasificador por el índice: ") )
                c -= 1
                print("")

                if c >= 0 and c < len(classifiers):
                    classifiers[c]['model'].printClassifier()
                    
                else:
                    print("-> El índice ingresado no corresponde a ningún clasificador")

            input("-> Oprima enter para volver al menú")