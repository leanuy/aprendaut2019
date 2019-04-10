# Dependencies
# --------------------------------------------------------------------------------
import math
import operator
from scipy.io import arff
import pandas as pd

# Main methods
# --------------------------------------------------------------------------------

# Retrieves a dataset to train
def get_dataset(index):

    ds = []

    if index == 0:
        ds = arff.loadarff('data/autismo.arff')
        df = pd.DataFrame(ds[0])
        ds = df.to_dict('records')
        ds = get_formatted_dataset(ds)

    elif index == 1:
        ds = [ {'temperatura': 'calida' ,'lluvia': 'si',  'horario': 'matutino', 'truth': True},
               {'temperatura': 'templada' ,'lluvia': 'no', 'horario': 'matutino', 'truth': True},
               {'temperatura': 'fria' ,'lluvia': 'si',  'horario': 'nocturno', 'truth': False},
               {'temperatura': 'calida' ,'lluvia': 'no',  'horario': 'matutino', 'truth': False},
               {'temperatura': 'calida' ,'lluvia': 'no',  'horario': 'nocturno', 'truth': True}
             ]

    elif index == 2:
        ds = [ {'temperatura': 10 ,'lluvia': 'si',  'horario': 'matutino', 'truth': True},
               {'temperatura': 20 ,'lluvia': 'no',  'horario': 'matutino', 'truth': True},
               {'temperatura': '?' ,'lluvia': 'no', 'horario': 'matutino', 'truth': False},
               {'temperatura': 10 ,'lluvia': 'no',  'horario': 'nocturno', 'truth': False},
               {'temperatura': 30 ,'lluvia': 'si',  'horario': 'nocturno', 'truth': False}
             ]

    return ds

# Given a dataset "ds", changes some values to be able to be processed by different models
def get_formatted_dataset(ds):
    for x in ds:
        x.pop('result', None)

        x['truth'] = x.pop('Class/ASD')
        if x['truth'] == b'NO':
            x['truth'] = False
        elif x['truth'] == b'YES':
            x['truth'] = True

        for key,val in x.items():
            if key == 'age' and math.isnan(val):
                x[key] = '?'
            if type(val) == bytes:
                x[key] = val.decode("utf-8")

    return ds

# Given a dataset "ds", gets a list of string representing each attribute in the "ds"
def get_attributes_from_dataset(ds):
    attributes = []
    for example in ds:
        for key in list(example.keys()):
            if key not in attributes and key != 'truth':
                attributes.append(str(key))

    return attributes

# Given a dataset "ds" and an attribute "att", returns the possibles values for "attribute" in "ds"
def get_possible_values(ds, att):
    possible_values = set()

    for x in ds:
        possible_values.add(x[att])

    possible_values.discard('?')

    return sorted(list(possible_values))

# Given a dataset "ds", an attribute "att" and a value "value", returns the list of examples in "ds" which have value "value" for attribute "att"
def get_examples_for_value(examples, att, value):
    return [x for x in examples if x[att] == value]

# Given a dataset "ds" and an attribute "att" with missing values, returns a list composed by examples with that value missing
def get_unknown_examples_for_value(ds,att):
    return [x for x in ds if x[att] == '?']

# Continuous methods
# --------------------------------------------------------------------------------

# Checks if "att" is continuous in "ds"
def get_continuity(ds, att):

    # If the first not missing value is numeric returns true, otherwise false
    for x in ds:
       if x[att] != '?':
            if type(x[att]) == int or type(x[att]) == float:
                return True
            else:
                return False

# Given a dataset "ds" and a continuous attribute "att", splits att's domain into intervals based on the changes in the
# result function, returning them as discrete values
def get_possible_continuous_values(ds, att):

    # Get out of the continuous range the missing values
    ds = [x for x in ds if x not in get_unknown_examples_for_value(ds, att)]

    # Sort training examples by att's value
    sorted_ds = sorted(ds, key=operator.itemgetter(att))

    possible_values = []
    old_res = None
    old_x = None

    # Iterate through sorted training examples, adding a new value to whenever the answer changes
    # adding the median value between the current value and the previous one
    for x in sorted_ds:
        res = x['truth']
        if old_res != None and res != old_res:
            mid = ((float(x[att]) - float(old_x)) / 2) + float(old_x)
            possible_values.append(mid)
        old_res = res
        old_x = x[att]

    # Always add at the end a value to represent the values greater than the great interval
    possible_values.append("bigger")

    return possible_values

