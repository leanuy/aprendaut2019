### DEPENDENCIAS
### ------------------
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree

from utils.const import MeasureOps, DistanceOps, NormOps, DistanceMetrics

### METODOS PRINCIPALES
### -------------------

def knnTrain(dataset, attributes, results, options):

    classificator = {}
    norm = options['norm']
    structure = options['structure']
    
    # No normalizar
    if norm == NormOps.NONE:
        classificator['dataset'] = dataset
    
    # Normalizar utilizando norma euclidea
    elif norm == NormOps.EUCLIDEAN:
        modifiedDataset = dataset.copy()
        
        # Dividir todos los elementos de cada fila entre su norma euclidea (Ignorando su clasificacion)
        modifiedDataset = modifiedDataset.drop(columns=['class'])
        modifiedDataset = modifiedDataset.apply(lambda row: np.divide(row, np.sqrt(sum(np.power(row, 2)))), axis = 1)

        # Unir columna de clases de nuevo
        classes = dataset.loc[:, 'class']
        modifiedDataset['class'] = classes
        
        classificator['dataset'] = modifiedDataset

    # Normalizar utilizando reescalamiento
    elif norm == NormOps.MIN_MAX:

        # Obtener maximo y minimo de cada atributo
        maxDict = {}
        minDict = {}
        for attr in attributes:
            (key, attrType) = attr
            data_column = dataset.loc[:,key]
            maxDict[key] = np.max(data_column, axis=0)
            minDict[key] = np.min(data_column, axis=0)

        # Reescalar todos los elementos de cada fila utilizando max y min para cada atributo
        modifiedDataset = dataset.copy()
        for index in modifiedDataset.index:
            for attr in attributes:
                (key, attrType) = attr
                element = modifiedDataset.at[index, key]
                element -= minDict[key]
                element /= (maxDict[key] + minDict[key])
                modifiedDataset.at[index, key] = element
        
        classificator['dataset'] = modifiedDataset
        classificator['max'] = maxDict
        classificator['min'] = minDict

    # Normalizar utilizando estandarizacion
    elif norm == NormOps.Z_SCORE:

        # Obtener media y desviacion estandar de cada atributo
        meanDict = {}
        stdDict = {}
        for attr in attributes:
            (key, attrType) = attr
            data_column = dataset.loc[:,key]
            meanDict[key] = np.mean(data_column, axis=0)
            stdDict[key] = np.std(data_column, axis=0)

        # Estandarizar todos los elementos de cada fila utilizando mean y std para cada atributo
        modifiedDataset = dataset.copy()
        for index in modifiedDataset.index:
            for attr in attributes:
                (key, attrType) = attr
                element = modifiedDataset.at[index, key]
                element -= meanDict[key]
                element /= stdDict[key]
                modifiedDataset.at[index, key] = element
            
        classificator['dataset'] = modifiedDataset
        classificator['mean'] = meanDict
        classificator['std'] = stdDict

    # Una vez normalizado el dataset, generar KDTree
    if structure:
        ds = classificator['dataset'].drop(columns=['class'])
        classificator['kdtree'] = KDTree(ds.values, leaf_size=8, metric=DistanceMetrics[options['measure']])

    return classificator

def knnClassify(classifier, example, attributes, results, options):

    # Normalizar ejemplo con norma euclidea
    if options['norm'] == NormOps.EUCLIDEAN:
        example = np.divide(example, np.sqrt(sum(np.power(example, 2))))

    # Normalizar ejemplo con reescalamiento
    elif options['norm'] == NormOps.MIN_MAX:
        for attr in attributes:
            (key, attrType) = attr
            value = example[key]
            value -= classifier['min'][key]
            value /= (classifier['max'][key] + classifier['min'][key])
            example[key] = value

    # Normalizar ejemplo con estandarizacion
    elif options['norm'] == NormOps.Z_SCORE:
        for attr in attributes:
            (key, attrType) = attr
            value = example[key]
            value -= classifier['mean'][key]
            value /= classifier['std'][key]
            example[key] = value

    dataset = classifier['dataset']

    # Obtener K vecinos mas cercanos utilizando estructura KDTree
    if options['structure']:
        dist, indexes = classifier['kdtree'].query(example.values.reshape(1,-1), k=options['k'])
        winners = dataset.iloc[indexes[0]]['class'].tolist()
        #indexes, distances = classifier['kdtree'].query_radius(example.values.reshape(1,-1), 1, return_distance=True, sort_results=True)
        #winners = dataset.iloc[indexes[0][:options['k']]]['class'].tolist()
    
    # Obtener K vecinos mas cercanos buscando en todo el dataset
    else:
        datasetWithoutClass = dataset.drop(columns=['class'])

        # Calcular distancias al ejemplo para todo el dataset
        if options['measure'] == DistanceOps.MANHATTAN:
            distances = np.sum(np.absolute(np.subtract(datasetWithoutClass.values, example.values)), axis = 1).transpose()
        elif options['measure'] == DistanceOps.EUCLIDEAN:
            distances = np.sqrt(np.sum(np.power(np.subtract(datasetWithoutClass.values, example.values), 2), axis = 1)).transpose()
        elif options['measure'] == DistanceOps.CHEBYCHEV:
            distances = np.max(np.absolute(np.subtract(datasetWithoutClass.values, example.values)), axis = 1).transpose()

        # Obtener indices de cada fila, asociarlos a su distancia al ejemplo y ordenarlos ascendentemente por distancia
        distancesDataframe = pd.DataFrame({'distances': distances}, index=dataset.index.values)
        distancesDataframe = distancesDataframe.sort_values('distances')

        # Obtener los primeros k elementos 
        kIndexes = distancesDataframe.index.values[:options['k']]
        winners = dataset.loc[kIndexes, 'class'].tolist()
    
    # Generar estructura para votar
    classes = {}
    for res in results:
        if res not in classes.keys():
            classes[res] = 0
    for n in winners:
        classes[n] += 1

    # Realizar votacion entre ganadores
    winner = None
    maxClass = -1
    for res in classes.keys():
        if classes[res] > maxClass:
            maxClass = classes[res]
            winner = res
    
    return winner, maxClass / len(winners)


