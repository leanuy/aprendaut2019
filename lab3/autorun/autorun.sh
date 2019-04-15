# Para agregar codigos a correr agregan la cantidad de lineas:
# python3 automain.py dataset model continuous measure validation
# dataset = 1..2
# model = 1..2
# continuous = 1..3
# measure = 1..3
# validation = 1..2

# IRIS - NB
# -----------------------------------------------------------------------------------

# Fijo: Iris, NB, Normal, Deshacer Onehot, Normal Dist
python automain.py 1 3 1 1 1 0
python automain.py 1 3 1 1 1 0.01
python automain.py 1 3 1 1 1 0.5
python automain.py 1 3 1 1 1 1
python automain.py 1 3 1 1 1 100

# Fijo: Iris, NB, Normal, Deshacer Onehot, Variables
python automain.py 1 3 1 1 2 0
python automain.py 1 3 1 1 2 0.01
python automain.py 1 3 1 1 2 0.5
python automain.py 1 3 1 1 2 1
python automain.py 1 3 1 1 2 100

# Fijo: Iris, NB, Cross, Deshacer Onehot, Normal Dist
python automain.py 1 3 2 1 1 0
python automain.py 1 3 2 1 1 0.01
python automain.py 1 3 2 1 1 0.5
python automain.py 1 3 2 1 1 1
python automain.py 1 3 2 1 1 100

# Fijo: Iris, NB, Cross, Deshacer Onehot, Variables
python automain.py 1 3 2 1 2 0
python automain.py 1 3 2 1 2 0.01
python automain.py 1 3 2 1 2 0.5
python automain.py 1 3 2 1 2 1
python automain.py 1 3 2 1 2 100

# IRIS - KNN
# -----------------------------------------------------------------------------------

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 1, Distancia Manhattan
python automain.py 1 4 1 1 1 1 1
python automain.py 1 4 1 1 1 1 2
python automain.py 1 4 1 1 1 1 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 1, Distancia Euclidea
python automain.py 1 4 1 1 1 2 1
python automain.py 1 4 1 1 1 2 2
python automain.py 1 4 1 1 1 2 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 1, Distancia Chebychev
python automain.py 1 4 1 1 1 3 1
python automain.py 1 4 1 1 1 3 2
python automain.py 1 4 1 1 1 3 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 1 4 1 1 1 4 4

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 3, Distancia Manhattan
python automain.py 1 4 1 1 3 1 1
python automain.py 1 4 1 1 3 1 2
python automain.py 1 4 1 1 3 1 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 3, Distancia Euclidea
python automain.py 1 4 1 1 3 2 1
python automain.py 1 4 1 1 3 2 2
python automain.py 1 4 1 1 3 2 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 3, Distancia Chebychev
python automain.py 1 4 1 1 3 3 1
python automain.py 1 4 1 1 3 3 2
python automain.py 1 4 1 1 3 3 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 1 4 1 1 3 4 4

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 7, Distancia Manhattan
python automain.py 1 4 1 1 7 1 1
python automain.py 1 4 1 1 7 1 2
python automain.py 1 4 1 1 7 1 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 7, Distancia Euclidea
python automain.py 1 4 1 1 7 2 1
python automain.py 1 4 1 1 7 2 2
python automain.py 1 4 1 1 7 2 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 7, Distancia Chebychev
python automain.py 1 4 1 1 7 3 1
python automain.py 1 4 1 1 7 3 2
python automain.py 1 4 1 1 7 3 3

# Fijo: Iris, KNN, Normal, Deshacer Onehot, 7, Distancia Mahalanobis
#python automain.py 1 4 1 1 7 4 4

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 1, Distancia Manhattan
python automain.py 1 4 2 1 1 1 1
python automain.py 1 4 2 1 1 1 2
python automain.py 1 4 2 1 1 1 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 1, Distancia Euclidea
python automain.py 1 4 2 1 1 2 1
python automain.py 1 4 2 1 1 2 2
python automain.py 1 4 2 1 1 2 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 1, Distancia Chebychev
python automain.py 1 4 2 1 1 3 1
python automain.py 1 4 2 1 1 3 2
python automain.py 1 4 2 1 1 3 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 1 4 2 1 1 4 4

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 3, Distancia Manhattan
python automain.py 1 4 2 1 3 1 1
python automain.py 1 4 2 1 3 1 2
python automain.py 1 4 2 1 3 1 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 3, Distancia Euclidea
python automain.py 1 4 2 1 3 2 1
python automain.py 1 4 2 1 3 2 2
python automain.py 1 4 2 1 3 2 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 3, Distancia Chebychev
python automain.py 1 4 2 1 3 3 1
python automain.py 1 4 2 1 3 3 2
python automain.py 1 4 2 1 3 3 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 1 4 2 1 3 4 4

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 7, Distancia Manhattan
python automain.py 1 4 2 1 7 1 1
python automain.py 1 4 2 1 7 1 2
python automain.py 1 4 2 1 7 1 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 7, Distancia Euclidea
python automain.py 1 4 2 1 7 2 1
python automain.py 1 4 2 1 7 2 2
python automain.py 1 4 2 1 7 2 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 7, Distancia Chebychev
python automain.py 1 4 2 1 7 3 1
python automain.py 1 4 2 1 7 3 2
python automain.py 1 4 2 1 7 3 3

