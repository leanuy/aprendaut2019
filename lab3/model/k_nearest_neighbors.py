### DEPENDENCIAS
### ------------------


### METODOS PRINCIPALES
### -------------------

def knnTrain(dataset, attributes, results, options):
    # for index in dataset.index:
    #     for attr in attributes:
    #         print(dataset.at[index, attr[0]], ',', end='')
    #     print()

    
    print(len(attributes))
    print(len(results))
    return
    knn_ds = list(ds)
    knn_ds_2 = list(ds)
    to_return = {'dataset': dataset}


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

def knnClassify(classifier, example, results):
    pass
    # k_nearest = []

	# normAtts = ['age']
	
	# for att in normAtts:
	# 	if example[att] != '?':
	# 		if classifier['normalize'][0] == '1' :
	# 			example[att] = example[att] / classifier['normalize'][1]
	# 		elif classifier['normalize'][0] == '2' :
	# 			(min_val, max_val) = classifier['normalize'][1]
	# 			example[att] = (example[att] - min_val) /(max_val-min_val)
	# 		elif classifier['normalize'][0] == '3' :
	# 			(mean, std) = classifier['normalize'][1]
	# 			example[att] = (example[att] - mean) / std

	# for x in classifier['dataset']:
	# 	distance = get_distance(x, example, missingOption)
	# 	if not math.isnan(distance):
	# 		k_nearest.append({'ejemplo': x, 'distancia': distance})

	# k_nearest = sorted(k_nearest, key=itemgetter('distancia'))[:k]
	# suma_pos = len( [ x for x in k_nearest if x['ejemplo']['truth'] ] )
	# suma_neg = len( [ x for x in k_nearest if not x['ejemplo']['truth'] ] )

	# return suma_pos > suma_neg

def entrenar(self,ejemplos, atributo_objetivo, atributos):
    self.ejemplos = ejemplos
    self.atributo_objetivo = atributo_objetivo
    self.atributos = atributos
    self.maximos, self.minimos = valores_maximos_minimos_atributos(ejemplos, atributos)


def clasificar(self, ejemplo):
    ordenado = deepcopy(self.ejemplos)
    #ordeno los ejemplos segun la distancia a ejemplo
    ordenado = self.ordenar(ordenado, self.atributos, ejemplo)

    valores = []
    # separo los k vecinos cercanos y obtengo el valor del objetivo.
    for n in ordenado[0:self.k]:
        valores.append(n[self.atributo_objetivo.get_pos()])

    #retorno el valor mas comun
    return objetivo_mas_comun(valores)

#ordena un conjunto de ejemplos respecto a la distancia a un ejemplo
def ordenar(self, ejemplos, atributos, ejemplo):
    # aca cargar los mas comunes
    comunes = valores_mas_comunes_para_cada_atributo(ejemplos, atributos)
    ordenados = []
    for e in ejemplos:
        ordenados.append([e, distancia1(ejemplo, e, atributos, comunes, self.maximos, self.minimos)])
    ordenados.sort(key = lambda x: x[1])
    return [x[0] for x in ordenados]