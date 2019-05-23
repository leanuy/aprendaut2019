### DEPENDENCIAS
### ------------------

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_predict
from sklearn.decomposition import PCA

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, dataset, candidates, parties, options):

        # Generar modelo de regresión logística con configuración paramétrica para candidatos
        self.model_candidates = LogisticRegression(multi_class='ovr', solver=options['solver'].value, penalty=options['penalty'].value, max_iter=options['max_iter'], C=options['regulation_strength'])
        
        # Generar modelo de regresión logística con configuración paramétrica para partidos
        self.model_parties = LogisticRegression(multi_class='ovr', solver=options['solver'].value, penalty=options['penalty'].value, max_iter=options['max_iter'], C=options['regulation_strength']) 

        # Almacenar informacion de entrenamiento y configuraciones
        self.all_dataset = dataset
        self.all_candidates = candidates
        self.all_parties = parties
        self.options = options
        self.explained_variance_ratio = None

    ### METODOS PRINCIPALES
    ### -------------------

    # Entrenar modelo utilizando 'dataset', 'results' y la configuración de 'options'
    # Reducir dimensionalidad de 'dataset' con PCA si es necesario
    # Separar 'dataset' con 80/20 para entrenamiento y evaluación
    def train(self):

        # Reducir dimensionalidad con PCA (si es necesario)
        self.transform()

        # Separar 80% dataset y 20% testset
        self.dataset_candidates, self.testset_candidates, self.candidates, self.testset_candidates_results = train_test_split(self.all_dataset, self.all_candidates, test_size=0.2)

        self.dataset_parties, self.testset_parties, self.parties, self.testset_parties_results = train_test_split(self.all_dataset, self.all_parties, test_size=0.2)

        # Entrenar cada clasificador con 80% dataset
        self.model_candidates.fit(self.dataset_candidates, self.candidates)
        self.model_parties.fit(self.dataset_parties, self.parties)

    # Clasificar 'examples' utilizando el modelo entrenado
    def classify(self, examples):
        return self.model_candidates.predict(examples), self.model_parties.predict(examples)

    # Evaluar el modelo entrenado
    def evaluate(self, k = 0):

        if k > 0:
            # Evaluar cruzadamente el dataset completo
            results_candidates = cross_val_predict(self.model_candidates, self.all_dataset, self.all_candidates, cv=k)

            results_parties = cross_val_predict(self.model_parties, self.all_dataset, self.all_parties, cv=k)

            # Evaluar distintas métricas de la clasificación de 'test' segun candidatos
            self.evaluation = {}
            self.evaluation['cv_accuracy_candidates'] = accuracy_score(self.all_candidates, results_candidates)
            self.evaluation['cv_confusion_matrix_candidates'] = confusion_matrix(self.all_candidates, results_candidates)
            self.evaluation['cv_report_candidates'] = classification_report(self.all_candidates, results_candidates)

            # Evaluar distintas métricas de la clasificación de 'test' segun partidos
            self.evaluation['cv_accuracy_parties'] = accuracy_score(self.all_parties, results_parties)
            self.evaluation['cv_confusion_matrix_parties'] = confusion_matrix(self.all_parties, results_parties)
            self.evaluation['cv_report_parties'] = classification_report(self.all_parties, results_parties)
            
            self.evaluation['explained_variance_ratio'] = self.explained_variance_ratio

        else:
            # Clasificar el conjunto 'test'
            testset_candidates_res = self.model_candidates.predict(self.testset_candidates)

            testset_parties_res = self.model_parties.predict(self.testset_parties)
            
            # Evaluar distintas métricas de la clasificación de 'test'
            self.evaluation = {}
            self.evaluation['accuracy_candidates'] = accuracy_score(self.testset_candidates_results, testset_candidates_res)
            self.evaluation['confusion_matrix_candidates'] = confusion_matrix(self.testset_candidates_results, testset_candidates_res)
            self.evaluation['report_candidates'] = classification_report(self.testset_candidates_results, testset_candidates_res)

            self.evaluation['accuracy_parties'] = accuracy_score(self.testset_parties_results, testset_parties_res)
            self.evaluation['confusion_matrix_parties'] = confusion_matrix(self.testset_parties_results, testset_parties_res)
            self.evaluation['report_parties'] = classification_report(self.testset_parties_results, testset_parties_res)
            
            self.evaluation['explained_variance_ratio'] = self.explained_variance_ratio

        return self.evaluation

    ### METODOS AUXILIARES
    ### -------------------

    def transform(self):
        # Si pca_dimension mayor a 0, se aplica la reducción
        if self.options['pca_dimension'] > 0:
            pca = PCA(n_components=self.options['pca_dimension'])
            self.all_dataset = pca.fit_transform(self.all_dataset)
            self.explained_variance_ratio = pca.explained_variance_ratio_

