from copy import deepcopy
import numpy as np
from numpy.linalg import svd, eig
from utils.const import PCAOps

def reduce_pca(matrix, k, options):

    # Copia del dataset original
    data = matrix.transpose()

    # Sustraer la media para cada atributo
    mean = data.mean(axis=1, keepdims=True)
    std = data.std(axis=1, keepdims=True)
    var = data.var(axis=1, keepdims=True)

    datac = np.subtract(data, mean)

    if options['pca_election'] == PCAOps.SVD:

        # Calculo SVD
        U, S, V = svd(datac.T, full_matrices=False)

        sigma_matrix = np.diag(S)
        reduced_sigma = []

        for i in range(k):
            reduced_sigma.append(sigma_matrix[i][:k])

        # primeras k columnas de U
        reduced_U = []
        for u in U:
            reduced_U.append(u[:k])

        T_k = np.array(reduced_U) @ np.array(reduced_sigma)
        return T_k, None
    
    elif options['pca_election'] == PCAOps.COVARIANZA:

        # Calculamos la matriz de covarianza de los datos
        cov_matrix = np.cov(datac)
        
        # Obtenemos los valores y vectores propios de la matriz de covarianza
        val_prop_cov, vect_prop_cov = np.linalg.eig(cov_matrix)

        eig_pairs = [(np.abs(val_prop_cov[i]), vect_prop_cov[:,i]) for i in range(len(val_prop_cov))]
        eig_pairs.sort()
        eig_pairs.reverse()

        matrix_w = np.hstack((eig_pairs[0][1].reshape(26,1), eig_pairs[1][1].reshape(26,1)))
        
        explained_variance_ratio = [np.abs(i)/np.sum(val_prop_cov) for i in val_prop_cov]

        transformed = np.dot(datac.T, matrix_w)
        extras = {
          'cov_matrix': cov_matrix,
          'eigen_values': val_prop_cov,
          'explained_variance_ratio': explained_variance_ratio,
        }
        return (transformed, extras)
      
