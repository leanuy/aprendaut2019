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

    while op == MenuOps.TRAIN or op == MenuOps.CLASSIFY or op == MenuOps.EVALUATE or op == MenuOps.PLOT:

        gui.printMenu(classifiers)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            pca_dimension = gui.printPCADimension()
            solver_election = gui.printSolverOptions()
            penalty_election = gui.printPenaltyOptions(solver_election)            
            max_iter = gui.printIterations()
            regulation_strength = gui.printRegulationStrength()
            
            # Leer dataset de respuestas a encuesta
            dataset, candidates = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'pca_dimension': pca_dimension,                
                'solver': solver_election,
                'penalty': penalty_election,
                'max_iter': max_iter,
                'regulation_strength': regulation_strength
            }

            m = Model(dataset.values, candidates.values, options)

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            m.train()

            print("-> FIN DEL ENTRENAMIENTO")
            print()

            classifiers.append(m)

        input("-> Oprima enter para volver al menú")
