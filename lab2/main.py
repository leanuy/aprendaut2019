### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model.model import Model

import utils.gui as gui
from utils.const import MenuOps, ModelOps, ContinuousOps

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    classifiers = []

    while op == MenuOps.TRAIN or op == MenuOps.CLASSIFY or op == MenuOps.EVALUATE:

        gui.printMenu(classifiers)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            (modelType, modelName) = gui.printModelType()
            continuous = gui.printContinuousStrategy()

            model = Model(modelType)

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            tic = time.time()
            model.train(continuous)
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print()

            classifier = {
                'model': model,
                'type': modelType,
                'name': modelName,
                'time': toc-tic,
                'continuous': continuous,
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
                print("")

                if c >= 0 and c < len(classifiers):
                    print("Clasificador " + str(c['name']) + " elegido para clasificar")
                else:
                    print("-> El índice ingresado no corresponde a ningún clasificador")

        elif op == MenuOps.EVALUATE:

            if classifiers == []:
                print()
                print ("-> No hay clasificadores, entrene uno para evaluar")
                input("-> Oprima enter para volver al menú")

            else:
                gui.printClear()
                gui.printClassifiers(classifiers)

                c = int( input("-> Elija un clasificador por el índice: ") )
                print("")

                if c >= 0 and c < len(classifiers):
                    print("Clasificador " + str(c['name']) + " elegido para evaluar")
                else:
                    print("-> El índice ingresado no corresponde a ningún clasificador")