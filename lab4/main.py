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
<<<<<<< HEAD
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps
from sklearn.metrics import silhouette_score
from sklearn.metrics.cluster import adjusted_rand_score
=======
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps, PCAOps
from sklearn.metrics import silhouette_samples, silhouette_score
>>>>>>> 6d8fb6c83ac68cbfc555d5fc3e26676dc4aa8d2e

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.PCA

    while op == MenuOps.PCA or MenuOps.KMEANS:

        gui.printMenu()
        op = gui.printMenuOption()

        if op == MenuOps.PCA:

            pca_election = gui.printPCAOptions()
            pca_analysis = gui.printPCAnalysis()
            pca_intermediates = gui.printPCAIntermediate(pca_election)

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            options = {
                'pca_election': pca_election,
                'pca_analysis': pca_analysis,
                'pca_intermediates': pca_intermediates
            }

            # Aplicar PCA para reducir a 2 dimensiones
            reducedDataset, extras = pca.reduce_pca(dataset.values, 2, options)

            # Generar
            pcaPlotting.plotPCA(reducedDataset, candidates, options, extras)

        elif op == MenuOps.KMEANS:

            # Leer K
            K = gui.printModelK(op)

            # Leer dataset de respuestas a encuesta
            candidates, dataset = reader.readDataset(DATA_ENCUESTAS)

            # Ejecutar K-Means
            (centroids, classes, dataset_classified) = k_means.KMeans(K, dataset.values)

            # Calcular el avg del silhouette de todas las filas
            cluster_labels = dataset_classified[:, 26]
            silhouette_avg = silhouette_score(dataset.values, cluster_labels, sample_size=22500)
            print("silhouette avg: ", silhouette_avg)

            # Calcular el Adjusted Rand Index
            # link https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html
            # Cambiar el valor de labels_true a lo que corresponda.
            labels_true = cluster_labels
            ari = adjusted_rand_score(labels_true, cluster_labels)
            print("ARI: ", ari)

            # Plotting
            kMeansPlotting.plotKMeansParties(dataset, candidates, centroids, classes)

        input("-> Oprima enter para volver al menú")
