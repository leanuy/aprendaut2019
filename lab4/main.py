### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model import pca, k_means
import processing.reader as reader
import processing.parser as parser
import processing.processor as processor
import plotting.pcaPlotting as pcaPlotting
import plotting.kMeansPlotting as kMeansPlotting
import utils.gui as gui
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps
from sklearn.metrics import silhouette_score
from sklearn.metrics.cluster import adjusted_rand_score

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.PCA

    while op == MenuOps.PCA or MenuOps.KMEANS:

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
            (centroids, classes, dataset_classified) = k_means.KMeans(K, dataset.values)

            # Calcular el avg del silhouette de todas las filas
            cluster_labels = dataset_classified[:, 26]
            silhouette_avg = silhouette_score(dataset.values, cluster_labels)
            print("silhouette avg: ", silhouette_avg)

            partyJSON = reader.readParties(DATA_CANDIDATOS)
            parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)

            # Calculamos ARI sólo para 11 clusters
            if K == 11:
                # Calcular el Adjusted Rand Index
                # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html
                labels_true = []
                for index in dataset.index:
                    labels_true.append(processor.getParty(parsedParties, candidates[index]))
                ari = adjusted_rand_score(labels_true, cluster_labels)
                print("ARI: ", ari)

            # Plotting
            kMeansPlotting.plotKMeansParties(dataset, candidates, parsedParties, centroids, classes)

        input("-> Oprima enter para volver al menú")
