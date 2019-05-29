### DEPENDENCIAS
### ------------------

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.decomposition import PCA

import processing.parser as parser
import processing.reader as reader
import pandas as pd

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, datasetC, datasetP, candidates, parties, options):

        # Generar modelo de regresión logística con configuración paramétrica para candidatos
        self.model_candidates = LogisticRegression(multi_class='ovr', solver=options['solver'].value, penalty=options['penalty'].value, max_iter=options['max_iter'], C=options['regulation_strength'])
        
        # Generar modelo de regresión logística con configuración paramétrica para partidos
        self.model_parties = LogisticRegression(multi_class='ovr', solver=options['solver'].value, penalty=options['penalty'].value, max_iter=options['max_iter'], C=options['regulation_strength']) 

        # Almacenar informacion de entrenamiento y configuraciones
        self.all_datasetC = datasetC
        self.all_datasetP = datasetP
        self.all_candidates = candidates
        self.all_parties = parties
        self.options = options

        # Reducir dimensionalidad con PCA (si es necesario)
        self.transform()

        # Separar 80% dataset y 20% testset
        self.datasetC, self.testsetC, self.candidates, self.candidates_results = train_test_split(self.all_datasetC, self.all_candidates, test_size=0.2)
        self.datasetP, self.testsetP, self.parties, self.parties_results = train_test_split(self.all_datasetP, self.all_parties, test_size=0.2)

        self.transformed = False
        self.evaluation = None
        self.explained_variance_ratioC = None
        self.explained_variance_ratioP = None

    ### METODOS PRINCIPALES
    ### -------------------

    # Entrenar modelo utilizando 'dataset', 'results' y la configuración de 'options'
    # Reducir dimensionalidad de 'dataset' con PCA si es necesario
    # Separar 'dataset' con 80/20 para entrenamiento y evaluación
    def train(self):

        # Entrenar cada clasificador con 80% dataset
        self.model_candidates.fit(self.datasetC, self.candidates)
        self.model_parties.fit(self.datasetP, self.parties)

    # Clasificar 'examples' utilizando el modelo entrenado
    def classify(self, examples_candidates, examples_parties):
        res = self.model_candidates.predict(examples_candidates), self.model_parties.predict(examples_parties)
        if self.options['candidate_to_party']:
            res = np.array(map(parser.getCandidateParty, res))
        return res

    # Evaluar el modelo entrenado
    def evaluate(self, k = 0):
    
        if not self.transformed:
            self.transform()

        if k > 0:
            # Evaluar cruzadamente el dataset completo
            results_candidates = cross_val_predict(self.model_candidates, self.datasetC, self.candidates, cv=k)
            results_parties = cross_val_predict(self.model_parties, self.datasetP, self.parties, cv=k)

            # Evaluar distintas métricas de la clasificación de 'test' segun candidatos
            self.evaluation = {'k': k}
            self.evaluation['cv_accuracy_candidates'] = accuracy_score(self.candidates, results_candidates)
            self.evaluation['cv_confusion_matrix_candidates'] = confusion_matrix(self.candidates, results_candidates)
            self.evaluation['cv_report_candidates'] = classification_report(self.candidates, results_candidates)
            self.evaluation['cv_report_candidates_dict'] = classification_report(self.candidates, results_candidates, output_dict=True)

            # Evaluar distintas métricas de la clasificación de 'test' segun partidos
            self.evaluation['cv_accuracy_parties'] = accuracy_score(self.parties, results_parties)
            self.evaluation['cv_confusion_matrix_parties'] = confusion_matrix(self.parties, results_parties)
            self.evaluation['cv_report_parties'] = classification_report(self.parties, results_parties)
            self.evaluation['cv_report_parties_dict'] = classification_report(self.parties, results_parties, output_dict=True)
            
            self.evaluation['explained_variance_ratioC'] = self.explained_variance_ratioC
            self.evaluation['explained_variance_ratioP'] = self.explained_variance_ratioP

        else:

            if not self.options['candidate_to_party']:
                # Clasificar el conjunto 'test'
                testset_candidates_res = self.model_candidates.predict(self.testsetC)
                testset_parties_res = self.model_parties.predict(self.testsetP)
                
                # Evaluar distintas métricas de la clasificación de 'test'
                self.evaluation = {'k': k}
                self.evaluation['accuracy_candidates'] = accuracy_score(self.candidates_results, testset_candidates_res)
                self.evaluation['confusion_matrix_candidates'] = confusion_matrix(self.candidates_results, testset_candidates_res)
                self.evaluation['report_candidates'] = classification_report(self.candidates_results, testset_candidates_res)
                self.evaluation['report_candidates_dict'] = classification_report(self.candidates_results, testset_candidates_res, output_dict=True)

                self.evaluation['accuracy_parties'] = accuracy_score(self.parties_results, testset_parties_res)
                self.evaluation['confusion_matrix_parties'] = confusion_matrix(self.parties_results, testset_parties_res)
                self.evaluation['report_parties'] = classification_report(self.parties_results, testset_parties_res)
                self.evaluation['report_parties_dict'] = classification_report(self.parties_results, testset_parties_res, output_dict=True)
                
                self.evaluation['explained_variance_ratioC'] = self.explained_variance_ratioC
                self.evaluation['explained_variance_ratioP'] = self.explained_variance_ratioP

            else:
                # Clasificar el conjunto 'test'
                testset_candidates_res = self.model_candidates.predict(self.testsetC)
                testset_parties_res = self.model_parties.predict(self.testsetP)
                
                # Convertir el teset_candidates_res a mapeo de partidos
                testset_candidates_res = self.candidates_to_parties(testset_candidates_res)

                # Convertir el self.candidates_results a su partido.
                true_parties_results_from_candidates = self.candidates_to_parties(self.candidates_results)

                # Evaluar distintas métricas de la clasificación de 'test'
                self.evaluation = {'k': k}
                self.evaluation['accuracy_candidates'] = accuracy_score(true_parties_results_from_candidates, testset_candidates_res)
                self.evaluation['confusion_matrix_candidates'] = confusion_matrix(true_parties_results_from_candidates, testset_candidates_res)
                self.evaluation['report_candidates'] = classification_report(true_parties_results_from_candidates, testset_candidates_res)
                self.evaluation['report_candidates_dict'] = classification_report(true_parties_results_from_candidates, testset_candidates_res, output_dict=True)

                self.evaluation['accuracy_parties'] = accuracy_score(self.parties_results, testset_parties_res)
                self.evaluation['confusion_matrix_parties'] = confusion_matrix(self.parties_results, testset_parties_res)
                self.evaluation['report_parties'] = classification_report(self.parties_results, testset_parties_res)
                self.evaluation['report_parties_dict'] = classification_report(self.parties_results, testset_parties_res, output_dict=True)
                
                self.evaluation['explained_variance_ratioC'] = self.explained_variance_ratioC
                self.evaluation['explained_variance_ratioP'] = self.explained_variance_ratioP

        return self.evaluation

    ### METODOS AUXILIARES
    ### -------------------

    def transform(self):
        # Si pca_dimension mayor a 0, se aplica la reducción
        if self.options['pca_dimension'] > 0:
            pcaC = PCA(n_components=self.options['pca_dimension'])
            self.all_datasetC = pcaC.fit_transform(self.all_datasetC)
            self.explained_variance_ratioC = pcaC.explained_variance_ratio_

            pcaP = PCA(n_components=self.options['pca_dimension'])
            self.all_datasetP = pcaP.fit_transform(self.all_datasetP)
            self.explained_variance_ratioP = pcaP.explained_variance_ratio_
        
            self.transformed = True
        
    def candidates_to_parties(self, candidates):
        partyJSON = reader.readParties(self.options)
        parties = []
        for i in range(0, len(partyJSON)):
            partyCandidates = []
            for candidate in partyJSON[i]['candidates']:
                partyCandidates.append(candidate['id'])
            parties.append((i, partyCandidates))

        res = []
        for c in candidates:
            for p in parties:
                if c in p[1]:
                    res.append(c)
                    break

        return np.array(res)



