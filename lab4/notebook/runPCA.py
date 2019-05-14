import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import utils.const as const
from model import pca
import processing.reader as reader

pcaRun()

### MÉTODOS
###########

def pcaRun():
    # Leer dataset de respuestas a encuesta
    candidates, dataset = reader.readDataset(const.DATA_ENCUESTAS)

    options = {
        'pca_election': const.PCAOps.COVARIANZA,
        'pca_analysis': const.PCAnalysis.NONE,
        'pca_intermediates': const.PCAIntermediates.NONE,
        'candidate_division': const.CandidateDivision.PARTIES
    }

    # Aplicar PCA para reducir a 2 dimensiones
    reducedDataset, extras = pca.reduce_pca(dataset.values, 2, options)