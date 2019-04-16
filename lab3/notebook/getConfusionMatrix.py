import csv
import os

# Dependencias de IPython
from IPython.display import display, clear_output, HTML
import tabulate
from ipywidgets import Button, Box, Layout
import ipywidgets as widgets

# Imprimir matrices de iris
def printIrisData(filename, printConfusionMatrix = True):
    hdir = os.path.dirname(__file__)
    matrix_data = os.path.join(hdir, 'matrix_data/' + filename + '.csv')
    f = open(matrix_data, 'r')
    reader = csv.reader(f, delimiter=',')
    i = 0
    matrix_rows = []
    matrix_rows.append(['X', 'Setosa', 'Versicolor', 'Virginica'])
    params_table = []
    params_table.append(['X', 'Precision', 'Recall', 'Fall-off','F-Measure'])
    for r in reader:
        if i == 0:
            accuracy = r[0]
        elif i == 1:
            precision = r[0]
            recall = r[1]
            falloff = r[2]
            fmeaseure = r[3]
        elif i == 2:
            precisionW = r[0]
            recallW = r[1]
            falloffW = r[2]
            fmeaseureW = r[3]
        elif i > 2 and i < 6:
            aux = r
            if i == 3:
                aux.insert(0, 'Setosa')
            elif i == 4:
                aux.insert(0, 'Versicolor')
            elif i == 5:
                aux.insert(0, 'Virginica')
            params_table.append(aux)
        elif i > 5 and i < 9:
            aux = r
            aux.insert(0, str(i - 9))
            matrix_rows.append(aux)
        i += 1

    prffm = ' \
        <div> \
          <style type="text/css"> \
          .tg  {border-collapse:collapse;border-spacing:0;} \
          .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top} \
          </style> \
          <table class="tg"> \
            <tr> \
              <th class="tg-0pky"><strong>Accuracy</strong></th> \
              <th class="tg-0pky"><strong>Precision promediada</strong></th> \
              <th class="tg-0pky"><strong>Recall promediada</strong></th> \
              <th class="tg-0pky"><strong>Fall-off promediada</strong></th> \
              <th class="tg-0pky"><strong>F-Measure promediada</strong></th> \
            </tr> \
            <tr> \
              <td class="tg-0pky">' + accuracy + '</td> \
              <td class="tg-0pky">' + precision + '</td> \
              <td class="tg-0pky">' + recall + '</td> \
              <td class="tg-0pky">' + falloff + '</td> \
              <td class="tg-0pky">' + fmeaseure + '</td> \
            </tr> \
          </table> \
        </div>'
    display(HTML(prffm))

    prffmw = ' \
        <div> \
          <style type="text/css"> \
          .tg  {border-collapse:collapse;border-spacing:0;} \
          .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top} \
          </style> \
          <table class="tg"> \
            <tr> \
              <th class="tg-0pky"><strong>Precision ponderada</strong></th> \
              <th class="tg-0pky"><strong>Recall ponderada</strong></th> \
              <th class="tg-0pky"><strong>Fall-off ponderada</strong></th> \
              <th class="tg-0pky"><strong>F-Measure ponderada</strong></th> \
            </tr> \
            <tr> \
              <td class="tg-0pky">' + precisionW + '</td> \
              <td class="tg-0pky">' + recallW + '</td> \
              <td class="tg-0pky">' + falloffW + '</td> \
              <td class="tg-0pky">' + fmeaseureW + '</td> \
            </tr> \
          </table> \
        </div>'
    display(HTML(prffmw))

    if printConfusionMatrix:
        display(HTML('<h2>Matriz de confusión</h2>'))
        display(HTML(tabulate.tabulate(matrix_rows, tablefmt='html')))

    display(HTML('<h2>Métricas</h2>'))
    display(HTML(tabulate.tabulate(params_table, tablefmt='html')))

