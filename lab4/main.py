### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model import pca, k_means
import processing.reader as reader
import processing.parser as parser
import plotting.pcaPlotting as pcaPlotting
import utils.gui as gui
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.PCA

    while op == MenuOps.PCA:

        gui.printMenu()
        op = gui.printMenuOption()

        if op == MenuOps.PCA:
            # Leer tipo de PCA usado
            pca_election = gui.printPCAOptions()
            pca_analysis = gui.printPCAnalysis()

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'pca_election': pca_election,
                'pca_analysis': pca_analysis
            }

            # Aplicar PCA para reducir a 2 dimensiones
            reducedDataset = pca.reduce_pca(dataset.values, 2, options)

            # Generar
            pcaPlotting.plotPCA(reducedDataset, candidates, options)

        elif op == MenuOps.KMEANS:

            # Leer K
            K = gui.printModelK(op)

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            # Ejecutar K-Means
            (centroids, classes) = k_means.KMeans(K, dataset.values)

            # Plotting
            kMeansPlotting.plotKMeans(classes)

            kMeansPlotting.plotKMeansParties(classes, candidates)

        input("-> Oprima enter para volver al menú")