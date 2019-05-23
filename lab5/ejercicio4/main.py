### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model.model import Model
import processing.reader as reader
import utils.gui as gui
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps


### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    classifiers = []

    while op == MenuOps.TRAIN or op == MenuOps.EVALUATE or op == MenuOps.PLOT:

        gui.printMenu(classifiers)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            pca_dimension = gui.printPCADimension()
            solver_election = gui.printSolverOptions()
            penalty_election = gui.printPenaltyOptions(solver_election)            
            max_iter = gui.printIterations()
            regulation_strength = gui.printRegulationStrength()
            
            # Leer dataset de respuestas a encuesta
            dataset, candidates, parties = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'pca_dimension': pca_dimension,                
                'solver': solver_election,
                'penalty': penalty_election,
                'max_iter': max_iter,
                'regulation_strength': regulation_strength
            }

            m = Model(dataset.values, candidates.values, parties.values, options)

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            m.train()

            print("-> FIN DEL ENTRENAMIENTO")
            print()

            classifiers.append(m)

        elif op == MenuOps.EVALUATE:

            trainNew = True

            if len(classifiers) > 0:
                gui.printClear()
                gui.printClassifiers(classifiers)

                print("-> Elija un modelo por el índice: ")
                print("-> DEFAULT: 0 (Entrenar modelo nuevo)")

                try:
                    c = int( input() )
                except:
                    c = 0
                c -= 1

                if c >= 0 and c < len(classifiers):

                    k = gui.printCrossK()

                    print()
                    print("-> Evaluación del modelo " + str(c+1))
                    print()

                    evaluation = m.evaluate(k)
                    gui.printEvaluation(evaluation, k)

                    trainNew = False

            if trainNew:

                print()
                print("-> Parte 1 - Entrenamiento")

                pca_dimension = gui.printPCADimension()
                solver_election = gui.printSolverOptions()
                penalty_election = gui.printPenaltyOptions(solver_election)            
                max_iter = gui.printIterations()
                regulation_strength = gui.printRegulationStrength()
                
                # Leer dataset de respuestas a encuesta
                dataset, candidates, parties = reader.readDataset(DATA_ENCUESTAS)

                options = {
                    'pca_dimension': pca_dimension,                
                    'solver': solver_election,
                    'penalty': penalty_election,
                    'max_iter': max_iter,
                    'regulation_strength': regulation_strength
                }

                m = Model(dataset.values, candidates.values, parties.values, options)

                print()
                print("-> COMIENZO DEL ENTRENAMIENTO")
                m.train()
                print("-> FIN DEL ENTRENAMIENTO")
                print()

                classifiers.append(m)

                print("-> Parte 2 - Evaluación")

                k = gui.printCrossK()

                print("-> Evaluación del modelo")
                print()
                
                evaluation = m.evaluate(k)
                gui.printEvaluation(evaluation, k)

        input("-> Oprima enter para volver al menú")
