### DEPENDENCIAS
### ------------------

import sys
import os
import time
import operator

from model.model import Model
import processing.reader as reader
import evaluation.evaluator as evaluator
import plotting.corpusPlotting as corpusPlotting
import plotting.pcaPlotting as pcaPlotting
import plotting.evalPlotting as evalPlotting
import utils.gui as gui
from utils.const import DATA_ENCUESTAS, DATA_CANDIDATOS, MenuOps, PlotOps

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    classifiers = []
    checked_pca = False

    while op == MenuOps.TRAIN or op == MenuOps.EVALUATE or op == MenuOps.PLOT or op == MenuOps.SEARCH:

        gui.printMenu(classifiers)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            candidate_to_party = 0
            pca_dimension = gui.printPCADimension()
            solver_election = gui.printSolverOptions()
            penalty_election = gui.printPenaltyOptions(solver_election)            
            max_iter = gui.printIterations()
            regulation_strength = gui.printRegulationStrength()
            candidate_to_party = gui.printCandidateToParty()

            # Leer dataset de respuestas a encuesta
            datasetC, candidates = reader.readDatasetCandidatosMasMil(DATA_ENCUESTAS)
            datasetP, parties = reader.readDatasetPartiesMasMil(DATA_ENCUESTAS)
            options = {
                'candidate_to_party': candidate_to_party,
                'pca_dimension': pca_dimension,                
                'solver': solver_election,
                'penalty': penalty_election,
                'max_iter': max_iter,
                'regulation_strength': regulation_strength
            }

            m = Model(datasetC.values, datasetP.values, candidates.values, parties.values, options)

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            m.train()

            print("-> FIN DEL ENTRENAMIENTO")
            print()

            classifiers.append(m)

        elif op == MenuOps.EVALUATE:

            trainNew = True

            if len(classifiers) > 0:
                gui.printClear()
                gui.printClassifiers(classifiers)

                print("-> Elija un modelo por el índice: ")
                print("-> DEFAULT: 0 (Entrenar modelo nuevo)")

                try:
                    c = int( input() )
                except:
                    c = 0
                c -= 1

                if c >= 0 and c < len(classifiers):

                    m = classifiers[c]

                    k = gui.printCrossK()

                    evaluation = m.evaluate(k)
                    if k == 0:
                        m.train()
                    gui.printEvaluation(evaluation, k)

                    trainNew = False

            if trainNew:

                print()
                print("-> Parte 1 - Entrenamiento")

                pca_dimension = gui.printPCADimension()
                solver_election = gui.printSolverOptions()
                penalty_election = gui.printPenaltyOptions(solver_election)            
                max_iter = gui.printIterations()
                regulation_strength = gui.printRegulationStrength()
                candidate_to_party = gui.printCandidateToParty(),

                # Leer dataset de respuestas a encuesta
                datasetC, candidates = reader.readDatasetCandidatosMasMil(DATA_ENCUESTAS)
                datasetP, parties = reader.readDatasetPartiesMasMil(DATA_ENCUESTAS)
                options = {
                    'pca_dimension': pca_dimension,                
                    'solver': solver_election,
                    'penalty': penalty_election,
                    'max_iter': max_iter,
                    'regulation_strength': regulation_strength,
                    'candidate_to_party': candidate_to_party
                }

                m = Model(datasetC.values, datasetP.values, candidates.values, parties.values, options)
                
                print()
                print("-> COMIENZO DEL ENTRENAMIENTO")

                m.train()

                print("-> FIN DEL ENTRENAMIENTO")
                print()
                
                classifiers.append(m)

                print("-> Parte 2 - Evaluación")

                k = gui.printCrossK()
                
                evaluation = m.evaluate(k)
                gui.printEvaluation(evaluation, k)

        elif op == MenuOps.PLOT:

            plot_op = gui.printPlotOption()

            if plot_op == PlotOps.CORPUS:

                # Leer dataset de respuestas a encuesta separando entre candidatos con más y menos de 1000 votos
                datasetC = reader.readDatasetCandidatosMasMil(DATA_ENCUESTAS)
                datasetNC = reader.readDatasetCandidatosMenosMil(DATA_ENCUESTAS)

                datasetP = reader.readDatasetPartiesMasMil(DATA_ENCUESTAS)
                datasetNP = reader.readDatasetPartiesMenosMil(DATA_ENCUESTAS)

                candidatesJSON = reader.readCandidates()
                partiesJSON = reader.readParties()

                # Graficar distribución de votantes según candidato y partido
                corpusPlotting.plotCorpus(datasetC, datasetNC, datasetP, datasetNP, candidatesJSON, partiesJSON)

                # Graficar ratio de varianza para cada dimensión
                pcaPlotting.plotPCA(datasetC, 'Candidatos')
                pcaPlotting.plotPCA(datasetP, 'Partidos')

            elif plot_op == PlotOps.SINGLE:

                if len(classifiers) > 0:
                    gui.printClear()
                    gui.printClassifiers(classifiers)

                    print("-> Elija un modelo por el índice: ")

                    try:
                        c = int( input() )
                    except:
                        c = 1
                    c -= 1

                    if c >= 0 and c < len(classifiers):

                        m = classifiers[c]

                        evaluation = m.evaluation
                        if evaluation == None:
                            k = gui.printCrossK()
                            evaluation = m.evaluate(k)
                            
                        gui.printEvaluation(evaluation, evaluation['k'])
                        evalPlotting.plotSingleEvaluation(evaluation, k)

                    else:
                        print('-> El número ingresado no corresponde a ningún modelo')
                        print()
                else:
                    print('-> No hay modelos para evaluar')
                    print()

            elif plot_op == PlotOps.ALL:
            
                if len(classifiers) > 0:

                    if checked_pca:
                        candidates = [(c.options['pca_dimension'], c.evaluation['cv_accuracy_candidates']) for c in classifiers]
                        parties = [(c.options['pca_dimension'], c.evaluation['cv_accuracy_parties']) for c in classifiers]

                        candidates.sort(key=operator.itemgetter(0))
                        parties.sort(key=operator.itemgetter(0))

                        candidates = [a for d,a in candidates]
                        parties = [a for d,a in parties]

                    else:
                        candidates = [c.evaluation['cv_accuracy_candidates'] for c in classifiers]
                        parties = [c.evaluation['cv_accuracy_parties'] for c in classifiers]

                    evalPlotting.plotAllEvaluations(candidates, parties, checked_pca)
                
                else:
                    print('-> No hay modelos para evaluar')
                    print()

        elif op == MenuOps.SEARCH:

            check_pca = gui.printCheckPCA()
            k = gui.printCrossK()
            
            # Leer dataset de respuestas a encuesta
            datasetC, candidates = reader.readDatasetCandidatosMasMil(DATA_ENCUESTAS)
            datasetP, parties = reader.readDatasetPartiesMasMil(DATA_ENCUESTAS)

            # Evaluar todas las configuraciones paramétricas posibles y ordenarlas según accuracy
            candidate_classifiers, party_classifiers = evaluator.getBestModel(datasetC, datasetP, candidates, parties, k, check_pca)

            # Mostrar el mejor clasificador según candidatos y según partidos
            gui.printBestClassifiers(candidate_classifiers, party_classifiers)

            # Guardar todos los clasificadores localmente
            classifiers = [m for a,m in candidate_classifiers]

            checked_pca = check_pca
            
        input("-> Oprima enter para volver al menú")
