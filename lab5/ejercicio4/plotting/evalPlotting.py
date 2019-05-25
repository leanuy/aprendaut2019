### DEPENDENCIAS
### ------------------

from .plotting import plotHeatmap, plotGroupBars, plotSubBars
from utils.const import CandidateDivision

### CONSTANTES
### ------------------

COLORS = ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#469990',  '#42d4f4', '#4363d8', '#000075', '#9F8BE5', '#9400FF']

### METODOS PRINCIPALES
### -------------------

def plotSingleEvaluation(evaluation, k):

    if k == 0:
        accuracy_candidates = evaluation['accuracy_candidates']
        metrics_candidates = evaluation['report_candidates_dict']
        confusion_matrix_candidates = evaluation['confusion_matrix_candidates']
        
        accuracy_parties = evaluation['accuracy_parties']
        metrics_parties = evaluation['report_parties_dict']
        confusion_matrix_parties = evaluation['confusion_matrix_parties']

    else:
        accuracy_candidates = evaluation['cv_accuracy_candidates']
        metrics_candidates = evaluation['cv_report_candidates_dict']
        confusion_matrix_candidates = evaluation['cv_confusion_matrix_candidates']
        
        accuracy_parties = evaluation['cv_accuracy_parties']
        metrics_parties = evaluation['cv_report_parties_dict']
        confusion_matrix_parties = evaluation['cv_confusion_matrix_parties']

    plotMetrics(accuracy_candidates, accuracy_parties, metrics_candidates, metrics_parties)
    plotConfusionMatrix(confusion_matrix_candidates, CandidateDivision.CANDIDATES)
    plotConfusionMatrix(confusion_matrix_parties, CandidateDivision.PARTIES)

def plotAllEvaluations(candidates, parties, is_pca=False):

    if not is_pca:
        title_candidates = 'Accuracy - Clasificadores por candidato según configuración paramétrica'
        title_parties = 'Accuracy - Clasificadores por partido según configuración paramétrica'
    
    else:
        title_candidates = 'Accuracy - Clasificadores por candidato según dimensionalidad'
        title_parties = 'Accuracy - Clasificadores por partido según dimensionalidad'

    meta = {
      'title': title_candidates,
      'xlabels': [str(i+1) for i in range(0, len(candidates))],
      'colors': [COLORS[1]]
    }

    metaC = {
      'title': title_parties,
      'xlabels': [str(i+1) for i in range(0, len(parties))],      
      'colors': [COLORS[7]]
    }

    plotSubBars((candidates, parties), (meta, metaC), True)

### METODOS AUXILIARES
### ------------------

def plotMetrics(accuracy_candidates, accuracy_parties, metrics_candidates, metrics_parties):

    dataset = [
      (metrics_candidates['micro avg']['precision'], metrics_parties['micro avg']['precision']),
      (metrics_candidates['macro avg']['precision'], metrics_parties['macro avg']['precision']),
      (metrics_candidates['weighted avg']['precision'], metrics_parties['weighted avg']['precision']),
      (metrics_candidates['micro avg']['recall'], metrics_parties['micro avg']['recall']),
      (metrics_candidates['macro avg']['recall'], metrics_parties['macro avg']['recall']),
      (metrics_candidates['weighted avg']['recall'], metrics_parties['weighted avg']['recall']),      
      (metrics_candidates['micro avg']['f1-score'], metrics_parties['micro avg']['f1-score']),
      (metrics_candidates['macro avg']['f1-score'], metrics_parties['macro avg']['f1-score']),
      (metrics_candidates['weighted avg']['f1-score'], metrics_parties['weighted avg']['f1-score'])      
    ]

    labels = [
      'Precision - Promedio micro', 'Precision - Promedio macro', 'Precision - Promedio ponderado',
      'Recall - Promedio micro', 'Recall - Promedio macro', 'Recall - Promedio ponderado',
      'F-Score - Promedio micro', 'F-Score - Promedio macro', 'F-Score - Promedio ponderado'
    ]

    meta = {
      'title': 'Métricas - Clasificador por candidato VS Clasificador por partido',
      'xlabels': ['Clasificador por candidato', 'Clasificador por partido'],
      'colors': COLORS
    }

    plotGroupBars(dataset, labels, meta)

def plotConfusionMatrix(confusion_matrix, division):

    if division == CandidateDivision.CANDIDATES:
        title = 'candidato'
    else:
        title = 'partido'
    
    meta = {
      'title': f'Matriz de Confusión - Clasificador por {title}'
    }

    # Generar única gráfica
    plotHeatmap(confusion_matrix, meta)