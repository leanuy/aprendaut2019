Para ejecutar el laboratorio, debe situarse en el mismo directorio que main.py y correr en python 3:
python main.py
Luego se le va a desplegar el siguiente menú, del cual puede elegir que acción realizar:

#######################################################
#                                                     #
#        MENÚ - Laboratorio 3 (Clasificadores)        #
#                                                     #
#######################################################

Clasificadores actuales:

1. Entrenar
2. Clasificar
3. Evaluar
4. Mostrar
0. Salir

-> Elija una opción:

--------------------------------------------------------------------------------------------------------

Para poder utilizar covertype, es necesario generar un archivo "covertype.arff" en la carpeta "data". La estructura del mismo
consiste en un cabezal arff y los datos, tal como se encuentran en la fuente.

El cabezal utilizado cuenta con la siguiente estructura:

@attribute elevation numeric
@attribute aspect numeric
@attribute slope numeric
@attribute horizontal_distance_to_hydrology numeric
@attribute vertical_distance_to_hydrology numeric
@attribute horizontal_distance_to_roadways numeric
@attribute hillshade_9am numeric
@attribute hillshade_noon numeric
@attribute hillshade_3pm numeric
@attribute horizontal_distance_to_fire_points numeric
@attribute wilderness_area_0 {0,1}
@attribute wilderness_area_1 {0,1}
@attribute wilderness_area_2 {0,1}
@attribute wilderness_area_3 {0,1}
@attribute soil_type_0 {0,1}
@attribute soil_type_1 {0,1}
@attribute soil_type_2 {0,1}
@attribute soil_type_3 {0,1}
@attribute soil_type_4 {0,1}
@attribute soil_type_5 {0,1}
@attribute soil_type_6 {0,1}
@attribute soil_type_7 {0,1}
@attribute soil_type_8 {0,1}
@attribute soil_type_9 {0,1}
@attribute soil_type_10 {0,1}
@attribute soil_type_11 {0,1}
@attribute soil_type_12 {0,1}
@attribute soil_type_13 {0,1}
@attribute soil_type_14 {0,1}
@attribute soil_type_15 {0,1}
@attribute soil_type_16 {0,1}
@attribute soil_type_17 {0,1}
@attribute soil_type_18 {0,1}
@attribute soil_type_19 {0,1}
@attribute soil_type_20 {0,1}
@attribute soil_type_21 {0,1}
@attribute soil_type_22 {0,1}
@attribute soil_type_23 {0,1}
@attribute soil_type_24 {0,1}
@attribute soil_type_25 {0,1}
@attribute soil_type_26 {0,1}
@attribute soil_type_27 {0,1}
@attribute soil_type_28 {0,1}
@attribute soil_type_29 {0,1}
@attribute soil_type_30 {0,1}
@attribute soil_type_31 {0,1}
@attribute soil_type_32 {0,1}
@attribute soil_type_33 {0,1}
@attribute soil_type_34 {0,1}
@attribute soil_type_35 {0,1}
@attribute soil_type_36 {0,1}
@attribute soil_type_37 {0,1}
@attribute soil_type_38 {0,1}
@attribute soil_type_39 {0,1}
@attribute class {1,2,3,4,5,6,7}

@data

--------------------------------------------------------------------------------------------------------

Para correr varios entrenamientos de manera automática y obtener sus resultados, debe ir a la carpeta
autorun del proyecto y editar autorun.sh (en linux) o autorun.bat (en windows).

El formato de comandos a ejecutar es el siguiente:

# Para agregar códigos a correr agregan la cantidad de lineas:
# python automain.py DATASET MODEL EVALUATION ... (parámetros que dependen del modelo, detallados a continuación)
# DATASET = { 1: Iris, 2: Covertype }
# MODEL = { 1: Arbol, 2: Bosque, 3: Naive Bayes, 4: KNN }
# EVALUATION = { 1: Validación Simple (80/20), 2: Validación Cruzada }

# Arboles o Bosques:
# python automain.py DATASET MODEL EVALUATION CONTINUOUS MEASURE
# CONTINUOUS = { 1: Intervalos Fijos, 2: Intervalos Variables, 3: Maximizando Ganancia }
# MEASURE = { 1: Ganancia, 2: Ratio de Ganancia, 3: Reducción de Impureza }

# python automain.py (1|2) (1|2) (1|2) (1|2|3) (1|2|3)
# EJ: python automain.py 2 2 1 2 3

# Bayes:
# python automain.py DATASET MODEL EVALUATION ONEHOT CONTINUOUS mEST
# ONEHOT = { 1: Deshacer Onehot Encoding, 2: Conservar Onehot Encoding }
# CONTINUOUS = { 1: Estandarización normal, 2: Intervalos Variables }
# mEST = n, real no negativo

# python automain.py (1|2) 3 (1|2) (1|2) (1|2) (n)
# EJ: python automain.py 2 3 1 1 1 0.5

# KNN:
# python automain.py DATASET MODEL EVALUATION ONEHOT K MEASURE NORM WEIGHTED
# ONEHOT = { 1: Deshacer Onehot Encoding, 2: Conservar Onehot Encoding }
# K = n, Entero positivo (se prefieren impares)
# MEASURE = { 1: Distancia 'Manhattan', 2: Distancia Euclidea, 3: Distancia de Chebychev, 4: Distancia de Mahalanobis }
# NORM = { 1: Norma Euclidea, 2: Norma Min-Max, 3: Norma Z-Score, 4: Ninguna Norma }
# WEIGHTED = { 1: Votacion ponderada, 2: Votacion sin ponderar }

# python automain.py (1|2) 4 (1|2) (1|2) (1..n) (1|2|3|4) (1|2|3|4) (1|2)
# EJ: python automain.py 2 4 1 1 3 2 1 1
