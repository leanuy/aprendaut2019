# Dependencias
# --------------------------------------------------------------------------------
import math
from preprocessor import *

# Métodos principales
# --------------------------------------------------------------------------------

def nb_train(ds, continuousOption = 2, missingOption = 2, m = 0):

    ret = {}
    ret_neg = {}

    counter_pos = {'tot': 0}
    counter_neg = {'tot': 0}

    cant_si = {}
    cant_no = {}

    examples_pos = [x for x in ds if x['truth'] == True]
    examples_neg = [x for x in ds if x['truth'] == False]

    for att in ds[0].keys():

        examples_pos_attribute = [x for x in examples_pos if x[att] != '?']
        cant_si[att] = len(examples_pos_attribute)

        examples_neg_attribute = [x for x in examples_neg if x[att] != '?']
        cant_no[att] = len(examples_neg_attribute)

    continuousAtts = ['age']

    # Para los atributos continuos asume distribucion normal y estima esperanza y varianza,
    # Para resultados positivos y negativos
    if continuousOption == 1:
        for att in ds[0].keys():
            if att in continuousAtts:
                neg_mean = estimate_mean(ds, att, False)
                neg_variance = estimate_variance(ds, att, neg_mean, False)

                pos_mean = estimate_mean(ds, att, True)
                pos_variance = estimate_variance(ds, att, pos_mean, True)

                ret[att] = {'mean': pos_mean, 'variance' : pos_variance}
                ret_neg[att] = {'mean' : neg_mean, 'variance': neg_variance}

    # Las variables counter_pos y counter_neg cuentan las ocurrencias de valores de atributos en ejemplos
    # positivos y negativos respectivamente
    for example in ds:

        counter = counter_pos if example['truth'] else counter_neg
        other_counter = counter_neg if example['truth'] else counter_pos

        for attribute, value in example.items():
            if attribute == 'truth':
                counter['tot'] += 1
                continue
            if missingOption == 0:
                continue
            if (missingOption == 1 and value == '?') or (attribute in continuousAtts and (continuousOption == 0 or continuousOption == 1)):
                continue

            # Si esta el atributo en el diccionario agrega el valor, sino agrega el atributo al diccionario
            if attribute in counter:
                if value in counter[attribute]:
                    counter[attribute][value] += 1
                else:
                    counter[attribute][value] = 1
            else:
                counter[attribute] = {value: 1}

            #Tambien agrega el atributo al otro diccionario, esto es para asegurarse que ambos diccionarios
            #tengan los mismos elementos
            if not attribute in other_counter:
                other_counter[attribute] = {value: 0}
            elif not value in other_counter[attribute]:
                other_counter[attribute][value] = 0

        counter_pos = counter if example['truth'] else other_counter
        counter_neg = other_counter if example['truth'] else counter

    #Aca se cuentan las probabilidades en base a cuantos ejemplos positivos / negativos hay
    for key, values in counter_pos.items():

        if key == 'tot':
            ret[key] = counter_pos[key] / (counter_pos[key] + counter_neg[key])
            ret_neg[key] = counter_neg[key] / (counter_pos[key] + counter_neg[key])
            continue

        ret[key] = {}
        ret_neg[key] = {}

        #Considera que hay una opcion mas para el m-estimador (la opcion ?/atributo no observado)
        values_number = (len(counter_pos[key]) + 1)

        #Aca se crea el diccionario de probabilidades, usando m como el factor de normalizacion
        for value, number in values.items():
            m_est = m if missingOption == 1 else 0
            ret[key][value] = (counter_pos[key][value] + m_est/values_number) / (cant_si[key] + m_est)
            ret_neg[key][value] = (counter_neg[key][value] + m_est/values_number) / (cant_no[key] + m_est)

    return (ret, ret_neg)

def nb_classify(ds, example, continuousOption = 0, missingOption = 0, m = 0):

    (probabilities, probabilities_neg) = ds

    pos = probabilities['tot']
    neg = probabilities_neg['tot']

    continuousAtts = ['age']

    for key, value in example.items():

        if key == 'tot': continue

        if key in continuousAtts and continuousOption == 1 and value != '?':
            gaussian_normal(float(value), probabilities[key]['mean'], probabilities[key]['variance'])
            pos = pos * gaussian_normal(float(value), probabilities[key]['mean'], probabilities[key]['variance'])
            neg = neg * gaussian_normal(float(value), probabilities_neg[key]['mean'], probabilities_neg[key]['variance'])
            continue

        elif missingOption == 2:
            has_value_pos = (value == '?' or not value in probabilities[key])
            has_value_neg = (value == '?' or not value in probabilities_neg[key])
            mult_pos = 1 if has_value_pos else probabilities[key][value]
            mult_neg = 1 if has_value_neg else probabilities_neg[key][value]
            pos = pos * mult_pos
            neg = neg * mult_neg

        elif missingOption == 1 and (value == '?' or not value in probabilities[key]):
            has_value_pos = (value == '?' or not value in probabilities[key])
            has_value_neg = (value == '?' or not value in probabilities_neg[key])
            mult_pos = m/(len(probabilities[key]) + 1) if has_value_pos else probabilities[key][value]
            mult_neg = m/(len(probabilities[key]) + 1) if has_value_neg else probabilities_neg[key][value]
            pos = pos * mult_pos
            neg = neg * mult_neg

        else:
            pos = pos * probabilities[key][value]
            neg = neg * probabilities_neg[key][value]

    return pos > neg

# Auxiliar methods
# --------------------------------------------------------------------------------

def estimate_mean(ds, att, truth):
    values_used = [x for x in ds if x[att] != '?' and x['truth'] == truth]
    values = [x[att]/len(values_used) for x in values_used]
    return sum(values)

def estimate_variance(ds, att, mean, truth):
    values = [(x[att] - mean) ** 2 for x in ds if x[att] != '?' and x['truth'] == truth]
    return math.sqrt(sum(values)/(len(values) - 1))

def gaussian_normal(value, mean, variance):
    return math.exp(-((value-mean)/(2*variance))**2)/(math.sqrt(2*math.pi*variance**2))
