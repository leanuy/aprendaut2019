### DEPENDENCIAS
### ------------------

import numpy as np
from random import randint
from sklearn.cluster import KMeans as skKMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics.cluster import adjusted_rand_score

import processing.reader as reader
import processing.parser as parser
from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, KmeansAnalysis, KmeansEvaluations, CandidateDivision

### METODOS PRINCIPALES
### --------------------

def k_means(dataset, k, options, candidates):

    print()
    if options['kmeans_iters'] == 1:
        (bestCentroids, bestClasses, dataset_classified) = train(dataset.values, k)

    else:
        # Se ejecutan n K-Means, manteniendo el mejor.
        bestSilhouette = -2
        for i in range(options['kmeans_iters']):
            
            print(f'Entrenamiento N° {i+1}')
            
            # Ejecutar K-Means
            (centroids, classes, dataset_classified) = train(dataset.values, k)

            # Calcular el avg del silhouette de todas las filas
            cluster_labels = dataset_classified[:, 26]
            silhouette_avg = silhouette_score(dataset.values, cluster_labels)
            print(f"Coeficiente Silhouette N° {i+1}: {silhouette_avg}")
            print()

            if bestSilhouette < silhouette_avg:
                bestIndex = i+1
                bestSilhouette = silhouette_avg
                bestCentroids = centroids
                bestClasses = classes
                bestClusterLabels = cluster_labels

        print(f'Mejor modelo: N° {bestIndex}')
        print(f'Mejor coeficiente silhouette: {bestSilhouette}')
        print()

    bestClusterLabels = dataset_classified[:, 26]

    silhouette = None
    if options['kmeans_evaluations'] == KmeansEvaluations.SILHOUETTE and options['kmeans_iters'] > 1:
        silhouette = bestSilhouette
    elif options['kmeans_evaluations'] == KmeansEvaluations.SILHOUETTE and options['kmeans_iters'] == 1:
        silhouette = silhouette_score(dataset.values, bestClusterLabels)

    ari = None
    if options['kmeans_evaluations'] == KmeansEvaluations.ARI:
        ari = getARI(dataset, candidates, bestClusterLabels, options['candidate_division'])

    extras = {
      'silhouette': silhouette,
      'ari': ari
    }

    return (bestCentroids, bestClasses, extras)

def train(dataset, k):

  tolerance = 0.0001
  maxIterations = 500
  centroids = {}

  # Initialize the centroids, 'k' random elements in the dataset will be our initial centroids
  for i in range(k):
    centroids[i] = dataset[randint(0, dataset.shape[0] - 1)]
  
  # Begin iteration
  countIterations = 0
  for i in range(maxIterations):
      print(f'-> Iteración N° {i}')
      countIterations += 1
      dataset_with_class = []

      classes = {}
      for j in range(k):
          classes[j] = []

      # Find the distance between the point and cluster; choose the nearest centroid
      for features in dataset:
          # np.linalg.norm calcula la norma euclidea
          distances = [np.linalg.norm(features - centroids[centroid]) for centroid in centroids]
          classification = distances.index(min(distances))
          classes[classification].append(features)

          features_list = list(features)
          features_list.append(classification)
          dataset_with_class.append(features_list)

      # Average the cluster datapoints to re-calculate the centroids
      previous = dict(centroids)
      for classification in classes:
          centroids[classification] = np.average(classes[classification], axis = 0)
      
      # Se revisa si una convergencia fue alcanzada
      convergencia = True
      for centroid in centroids:
          original_centroid = previous[centroid]
          curr = centroids[centroid]
          if np.sum((curr - original_centroid)/original_centroid * 100.0) > tolerance:
              convergencia = False

      # Break out of the main loop if the results are optimal, ie. the centroids don't change their positions much(more than our tolerance)
      if convergencia:
          break

  mejor_varianza = 99999999
  # calculo la varianza y guardo la mejor
  varianza_actual = 0
  for classification in classes:
      varianzas = [np.linalg.norm(example - centroids[classification]) for example in classes[classification]]
      varianza_actual += sum(var for var in varianzas)
  mejor_varianza = min(mejor_varianza,varianza_actual)
  print(f'-> Iteración N° {countIterations} - Convergencia (Varianza = {mejor_varianza})')

  return (centroids, classes, np.array(dataset_with_class))

def classify(dataset, centroids):
  distances = [np.linalg.norm(dataset - centroids[centroid]) for centroid in centroids]
  classification = distances.index(min(distances))
  return classification

### METODOS AUXILIARES
### --------------------

def getARI(dataset, candidates, labels, division):
    # Leer archivo JSON de candidatos para parsear candidatos del dataset 
    partyJSON = None
    if division == CandidateDivision.PARTIES:
        partyJSON = reader.readParties(DATA_CANDIDATOS)
    elif division == CandidateDivision.SPECTRUM:
        partyJSON = reader.readParties(DATA_CANDIDATOS_ESPECTRO)
    elif division == CandidateDivision.NOLAN:
        partyJSON = reader.readParties(DATA_CANDIDATOS_NOLAN)

    # Obtener partidos y candidatos parseados
    # - parsedParties: Lista de tuplas (idPartido, nombrePartido, candidatosPartido)
    # - parsedCandidates: Lista de partidos que preserva el orden de candidatos en el dataset original
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)
    labels_true = []
    for index in dataset.index:
        labels_true.append(parsedCandidates[index-1])

    return adjusted_rand_score(labels_true, labels)
    
def kMeans_sklearn(k, dataset):
  km = skKMeans(n_clusters=k, init='random', n_init=1, max_iter=500, tol=0.0001, n_jobs=-1).fit(dataset)
  print(km.inertia_)
  for centroid in km.cluster_centers_:
      print(centroid)
