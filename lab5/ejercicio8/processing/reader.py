### DEPENDENCIAS
### ------------------
import pandas as pd

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDatasetBoard(filename):
    dataset = pd.read_csv(filename)
    qValues = dataset.iloc[1:, 81]
    boards = dataset.iloc[1:, 0:81]
    return qValues.apply(pd.to_numeric, downcast='unsigned'), boards.apply(pd.to_numeric, downcast='unsigned')

def readDatasetMetrics(filename):
    dataset = pd.read_csv(filename)
    qValues = dataset.iloc[1:, 9]
    metrics = dataset.iloc[1:, 0:9]
    return qValues.apply(pd.to_numeric, downcast='unsigned'), metrics.apply(pd.to_numeric, downcast='unsigned')