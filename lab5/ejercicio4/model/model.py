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

    def __init__(self, dataset, results, options):

        # Generar modelo de regresión logística con configuración paramétrica
        self.model = LogisticRegression(multi_class='ovr', solver=options['solver'].value, penalty=options['penalty'].value, max_iter=options['max_iter'], C=options['regulation_strength'])
        
        # Almacenar informacion de entrenamiento y configuraciones
        self.all_dataset = dataset
        self.all_results = results
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
        self.dataset, self.testset, self.results, self.testset_results = train_test_split(self.all_dataset, self.all_results, test_size=0.2)

        # Entrenar clasificador con 80% dataset
        self.model.fit(self.dataset, self.results)
        return self.model

    # Clasificar 'examples' utilizando el modelo entrenado
    def classify(self, examples):
        return self.model.predict(examples)

    # Evaluar el modelo entrenado
    def evaluate(self, k = 0):

        if k > 0:
            # Evaluar cruzadamente el dataset completo
            results = cross_val_predict(self.model, self.all_dataset, self.all_results, cv=k)

            # Evaluar distintas métricas de la clasificación de 'test'
            self.evaluation = {}
            self.evaluation['cv_accuracy'] = accuracy_score(self.all_results, results)
            self.evaluation['cv_confusion_matrix'] = confusion_matrix(self.all_results, results)
            self.evaluation['cv_report'] = classification_report(self.all_results, results)
            self.evaluation['explained_variance_ratio'] = self.explained_variance_ratio

        else:
            # Clasificar el conjunto 'test'
            testset_results = self.model.predict(self.testset)
            
            # Evaluar distintas métricas de la clasificación de 'test'
            self.evaluation = {}
            self.evaluation['accuracy'] = accuracy_score(self.testset_results, testset_results)
            self.evaluation['confusion_matrix'] = confusion_matrix(self.testset_results, testset_results)
            self.evaluation['report'] = classification_report(self.testset_results, testset_results)
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




