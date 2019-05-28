### DEPENDENCIAS
### ------------------

import operator

from model.model import Model
from utils.const import SolverOps, PenaltyOps, MaxIterOps, RegulationStrengthOps
from utils.gui import printClassifierTraining, printClassifierEvaluation

### METODOS PRINCIPALES
### -------------------

def getBestModel(datasetC, datasetP, candidates, parties, k, check_pca = False):

    classifiers_candidates = []
    classifiers_parties = []

    if not check_pca:

        for solver in SolverOps:

            PenaltyOptions = []
            if solver == SolverOps.LBFGS or solver == SolverOps.SAG or solver == SolverOps.NEWTON_CG:
                PenaltyOptions = [PenaltyOps.L2]     
            elif solver == SolverOps.LIBLINEAR or solver == SolverOps.SAGA:
                PenaltyOptions = [PenaltyOps.L2, PenaltyOps.L1]

            for penalty in PenaltyOptions:
                for max_iter in MaxIterOps:
                    for regulation_strength in RegulationStrengthOps:
                        
                        options = {
                            'pca_dimension': 0,                
                            'solver': solver,
                            'penalty': penalty,
                            'max_iter': max_iter,
                            'regulation_strength': regulation_strength
                        }

                        printClassifierTraining(len(classifiers_candidates) + 1, options)

                        m = Model(datasetC.values, datasetP.values, candidates.values, parties.values, options)
                        if k == 0:
                            m.train()
                        evaluation = m.evaluate(k)

                        if k != 0:
                            printClassifierEvaluation(evaluation['cv_accuracy_candidates'], evaluation['cv_accuracy_parties'])

                            classifiers_candidates.append((evaluation['cv_accuracy_candidates'], m))
                            classifiers_parties.append((evaluation['cv_accuracy_parties'], m))
                        else:
                            printClassifierEvaluation(evaluation['accuracy_candidates'], evaluation['accuracy_parties'])

                            classifiers_candidates.append((evaluation['accuracy_candidates'], m))
                            classifiers_parties.append((evaluation['accuracy_parties'], m))
    else:

        for i in range(1, 26):

            options = {
                'pca_dimension': i,                
                'solver': SolverOps.LIBLINEAR,
                'penalty': PenaltyOps.L2,
                'max_iter': 1000,
                'regulation_strength': 100.0
            }

            printClassifierTraining(len(classifiers_candidates) + 1, options)

            m = Model(datasetC.values, datasetP.values, candidates.values, parties.values, options)
            if k == 0:
                m.train()
            evaluation = m.evaluate(k)
            if k != 0:
                printClassifierEvaluation(evaluation['cv_accuracy_candidates'], evaluation['cv_accuracy_parties'])

                classifiers_candidates.append((evaluation['cv_accuracy_candidates'], m))
                classifiers_parties.append((evaluation['cv_accuracy_parties'], m))
            else:
                printClassifierEvaluation(evaluation['accuracy_candidates'], evaluation['accuracy_parties'])

                classifiers_candidates.append((evaluation['accuracy_candidates'], m))
                classifiers_parties.append((evaluation['accuracy_parties'], m))

    return (classifiers_candidates, classifiers_parties)
    