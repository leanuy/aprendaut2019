from copy import deepcopy
import numpy as np
from numpy.linalg import svd


def pca(matrix, k):
    targets = []
    data = deepcopy(matrix)

    mean = np.mean(data, axis=0)
    datac = data - mean

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