# Fijo: Iris, KNN, Cross, Deshacer Onehot, 7, Distancia Mahalanobis
#python automain.py 1 4 2 1 7 4 4

# CoverType - NB
# -----------------------------------------------------------------------------------

# Fijo: CoverType, NB, Normal, Deshacer Onehot, Normal Dist
python automain.py 2 3 1 1 1 0
python automain.py 2 3 1 1 1 0.01
python automain.py 2 3 1 1 1 0.5
python automain.py 2 3 1 1 1 1
python automain.py 2 3 1 1 1 100

# Fijo: CoverType, NB, Normal, Deshacer Onehot, Variables
python automain.py 2 3 1 1 2 0
python automain.py 2 3 1 1 2 0.01
python automain.py 2 3 1 1 2 0.5
python automain.py 2 3 1 1 2 1
python automain.py 2 3 1 1 2 100

# Fijo: CoverType, NB, Normal, Conservar Onehot, Normal Dist
python automain.py 2 3 1 2 1 0
python automain.py 2 3 1 2 1 0.01
python automain.py 2 3 1 2 1 0.5
python automain.py 2 3 1 2 1 1
python automain.py 2 3 1 2 1 100

# Fijo: CoverType, NB, Normal, Conservar Onehot, Variables
python automain.py 2 3 1 2 2 0
python automain.py 2 3 1 2 2 0.01
python automain.py 2 3 1 2 2 0.5
python automain.py 2 3 1 2 2 1
python automain.py 2 3 1 2 2 100

# Fijo: CoverType, NB, Cross, Deshacer Onehot, Normal Dist
python automain.py 2 3 2 1 1 0
python automain.py 2 3 2 1 1 0.01
python automain.py 2 3 2 1 1 0.5
python automain.py 2 3 2 1 1 1
python automain.py 2 3 2 1 1 100

# Fijo: CoverType, NB, Cross, Deshacer Onehot, Variables
python automain.py 2 3 2 1 2 0
python automain.py 2 3 2 1 2 0.01
python automain.py 2 3 2 1 2 0.5
python automain.py 2 3 2 1 2 1
python automain.py 2 3 2 1 2 100

# Fijo: CoverType, NB, Cross, Conservar Onehot, Normal Dist
python automain.py 2 3 2 2 1 0
python automain.py 2 3 2 2 1 0.01
python automain.py 2 3 2 2 1 0.5
python automain.py 2 3 2 2 1 1
python automain.py 2 3 2 2 1 100

# Fijo: CoverType, NB, Cross, Conservar Onehot, Variables
python automain.py 2 3 2 2 2 0
python automain.py 2 3 2 2 2 0.01
python automain.py 2 3 2 2 2 0.5
python automain.py 2 3 2 2 2 1
python automain.py 2 3 2 2 2 100

# COVERTYPE - KNN
# -----------------------------------------------------------------------------------

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Manhattan
python automain.py 2 4 1 1 1 1 1
python automain.py 2 4 1 1 1 1 2
python automain.py 2 4 1 1 1 1 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Euclidea
python automain.py 2 4 1 1 1 2 1
python automain.py 2 4 1 1 1 2 2
python automain.py 2 4 1 1 1 2 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Chebychev
python automain.py 2 4 1 1 1 3 1
python automain.py 2 4 1 1 1 3 2
python automain.py 2 4 1 1 1 3 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 1 1 1 4 4

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 3, Distancia Manhattan
python automain.py 2 4 1 1 3 1 1
python automain.py 2 4 1 1 3 1 2
python automain.py 2 4 1 1 3 1 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 3, Distancia Euclidea
python automain.py 2 4 1 1 3 2 1
python automain.py 2 4 1 1 3 2 2
python automain.py 2 4 1 1 3 2 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 3, Distancia Chebychev
python automain.py 2 4 1 1 3 3 1
python automain.py 2 4 1 1 3 3 2
python automain.py 2 4 1 1 3 3 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 1 1 3 4 4

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Manhattan
python automain.py 2 4 1 1 7 1 1
python automain.py 2 4 1 1 7 1 2
python automain.py 2 4 1 1 7 1 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Euclidea
python automain.py 2 4 1 1 7 2 1
python automain.py 2 4 1 1 7 2 2
python automain.py 2 4 1 1 7 2 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Chebychev
python automain.py 2 4 1 1 7 3 1
python automain.py 2 4 1 1 7 3 2
python automain.py 2 4 1 1 7 3 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Mahalanobis
#python automain.py 2 4 1 1 7 4 4

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Manhattan
python automain.py 2 4 2 1 1 1 1
python automain.py 2 4 2 1 1 1 2
python automain.py 2 4 2 1 1 1 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Euclidea
python automain.py 2 4 2 1 1 2 1
python automain.py 2 4 2 1 1 2 2
python automain.py 2 4 2 1 1 2 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Chebychev
python automain.py 2 4 2 1 1 3 1
python automain.py 2 4 2 1 1 3 2
python automain.py 2 4 2 1 1 3 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 2 1 1 4 4

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 3, Distancia Manhattan
python automain.py 2 4 2 1 3 1 1
python automain.py 2 4 2 1 3 1 2
python automain.py 2 4 2 1 3 1 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 3, Distancia Euclidea
python automain.py 2 4 2 1 3 2 1
python automain.py 2 4 2 1 3 2 2
python automain.py 2 4 2 1 3 2 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 3, Distancia Chebychev
python automain.py 2 4 2 1 3 3 1
python automain.py 2 4 2 1 3 3 2
python automain.py 2 4 2 1 3 3 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 2 1 3 4 4

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Manhattan
python automain.py 2 4 2 1 7 1 1
python automain.py 2 4 2 1 7 1 2
python automain.py 2 4 2 1 7 1 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Euclidea
python automain.py 2 4 2 1 7 2 1
python automain.py 2 4 2 1 7 2 2
python automain.py 2 4 2 1 7 2 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Chebychev
python automain.py 2 4 2 1 7 3 1
python automain.py 2 4 2 1 7 3 2
python automain.py 2 4 2 1 7 3 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Mahalanobis
#python automain.py 2 4 2 1 7 4 4

