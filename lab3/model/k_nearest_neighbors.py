### DEPENDENCIAS
### ------------------
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree

from utils.const import MeasureOps, DistanceOps, NormOps, DistanceMetrics

### METODOS PRINCIPALES
### -------------------

def knnTrain(dataset, attributes, results, options):

    to_return = {}
    norm = options['norm']
    
    if norm == NormOps.NONE:
        to_return['dataset'] = dataset
     
    elif norm == NormOps.EUCLIDEAN:
        modifiedDataset = dataset.copy()
        modifiedDataset = modifiedDataset.drop(columns=['class'])
        modifiedDataset = modifiedDataset.apply(lambda row: np.divide(row, np.sqrt(sum(np.power(row, 2)))), axis = 1)
        classes = dataset.loc[:, 'class']
        modifiedDataset['class'] = classes
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

    ds = to_return['dataset'].drop(columns=['class'])
    to_return['kdtree'] = KDTree(ds.values, leaf_size=8, metric=DistanceMetrics[options['measure']])   
    return to_return

def knnClassify(classifier, example, attributes, results, options):

    if options['norm'] == NormOps.EUCLIDEAN:
        example = np.divide(example, np.sqrt(sum(np.power(example, 2))))

    elif options['norm'] == NormOps.Z_SCORE:
        for attr in attributes:
            (key, attrType) = attr
            value = example[key]
            value -= classifier['mean'][key]
            value /= classifier['std'][key]
            example[key] = value

    elif options['norm'] == NormOps.MIN_MAX:
        for attr in attributes:
            (key, attrType) = attr
            value = example[key]
            value -= classifier['min'][key]
            value /= (classifier['max'][key] + classifier['min'][key])
            example[key] = value
   
    elif options['norm'] == NormOps.NONE:
        pass

    dataset = classifier['dataset']
    dist, indexes = classifier['kdtree'].query(example.values.reshape(1,-1), k=options['k'])
    winners = dataset.iloc[indexes[0]]['class'].tolist()
    
    classes = {}

    for res in results:
        if res not in classes.keys():
            classes[res] = 0
        
    for n in winners:
        classes[n] += 1

    winner = None
    max_class = -1
    for res in classes.keys():
        if classes[res] > max_class:
            max_class = classes[res]
            winner = res
    
    return winner, max_class / len(winners)


