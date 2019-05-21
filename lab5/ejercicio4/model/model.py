### DEPENDENCIAS
### ------------------

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, dataset, results, options):

        # Generar modelo de regresión logística con configuración paramétrica
        self.model = LogisticRegression(solver=options['solver'].value, penalty=options['penalty'].value, max_iter=options['max_iter'], C=options['regulation_strength'])
        
        # Almacenar informacion de entrenamiento y configuraciones
        self.dataset = dataset
        self.results = results
        self.options = options

    ### METODOS PRINCIPALES
    ### -------------------

    def train(self):

        # Reducir dimensionalidad con PCA (si es necesario)
        self.transform()

        # Separar 80% dataset y 20% testset
        self.dataset, self.test, self.results, self.test_results = train_test_split(self.dataset, self.results, test_size=0.2)

        print(self.dataset.shape)
        print(self.test.shape)
        print(self.results.shape)
        print(self.test_results.shape)
        
        # Entrenar clasificador con 80% dataset
        self.model.fit(self.dataset, self.results)
        return self.model

    def classify(self, examples):
        return self.model.predict(examples)

    def evaluate(self):
        return 0

    ### METODOS AUXILIARES
    ### -------------------

    def transform(self):
        return 0


