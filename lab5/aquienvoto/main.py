### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model import pca, k_means
import processing.reader as reader
import processing.parser as parser
import plotting.pcaPlotting as pcaPlotting
import plotting.kMeansPlotting as kMeansPlotting
import utils.gui as gui
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps


### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.LOGISTIC_REGRESSION

    while op == MenuOps.LOGISTIC_REGRESSION or MenuOps.PCA:

        gui.printMenu()
        op = gui.printMenuOption()

        if op == MenuOps.LOGISTIC_REGRESSION:

            solver_election = gui.printSOLVEROptions()
            penalty_election = gui.printPENALTYOptions(solver_election)            
            max_iter = gui.printMaxIterations()
            regulation_strength = gui.printRegulationStrength()

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'solver_election': solver_election,
                'penalty_election': penalty_election,
                'max_iter': max_iter,
                'regulation_strength': regulation_strength,
            }
            
            print(options)
            exit()
            # Aplicar PCA para reducir a 2 dimensiones
            reducedDataset, extras = logistic_regression.train(dataset.values, candidates.values, options)

            # Generar gráficas si es necesario
            pcaPlotting.plotPCA(reducedDataset, candidates, options, extras)

        elif op == MenuOps.PCA:

            # Leer K
            k = gui.printModelK(op)
            iters = gui.printItersK(op)
            kmeans_analysis = gui.printKmeansAnalysis()
            candidate_division = gui.printCandidateDivision(kmeans_analysis)
            kmeans_evaluations = gui.printKmeansEvaluations(k)            

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'kmeans_iters': iters,
                'kmeans_analysis': kmeans_analysis,
                'kmeans_evaluations': kmeans_evaluations,
                'candidate_division': candidate_division,
                'from_notebook': False
            }

            # Aplicar K-Means
            centroids, classes = k_means.k_means(dataset, k, options, candidates)

            # Generar gráficas si es necesario
            kMeansPlotting.plotKMeans(dataset, candidates, centroids, classes, options)
            
        input("-> Oprima enter para volver al menú")