# Imprimir matrices de covertype
def printCovertypeData(filename, printConfusionMatrix = True):
    hdir = os.path.dirname(__file__)
    matrix_data = os.path.join(hdir, 'matrix_data/' + filename + '.csv')
    f = open(matrix_data, 'r')
    reader = csv.reader(f, delimiter=',')
    i = 0
    params_table = []
    params_table.append(['X', 'Precision', 'Recall', 'Fall-off', 'F-Measure'])
    matrix_rows = []
    matrix_rows.append(['X', '1', '2', '3', '4', '5', '6', '7'])
    for r in reader:
        if i == 0:
            accuracy = r[0]
        elif i == 1:
            precision = r[0]
            recall = r[1]
            falloff = r[2]
            fmeaseure = r[3]
        elif i == 2:
            precisionW = r[0]
            recallW = r[1]
            falloffW = r[2]
            fmeaseureW = r[3]
        elif i == 3:
            aux = r
            aux.insert(0, '1')
            params_table.append(aux)
        elif i == 4:
            aux = r
            aux.insert(0, '2')
            params_table.append(aux)
        elif i == 5:
            aux = r
            aux.insert(0, '3')
            params_table.append(aux)
        elif i == 6:
            aux = r
            aux.insert(0, '4')
            params_table.append(aux)
        elif i == 7:
            aux = r
            aux.insert(0, '5')
            params_table.append(aux)
        elif i == 8:
            aux = r
            aux.insert(0, '6')
            params_table.append(aux)
        elif i == 9:
            aux = r
            aux.insert(0, '7')
            params_table.append(aux)
        elif i > 9 and i < 17:
            aux = r
            aux.insert(0, str(i - 9))
            matrix_rows.append(aux)
        i += 1

    prffm = ' \
        <div> \
          <style type="text/css"> \
          .tg  {border-collapse:collapse;border-spacing:0;} \
          .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top} \
          </style> \
          <table class="tg"> \
            <tr> \
              <th class="tg-0pky"><strong>Accuracy</strong></th> \
              <th class="tg-0pky"><strong>Precision promediada</strong></th> \
              <th class="tg-0pky"><strong>Recall promediada</strong></th> \
              <th class="tg-0pky"><strong>Fall-off promediada</strong></th> \
              <th class="tg-0pky"><strong>F-Measure promediada</strong></th> \
            </tr> \
            <tr> \
              <td class="tg-0pky">' + accuracy + '</td> \
              <td class="tg-0pky">' + precision + '</td> \
              <td class="tg-0pky">' + recall + '</td> \
              <td class="tg-0pky">' + falloff + '</td> \
              <td class="tg-0pky">' + fmeaseure + '</td> \
            </tr> \
          </table> \
        </div>'
    display(HTML(prffm))

    prffmw = ' \
        <div> \
          <style type="text/css"> \
          .tg  {border-collapse:collapse;border-spacing:0;} \
          .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top} \
          </style> \
          <table class="tg"> \
            <tr> \
              <th class="tg-0pky"><strong>Precision ponderada</strong></th> \
              <th class="tg-0pky"><strong>Recall ponderada</strong></th> \
              <th class="tg-0pky"><strong>Fall-off ponderada</strong></th> \
              <th class="tg-0pky"><strong>F-Measure ponderada</strong></th> \
            </tr> \
            <tr> \
              <td class="tg-0pky">' + precisionW + '</td> \
              <td class="tg-0pky">' + recallW + '</td> \
              <td class="tg-0pky">' + falloffW + '</td> \
              <td class="tg-0pky">' + fmeaseureW + '</td> \
            </tr> \
          </table> \
        </div>'
    display(HTML(prffmw))

    if printConfusionMatrix:
        display(HTML('<h2>Matriz de confusión</h2>'))
        display(HTML(tabulate.tabulate(matrix_rows, tablefmt='html')))

    display(HTML('<h2>Métricas</h2>'))
    display(HTML(tabulate.tabulate(params_table, tablefmt='html')))

def printNotFound():
    prffmw = '<h1>Archivo no encontrado.</h1>'
    display(HTML(prffmw))

# Imprimir titulo
def printTitle():
    display(HTML('<h1 style="text-align: center;">Seleccione los parametros del caso que desee visualizar</h1>'))

ConjuntoDict = { 'Conjunto: Iris': 'Iris', 'Conjunto: Covertype': 'Covertype' }
ModeloDict = { 'Modelo: Árbol de decisión': 'Arbol', 'Modelo: Bosque de decisión': 'Bosque', 'Modelo: Bayes sencillo': 'Bayes', 'Modelo: K vecinos más cercanos': 'KNN' }
ValidacionDict = { 'Validación: Normal': 'Normal', 'Validación: Cruzada': 'Cross' }

ContinuousTreesDict = { 'Continuos: Partir en intervalos fijos': 'Fixed', 'Continuos: Partir en intervalos variables': 'Variable', 'Continuos: Intervalos que maximicen ganancia': 'C45' }
MeasureTreesDict = { 'Medida: Ganancia': 'Gain', 'Medida: Ratio de ganancia': 'GainRatio', 'Medida: Reducción de impureza': 'ImpurityReduction' }

OnehotDict = { 'Revertir one-hot encoding': 'No Onehot', 'Mantener one-hot encoding': 'Onehot' }

ContinuousBayesDict = { 'Continuos: Estandarizar según distribución': 'Standarization', 'Continuos: Partir en intervalos variables': 'Variable' }
mEstDict = { 'm estimador: 0': 'mEst - 0.0', 'm estimador: 0.5': 'mEst - 0.5', 'm estimador: 1': 'mEst - 1.0', 'm estimador: 10': 'mEst - 10.0', 'm estimador: 100': 'mEst - 100.0' }