# Given a dataset "ds" and a continuous attribute "att", splits att's domain into 3 intervals
def get_possible_fixed_continuous_values(ds, att):

    values = get_possible_values(ds, att)
    min_val = min(values)
    max_val = max(values)

    possible_values = []
    possible_values.append((max_val - min_val) / 3 + min_val)
    possible_values.append((max_val - min_val) / 3 + (2* min_val))
    possible_values.append("bigger")

    return possible_values

# Given a dataset "ds", a continuous attribute "att" and an interval "interval", returns the list of examples in "ds"
# which are between interval
def get_examples_for_interval(examples, att, interval, intervals):

    # Get position of interval in list of intervals (always sorted)
    index = intervals.index(interval)

    # If it is the first element, just check if the value is lesser
    if index == 0:
        return [x for x in examples if x[att] <= interval]
    # If it is the last element, just check if the value is greater
    elif interval != "bigger":
        return [x for x in examples if x[att] <= interval and x[att] > intervals[index-1]]
    # If it is an intermediate interval, check if the value is in there
    else:
        return [x for x in examples if x[att] > intervals[index-1]]


# Missing methods
# --------------------------------------------------------------------------------

# Given a dataset "ds" fills every missing value with the most likely value for that attribute
def fill_missing_values(ds, attributes):
    for att in attributes:
        if get_missing(ds,att):
            set_most_likely_value(ds, att)

# Given a dataset "ds" and an attribute "att", discards every example with missing value in att
def discard_missing_values(ds, att):
    new_ds = []
    for x in ds:
        if x[att] != '?':
            new_ds.append(x)

    return new_ds


# Checks if "att" has missing values in "ds"
def get_missing(ds, att):

    # If there is some missing value returns true
    for x in ds:
        if x[att] == '?':
            return True

    # If there are not missing values at all, returns false
    return False

# Given a dataset "ds" and an attribute "att" with missing values, fills them with the most likely value of "att" in "ds"
def get_most_likely_value(ds, att):

    values = get_possible_values(ds, att)
    most_likely = ''
    count = 0

    for value in values:
        large = len([x for x in ds if x[att] == value])
        if (large) > count:
            most_likely = value
            count = large

    return most_likely

# Given a dataset "ds" and an attribute "att" with missing values, fills them with the most likely value of "att" in "ds"
def set_most_likely_value(ds, att):

    most_likely = get_most_likely_value(ds,att)

    for example in ds:
        if example[att] == '?':
            example[att] = most_likely


# KNN methods
# --------------------------------------------------------------------------------

# Given a dataset "ds" and an attribute "att", performs a one hot encoding in att
def one_hot_encode(ds,att):
    values = get_different_values(ds,att)
    for x in ds:
        index = values.index(x[att])
        x[att] = [0] * len(values)
        x[att][index] = 1
    return values

def one_hot_encode_ds(ds):

    knn_ds = list(ds)
    one_hot_encode(knn_ds,'gender')
    one_hot_encode(knn_ds,'ethnicity')
    one_hot_encode(knn_ds,'contry_of_res')
    one_hot_encode(knn_ds,'relation')
    one_hot_encode(knn_ds,'used_app_before')
    one_hot_encode(knn_ds,'jundice')
    one_hot_encode(knn_ds,'austim')
    one_hot_encode(knn_ds,'age_desc')

    return knn_ds

# Given a dataset "ds" and an attribute "att", returns a list with every possible value for "att" in "ds"
def get_different_values(ds, att):
    values = []
    for x in ds:
        if x[att] not in values:
            values.append(x[att])
    return values

# Given a dataset "ds" and an attribute "att", normalizes every value for "att" using euclidean norm
def normalize(ds,att):
    norm = math.sqrt(sum([x[att] ** 2 for x in ds if not math.isnan(x[att])]))
    for x in ds:
        x[att] = x[att] / norm
    return norm

# Given a dataset "ds" and an attribute "att", normalizes every value for "att" using mean and variance
def z_normalize(ds, att):

    tamanio_muestra = len(ds)
    xi = [x[att] for x in ds if not math.isnan(x[att])]
    mean = sum(xi) / tamanio_muestra
    variance = (sum([(x-mean)**2 for x in xi]) ) / tamanio_muestra
    std = math.sqrt(variance)

    for x in ds:
        x[att] = (x[att] - mean) / std
    return (mean, std)

# Given a dataset "ds" and an attribute "att", normalizes every value for "att" using the range of values for "att"
def min_max_normalize(ds,att):

    max = ds[0][att]
    min = ds[0][att]
    for x in ds[1:]:
        if x[att] < min:
            min = x[att]
        if x[att] > max:
            max = x[att]

    for x in ds:
        x[att] = (x[att] - min) / (max-min)
    return (min,max)
