from copy import deepcopy
import numpy as np
from numpy.linalg import svd, eig
from utils.const import PCAOps

def pca(matrix, k, options):
    # Copia del dataset original
    # data = deepcopy(matrix)
    data = matrix
    # Sustraer la media para cada atributo
    mean = np.mean(data, axis=0)
    datac = data - mean


    if options['pca_type'] == PCAOps.SVD:
        # Calculo SVD
        U, S, V = svd(datac, full_matrices=False)

        # diagonalizar los valores propios, armar la matriz diagonal y extraer k x k
        sigma_matrix = np.diag(S)
        reduced_sigma = []

        for i in range(k):
            reduced_sigma.append(sigma_matrix[i][:k])

        # primeras k columnas de U
        reduced_U = []
        for u in U:
            reduced_U.append(u[:k])

        reduced_V = []
        for i in range(k):
            reduced_V.append(V[i][:k])

        T_k = np.array(reduced_U) @ np.array(reduced_sigma) @ np.array(reduced_V)
        return T_k
    
    elif options['pca_type'] == PCAOps.COVARIANZA:
        # Calculamos la matriz de covarianza de los datos
        # puto memory error aqui...
        matrix_cov = np.cov(datac)
        
        # Obtenemos los valores y vectores propios de la matriz de covarianza
        val_prop_cov, vect_prop_cov = np.linalg.eig(matrix_cov)

        eig_pairs = [(np.abs(val_prop_cov[i]), vect_prop_cov[:,i]) for i in range(len(val_prop_cov))]

        eig_pairs.sort()
        eig_pairs.reverse()

        print(eig_pairs)
        exit()