KDict = { 'K: 1': 'k - 1', 'K: 3': 'k - 3', 'K: 5': 'k - 5' }
MeasureKNNDict = { "Medida: Distancia 'Manhattan'": "Distancia 'Manhattan'", 'Medida: Distancia Euclídea': 'Distancia Euclídea', 'Medida: Distancia de Chebychev': 'Distancia de Chebychev', 'Medida: Distancia de Mahalanobis': 'Distancia de Mahalanobis' }
NormDict = { 'Norma: Euclídea (División por norma)': 'Norma Euclídea', 'Norma: Min-Max (Reescalamiento)': 'Norma Min-Max', 'Norma: Z-Score (Estandarización)': 'Norma Z-Score', 'Norma: Ninguna': 'Ninguna Norma' }

box_layout = Layout(display='flex',
                    flex_flow='row',
                    margin='8px 0px 8px 0px',
                    width='100%',
                    justify_content='space-between')

# Independiente del modelo
Conjunto = widgets.Dropdown(options=ConjuntoDict.keys())
Modelo = widgets.Dropdown(options=ModeloDict.keys())
Validacion = widgets.Dropdown(options=ValidacionDict.keys())

boxGeneral = Box(children=[Conjunto, Modelo, Validacion], layout=box_layout)

# Arboles y Bosques
ContinuousTrees = widgets.Dropdown(options=ContinuousTreesDict.keys())
MeasureTrees = widgets.Dropdown(options=MeasureTreesDict.keys())

boxArboles = Box(children=[ContinuousTrees, MeasureTrees], layout=box_layout)

# Bayes y KNN
Onehot = widgets.Dropdown(options=OnehotDict.keys())

# Bayes
ContinuousBayes = widgets.Dropdown(options=ContinuousBayesDict.keys())
mEst = widgets.Dropdown(options=mEstDict.keys())

boxBayes = Box(children=[Onehot, ContinuousBayes, mEst], layout=box_layout)

# KNN
K = widgets.Dropdown(options=KDict.keys())
MeasureKNN = widgets.Dropdown(options=MeasureKNNDict.keys(), value='Medida: Distancia Euclídea')
Norm = widgets.Dropdown(options=NormDict.keys())

boxKNN = Box(children=[Onehot, K, MeasureKNN, Norm], layout=box_layout)

main_box_layout = Layout(display='flex',
                        flex_flow='column',
                        width='100%')

def getBox(model):
    if model == 'Arbol' or model == 'Bosque':
      main_box = Box(children=[boxGeneral, boxArboles], layout=main_box_layout) 
    elif model == 'Bayes':
      main_box = Box(children=[boxGeneral, boxBayes], layout=main_box_layout)           
    else: # KNN
      main_box = Box(children=[boxGeneral, boxKNN], layout=main_box_layout)     
    return main_box

def refreshMatrix(dropdown = None):
    clear_output()
    printTitle()
    main_box = getBox(ModeloDict[Modelo.value])
    display(main_box)

    try:
        fileName = ConjuntoDict[Conjunto.value] + ', ' + ModeloDict[Modelo.value] + ', '
        if ModeloDict[Modelo.value] == 'Arbol' or ModeloDict[Modelo.value] == 'Bosque':
            fileName += ContinuousTreesDict[ContinuousTrees.value] + ', ' + MeasureTreesDict[MeasureTrees.value] + ', '
        elif ModeloDict[Modelo.value] == 'Bayes':
            fileName += OnehotDict[Onehot.value] + ', ' + ContinuousBayesDict[ContinuousBayes.value] + ', ' + mEstDict[mEst.value] + ', '
        else: # KNN
            fileName += OnehotDict[Onehot.value] + ', ' + KDict[K.value] + ', ' + MeasureKNNDict[MeasureKNN.value] + ', ' + NormDict[Norm.value] + ', '
        fileName += ValidacionDict[Validacion.value]
        if ConjuntoDict[Conjunto.value] == 'Covertype':
            printCovertypeData(fileName, ValidacionDict[Validacion.value] == 'Normal')
        else: # Iris
            printIrisData(fileName, ValidacionDict[Validacion.value] == 'Normal')
    except:
        printNotFound()
        

Conjunto.observe(refreshMatrix, names='value')
Modelo.observe(refreshMatrix, names='value')
Validacion.observe(refreshMatrix, names='value')

ContinuousTrees.observe(refreshMatrix, names='value')
MeasureTrees.observe(refreshMatrix, names='value')

Onehot.observe(refreshMatrix, names='value')

ContinuousBayes.observe(refreshMatrix, names='value')
mEst.observe(refreshMatrix, names='value')

K.observe(refreshMatrix, names='value')
MeasureKNN.observe(refreshMatrix, names='value')
Norm.observe(refreshMatrix, names='value')

# Todo

refreshMatrix()