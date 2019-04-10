# Dependencies
# --------------------------------------------------------------------------------

from enum import Enum
from model_id3_tree import id3_train, id3_classify
from model_naive_bayes import nb_train, nb_classify
from model_knn import knn_train, knn_classify
from preprocessor import *

# Enum class
# --------------------------------------------------------------------------------

class ModelType(Enum):
    DECISION_TREE = 1
    NAIVE_BAYES = 2
    KNN = 3

# Main class
# --------------------------------------------------------------------------------

class Model:

    def __init__(self, model):
        self.model = model
        self.ds = None
        self.attributes = None
        self.classifier = None

    # Main methods
    # ----------------------------------------------------------------------------

    def train(self, dataset, continuousOption = 0, missingOption = 0,  normOption = 3, k = 3, m = 0, isEvaluating = False):

        self.ds = dataset
        self.attributes = get_attributes_from_dataset(dataset)

        if self.model == ModelType.DECISION_TREE:
            self.classifier = self.train_tree(dataset, continuousOption, missingOption)

        elif self.model == ModelType.NAIVE_BAYES:
            self.classifier = self.train_nb(dataset, continuousOption, missingOption, m)

        elif self.model == ModelType.KNN:
            self.classifier = self.train_knn(dataset, k, missingOption, normOption, isEvaluating)

    def classify(self, example, continuousOption = 0, missingOption = 0, normOption = 3, k = 3, m = 0):

        if self.model == ModelType.DECISION_TREE:
            return self.classify_tree(example, continuousOption, missingOption)

        elif self.model == ModelType.NAIVE_BAYES:
            return self.classify_nb(example, continuousOption, missingOption, m)

        elif self.model == ModelType.KNN:
            return self.classify_knn(example, k, missingOption, normOption)

    def classify_set(self, example_set, continuousOption = 0, missingOption = 0, normOption = 3, k = 3, m = 0):
        results = []

        for example in example_set:

            if self.model == ModelType.DECISION_TREE:
                res = self.classify_tree(example, continuousOption, missingOption)

            elif self.model == ModelType.NAIVE_BAYES:
                res =  self.classify_nb(example, continuousOption, missingOption, m)

            elif self.model == ModelType.KNN:
                res =  self.classify_knn(example, k, missingOption, normOption)

            results.append(res)

        return results

    def print_classifier(self):

        if self.model == ModelType.DECISION_TREE:

            if type(self.classifier) is bool:
                print(self.classifier)
            else:
                self.classifier.print_tree(0)

    # Auxiliar methods
    # ----------------------------------------------------------------------------

    def train_tree(self, dataset, continuousOption, missingOption):
        return id3_train(dataset, self.attributes, continuousOption, missingOption)

    def classify_tree(self, example, continuousOption, missingOption):
        res = id3_classify(self.classifier, example, continuousOption, missingOption)

        if type(res) is tuple:
            (a,b) = res
            if type(a) is bool:
                return a
            elif type(b) is bool:
                return b
            else:
                if a >= b:
                    return True
                else:
                    return False
        else:
            return res

    def train_nb(self, dataset, continuousOption, missingOption, m):
        return nb_train(dataset, continuousOption, missingOption, m)

    def classify_nb(self, example, continuousOption, missingOption, m):
        return nb_classify(self.classifier, example, continuousOption, missingOption, m)

    def train_knn(self, dataset, k, missingOption, normOption, isEvaluating):
        return knn_train(dataset, k, missingOption, normOption, isEvaluating)

    def classify_knn(self, example, k, missingOption, normOption):
        return knn_classify(self.classifier, example, k, missingOption, normOption)
