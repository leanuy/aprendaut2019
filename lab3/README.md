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
