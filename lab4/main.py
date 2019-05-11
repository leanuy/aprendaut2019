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

    op = MenuOps.PCA

    while op == MenuOps.PCA or MenuOps.KMEANS:

        gui.printMenu()
        op = gui.printMenuOption()

        if op == MenuOps.PCA:

            pca_election = gui.printPCAOptions()
            pca_intermediates = gui.printPCAIntermediate(pca_election)            
            pca_analysis = gui.printPCAnalysis()
            candidate_division = gui.printCandidateDivision(pca_analysis)

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'pca_election': pca_election,
                'pca_analysis': pca_analysis,
                'pca_intermediates': pca_intermediates,
                'candidate_division': candidate_division
            }

            # Aplicar PCA para reducir a 2 dimensiones
            reducedDataset, extras = pca.reduce_pca(dataset.values, 2, options)

            # Generar gráficas si es necesario
            pcaPlotting.plotPCA(reducedDataset, candidates, options, extras)

        elif op == MenuOps.KMEANS:

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
                'candidate_division': candidate_division
            }

            # Aplicar PCA para reducir a 2 dimensiones
            centroids, classes, extras = k_means.k_means(dataset, k, options, candidates)

            # Generar gráficas si es necesario
            kMeansPlotting.plotKMeans(dataset, candidates, centroids, classes, options, extras)
            
        input("-> Oprima enter para volver al menú")
