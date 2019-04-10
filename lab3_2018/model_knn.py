# Dependencies
# --------------------------------------------------------------------------------
import pdb
import math
from operator import itemgetter
from preprocessor import *

# Métodos principales
# --------------------------------------------------------------------------------

def knn_train(ds, k, missingOption = 0, normOption = 3, isEvaluating = False):
    
    knn_ds = list(ds)
    knn_ds_2 = list(ds)
    to_return = {'dataset': knn_ds}

    if missingOption == 1:
    	fill_missing_values(ds, get_attributes_from_dataset(ds))

    normAtts = ['age']

    for att in normAtts:
    	if missingOption == 2:
    		knn_ds_2 = discard_missing_values(knn_ds, att)

    for att in normAtts:
        if normOption == 1:
            to_return['normalize']= ('1',normalize(knn_ds_2, att))
        elif normOption == 2:
            to_return['normalize']= ('2',min_max_normalize(knn_ds_2, att))
        elif normOption == 3:
            to_return['normalize']= ('3',z_normalize(knn_ds_2, att))

    if not isEvaluating:
	    one_hot = []
	    one_hot.append(('gender',one_hot_encode(knn_ds,'gender')))
	    one_hot.append(('ethnicity',one_hot_encode(knn_ds,'ethnicity')))
	    one_hot.append(('contry_of_res',one_hot_encode(knn_ds,'contry_of_res')))
	    one_hot.append(('relation',one_hot_encode(knn_ds,'relation')))
	    one_hot.append(('used_app_before',one_hot_encode(knn_ds,'used_app_before')))
	    one_hot.append(('jundice',one_hot_encode(knn_ds,'jundice')))
	    one_hot.append(('austim',one_hot_encode(knn_ds,'austim')))
	    one_hot.append(('age_desc',one_hot_encode(knn_ds,'age_desc')))
	    to_return['one_hot'] = one_hot

    return to_return

def knn_classify(classifier, example, k, missingOption, normOption):

	k_nearest = []

	normAtts = ['age']
	
	for att in normAtts:
		if example[att] != '?':
			if classifier['normalize'][0] == '1' :
				example[att] = example[att] / classifier['normalize'][1]
			elif classifier['normalize'][0] == '2' :
				(min_val, max_val) = classifier['normalize'][1]
				example[att] = (example[att] - min_val) /(max_val-min_val)
			elif classifier['normalize'][0] == '3' :
				(mean, std) = classifier['normalize'][1]
				example[att] = (example[att] - mean) / std

	for x in classifier['dataset']:
		distance = get_distance(x, example, missingOption)
		if not math.isnan(distance):
			k_nearest.append({'ejemplo': x, 'distancia': distance})

	k_nearest = sorted(k_nearest, key=itemgetter('distancia'))[:k]
	suma_pos = len( [ x for x in k_nearest if x['ejemplo']['truth'] ] )
	suma_neg = len( [ x for x in k_nearest if not x['ejemplo']['truth'] ] )

	return suma_pos > suma_neg

# Métodos auxiliares
# --------------------------------------------------------------------------------

def get_distance(example, new_example, missingOption):
    distance = 0
    for key, value in example.items():
        if key == 'truth':
            continue
        elif example[key] == '?' or new_example[key] == '?':
        	continue
        if type(example[key]) is list:
            distance += get_vector_distance(example[key], new_example[key])
        else:
            distance += (float(example[key]) - float(new_example[key])) ** 2
    return distance

def get_vector_distance(example, new_example):
    distance = 0
    for i in range(len(example)):
        distance += (example[i] - new_example[i]) ** 2


    return distance
