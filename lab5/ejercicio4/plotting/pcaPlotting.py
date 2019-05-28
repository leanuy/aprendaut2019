### DEPENDENCIAS
### ------------------

from sklearn.decomposition import PCA

from .plotting import plotCurve

### CONSTANTES
### ------------------

COLORS = ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF']

### METODO PRINCIPAL
### ----------------

def plotPCA(dataset_full, dataset_type):

    dataset, _ = dataset_full

    pca = PCA(n_components=26)
    pca.fit_transform(dataset.values)
    variance_ratio = list(pca.explained_variance_ratio_)

    plotVarianceRatio(variance_ratio, dataset_type)
        
### METODOS AUXILIARES
### ------------------
    
def plotVarianceRatio(variance_ratio, dataset_type):

    # Generar metadatos para la gráfica
    meta = {
      'title': f'Ratio de Varianza - {dataset_type}',
      'xlabel': 'Número de Componentes',
      'ylabel': '% Varianza',
      'colors': [COLORS[0]]
    }

    # Generar única gráfica
    plotCurve(variance_ratio, meta)