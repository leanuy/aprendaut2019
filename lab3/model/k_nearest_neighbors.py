### DEPENDENCIAS
### ------------------
import numpy as np
import time

from utils.const import MeasureOps, DistanceOps, NormOps

### METODOS PRINCIPALES
### -------------------

def knnTrain(dataset, attributes, results, options):

    to_return = {}

    k = options['k']
    distanceType = options['measure']
    norm = options['norm']

    to_return['k'] = k
    to_return['distance'] = distanceType
    to_return['norm'] = norm
    to_return['attributes'] = attributes
    to_return['results'] = results
    
    if norm == NormOps.NONE:
        to_return['dataset'] = dataset
     
    elif norm == NormOps.EUCLIDEAN:
        modifiedDataset = dataset.copy()
        modifiedDataset = modifiedDataset.drop(columns=['class'])
        modifiedDataset = modifiedDataset.apply(lambda row: np.divide(row, np.sqrt(sum(np.power(row, 2)))), axis = 1)
        classes = dataset.loc[:, 'class']
        modifiedDataset = modifiedDataset.assign(class_col=classes)
        to_return['dataset'] = modifiedDataset

    elif norm == NormOps.Z_SCORE or norm == NormOps.MIN_MAX:
        mean_dict = {}
        std_dict = {}
        max_dict = {}
        min_dict = {}
        for attr in attributes:
            (key, attrType) = attr
            data_column = dataset.loc[:,key]
            if norm == NormOps.Z_SCORE:
                mean_dict[key] = np.mean(data_column, axis=0)
                std_dict[key] = np.std(data_column, axis=0)
            elif norm == NormOps.MIN_MAX:
                max_dict[key] = np.max(data_column, axis=0)
                min_dict[key] = np.min(data_column, axis=0)

        modifiedDataset = dataset.copy()
        if norm == NormOps.Z_SCORE:
            modifiedDataset = dataset.copy()
            for index in modifiedDataset.index:
                for attr in attributes:
                    (key, attrType) = attr
                    element = modifiedDataset.at[index, key]
                    element -= mean_dict[key]
                    element /= std_dict[key]
                    modifiedDataset.at[index, key] = element
            
            to_return['dataset'] = modifiedDataset
            to_return['mean'] = mean_dict
            to_return['std'] = std_dict
        elif norm == NormOps.MIN_MAX:
            for index in modifiedDataset.index:
                for attr in attributes:
                    (key, attrType) = attr
                    element = modifiedDataset.at[index, key]
                    element -= min_dict[key]
                    element /= (max_dict[key] + min_dict[key])
                    modifiedDataset.at[index, key] = element
            
            to_return['dataset'] = modifiedDataset
            to_return['max'] = max_dict
            to_return['min'] = min_dict

    return to_return

def knnClassify(classifier, example):

    example = example.drop('class')

    if classifier['norm'] == NormOps.EUCLIDEAN:
        example = np.divide(example, np.sqrt(sum(np.power(example, 2))))

    elif classifier['norm'] == NormOps.Z_SCORE:
        for attr in classifier['attributes']:
            (key, attrType) = attr
            value = example[key]
            value -= classifier['mean'][key]
            value /= classifier['std'][key]
            example[key] = value

    elif classifier['norm'] == NormOps.MIN_MAX:
        for attr in classifier['attributes']:
            (key, attrType) = attr
            value = example[key]
            value -= classifier['min'][key]
            value /= (classifier['max'][key] + classifier['min'][key])
            example[key] = value
   
    elif classifier['norm'] == NormOps.NONE:
        pass

    tic = time.time()
    dataset = classifier['dataset'].reset_index()
    toc = time.time()

    print('Tiempo de reseteo de indices: ' + str(toc-tic))
    print()

    tic = time.time()
    distances = dataset.apply(lambda point: distance(example, point, classifier['attributes'], classifier['distance'], classifier['norm']), axis = 1)
    toc = time.time()
    print('Tiempo de calculo de distancias: ' + str(toc-tic))
    print()

    tic = time.time()
    dataset = dataset.assign(distances=distances)
    toc = time.time()
    print('Tiempo de agregado de columna: ' + str(toc-tic))
    print()

    tic = time.time()
    dataset = dataset.sort_values('distances')
    toc = time.time()
    print('Tiempo de reordenamiento de dataset: ' + str(toc-tic))
    print()
   
    if classifier['norm'] == NormOps.EUCLIDEAN:
        winners = dataset.loc[:, 'class_col'].tolist()
    else:
        winners = dataset.loc[:, 'class'].tolist()

    return classification(winners[0:classifier['k']], classifier['results'])


def distance(example, point, attributes, distanceType, norm):

    point = point.drop('index')
    if norm == NormOps.EUCLIDEAN:
        point = point.drop('class_col')
    else:
        point = point.drop('class')

    if distanceType == DistanceOps.MANHATTAN:
        res = np.sum(np.absolute(np.subtract(example, point)), axis = 0)
    
    elif distanceType == DistanceOps.EUCLIDEAN:
        res = np.sqrt(np.sum(np.power(np.subtract(example, point), 2), axis = 0))

    elif distanceType == DistanceOps.CHEBYCHEV:
        res = np.max(np.absolute(np.subtract(example, point)), axis = 0)

    elif distanceType == DistanceOps.MAHALANOBIS:
        pass

    return res

def classification(k_nearest, results):
    classes = {}

    for res in results:
        if res not in classes.keys():
            classes[res] = 0
        
    for n in k_nearest:
        classes[n] += 1

    winner = None
    max_class = -1
    for res in classes.keys():
        if classes[res] > max_class:
            max_class = classes[res]
            winner = res
    
    return winner, max_class / len(k_nearest)
