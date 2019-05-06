import numpy as np

from random import randint

from sklearn.cluster import KMeans as skKMeans

def KMeans(k, dataset):
  tolerance = 0.0001
  maxIterations = 500
  centroids = {}

  # Initialize the centroids, 'k' random elements in the dataset will be our initial centroids
  for i in range(k):
    centroids[i] = dataset[randint(0, rowLength(dataset) - 1)]
  
  # Begin iteration
  countIterations = 0
  for i in range(maxIterations):
    print(f"Iteración número: {i}")
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
  print(f'Convergencia en iteración: {countIterations}. Mejor Varianza: {mejor_varianza}')
  print()

  return (centroids, classes, np.array(dataset_with_class))

def kMeans_sklearn(k, dataset):
  km = skKMeans(n_clusters=k, init='random', n_init=1, max_iter=500, tol=0.0001, n_jobs=-1).fit(dataset)
  print(km.inertia_)
  for centroid in km.cluster_centers_:
    print(centroid)

def rowLength(dataset):
  return dataset.shape[0]

def columnLength(dataset):
  return dataset.shape[1]

def classify(dataset, centroids):
  distances = [np.linalg.norm(dataset - centroids[centroid]) for centroid in centroids]
  classification = distances.index(min(distances))
  return classification