# Fijo: CoverType, KNN, Normal, Conservar Onehot, 1, Distancia Manhattan
python automain.py 2 4 1 2 1 1 1
python automain.py 2 4 1 2 1 1 2
python automain.py 2 4 1 2 1 1 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Euclidea
python automain.py 2 4 1 2 1 2 1
python automain.py 2 4 1 2 1 2 2
python automain.py 2 4 1 2 1 2 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Chebychev
python automain.py 2 4 1 2 1 3 1
python automain.py 2 4 1 2 1 3 2
python automain.py 2 4 1 2 1 3 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 1 2 1 4 4

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 3, Distancia Manhattan
python automain.py 2 4 1 2 3 1 1
python automain.py 2 4 1 2 3 1 2
python automain.py 2 4 1 2 3 1 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 3, Distancia Euclidea
python automain.py 2 4 1 2 3 2 1
python automain.py 2 4 1 2 3 2 2
python automain.py 2 4 1 2 3 2 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 3, Distancia Chebychev
python automain.py 2 4 1 2 3 3 1
python automain.py 2 4 1 2 3 3 2
python automain.py 2 4 1 2 3 3 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 1 2 3 4 4

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Manhattan
python automain.py 2 4 1 2 7 1 1
python automain.py 2 4 1 2 7 1 2
python automain.py 2 4 1 2 7 1 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Euclidea
python automain.py 2 4 1 2 7 2 1
python automain.py 2 4 1 2 7 2 2
python automain.py 2 4 1 2 7 2 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Chebychev
python automain.py 2 4 1 2 7 3 1
python automain.py 2 4 1 2 7 3 2
python automain.py 2 4 1 2 7 3 3

# Fijo: CoverType, KNN, Normal, Deshacer Onehot, 7, Distancia Mahalanobis
#python automain.py 2 4 1 2 7 4 4

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Manhattan
python automain.py 2 4 2 2 1 1 1
python automain.py 2 4 2 2 1 1 2
python automain.py 2 4 2 2 1 1 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Euclidea
python automain.py 2 4 2 2 1 2 1
python automain.py 2 4 2 2 1 2 2
python automain.py 2 4 2 2 1 2 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Chebychev
python automain.py 2 4 2 2 1 3 1
python automain.py 2 4 2 2 1 3 2
python automain.py 2 4 2 2 1 3 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 2 2 1 4 4

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 3, Distancia Manhattan
python automain.py 2 4 2 2 3 1 1
python automain.py 2 4 2 2 3 1 2
python automain.py 2 4 2 2 3 1 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 3, Distancia Euclidea
python automain.py 2 4 2 2 3 2 1
python automain.py 2 4 2 2 3 2 2
python automain.py 2 4 2 2 3 2 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 3, Distancia Chebychev
python automain.py 2 4 2 2 3 3 1
python automain.py 2 4 2 2 3 3 2
python automain.py 2 4 2 2 3 3 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 1, Distancia Mahalanobis
#python automain.py 2 4 2 2 3 4 4

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Manhattan
python automain.py 2 4 2 2 7 1 1
python automain.py 2 4 2 2 7 1 2
python automain.py 2 4 2 2 7 1 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Euclidea
python automain.py 2 4 2 2 7 2 1
python automain.py 2 4 2 2 7 2 2
python automain.py 2 4 2 2 7 2 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Chebychev
python automain.py 2 4 2 2 7 3 1
python automain.py 2 4 2 2 7 3 2
python automain.py 2 4 2 2 7 3 3

# Fijo: CoverType, KNN, Cross, Deshacer Onehot, 7, Distancia Mahalanobis
#python automain.py 2 4 2 2 7 4 4
