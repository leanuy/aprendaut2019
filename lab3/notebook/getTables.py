import csv
import os

import matplotlib.pyplot as plt
import numpy as np

#  Codigo para celda del notebook
# %matplotlib inline
# %config InlineBackend.print_figure_kwargs={'bbox_inches':None}
# import getResultsTables.py

# Dependencias de IPython
from IPython.display import display, clear_output, HTML
import tabulate
from ipywidgets import Button, Box, Layout
import ipywidgets as widgets
from math import log10, floor

ConjuntoDict = { 'Conjunto: Iris': 'Iris', 'Conjunto: Covertype': 'Covertype' }
ModeloDict = { 'Modelo: Árbol de decisión': 'Arbol', 'Modelo: Bosque de decisión': 'Bosque', 'Modelo: Bayes sencillo': 'Bayes', 'Modelo: K vecinos más cercanos': 'KNN' }
ValidacionDict = { 'Validación: Normal': 'Normal', 'Validación: Cruzada': 'Cross' }

ContinuousTreesDict = { 'Continuos: Partir en intervalos fijos': 'Fixed', 'Continuos: Partir en intervalos variables': 'Variable', 'Continuos: Intervalos que maximicen ganancia': 'C45' }
MeasureTreesDict = { 'Medida: Ganancia': 'Gain', 'Medida: Ratio de ganancia': 'GainRatio', 'Medida: Reducción de impureza': 'ImpurityReduction' }

OnehotDict = { 'Revertir one-hot encoding': 'No Onehot', 'Mantener one-hot encoding': 'Onehot' }

ContinuousBayesDict = { 'Continuos: Estandarizar según distribución': 'Standarization', 'Continuos: Partir en intervalos variables': 'Variable' }
mEstDict = { 'm estimador: 0': 'mEst - 0.0', 'm estimador: 0.01': 'mEst - 0.01', 'm estimador: 0.5': 'mEst - 0.5', 'm estimador: 1': 'mEst - 1.0', 'm estimador: 100': 'mEst - 100.0' }

KDict = { 'K: 1': 'k - 1', 'K: 3': 'k - 3', 'K: 7': 'k - 7' }
MeasureKNNDict = { "Medida: Distancia 'Manhattan'": "Distancia 'Manhattan'", 'Medida: Distancia Euclídea': 'Distancia Euclídea', 'Medida: Distancia de Chebychev': 'Distancia de Chebychev' }
NormDict = { 'Norma: Euclídea (División por norma)': 'Norma Euclídea', 'Norma: Min-Max (Reescalamiento)': 'Norma Min-Max', 'Norma: Z-Score (Estandarización)': 'Norma Z-Score' }

humanizeOnehot = { 'No Onehot': 'No', 'Onehot': 'Si' }
humanizeMEst = { 'mEst - 0.0': '0.0', 'mEst - 0.01': '0.01', 'mEst - 0.5': '0.5', 'mEst - 1.0': '1.0', 'mEst - 100.0': '100.0' }
humanizeK = { 'k - 1': '1', 'k - 3': '3', 'k - 7': '7' }

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

main_box_layout = Layout(display='flex',
                        flex_flow='column',
                        width='100%')

main_box = Box(children=[boxGeneral], layout=main_box_layout)

datosTrees = {}
datosBayes = {}
datosKNN = {}
for conjunto in ConjuntoDict.values():
    datosTrees[conjunto] = {}
    datosBayes[conjunto] = {}
    datosKNN[conjunto] = {}
    for modelo in ModeloDict.values():
        datosTrees[conjunto][modelo] = {}
        datosBayes[conjunto][modelo] = {}
        datosKNN[conjunto][modelo] = {}
        for validacion in ValidacionDict.values():
            datosTrees[conjunto][modelo][validacion] = {}
            datosBayes[conjunto][modelo][validacion] = {}
            datosKNN[conjunto][modelo][validacion] = {}
            # Arbol y Bosques
            for continuous in ContinuousTreesDict.values():
                if conjunto == 'Iris' or (conjunto == 'Covertype' and continuous != 'Variable'):
                    datosTrees[conjunto][modelo][validacion][continuous] = {}
                    for measure in MeasureTreesDict.values():
                        datosTrees[conjunto][modelo][validacion][continuous][measure] = conjunto + ', ' + modelo + ', ' + continuous + ', ' + measure + ', ' + validacion
            for onehot in OnehotDict.values():
                datosBayes[conjunto][modelo][validacion][onehot] = {}
                datosKNN[conjunto][modelo][validacion][onehot] = {}
                # Bayes
                for continuous in ContinuousBayesDict.values():
                    datosBayes[conjunto][modelo][validacion][onehot][continuous] = {}
                    for mEst in mEstDict.values():
                        datosBayes[conjunto][modelo][validacion][onehot][continuous][mEst] = conjunto + ', ' + modelo + ', ' + onehot + ', ' + continuous + ', ' + mEst + ', ' + validacion
                # KNN
                for k in KDict.values():
                    datosKNN[conjunto][modelo][validacion][onehot][k] = {}
                    for measure in MeasureKNNDict.values():
                        datosKNN[conjunto][modelo][validacion][onehot][k][measure] = {}
                        for norm in NormDict.values():
                            datosKNN[conjunto][modelo][validacion][onehot][k][measure][norm] = conjunto + ', ' + modelo + ', ' + onehot + ', ' + k + ', ' + measure + ', ' + norm + ', ' + validacion

def round_sig(x, sig=4):
    return round(x, sig-int(floor(log10(abs(x))))-1)

# Imprimir matrices de iris
def printData(dataset, model, validation):
    params = ['<b>|</b>', '<b>Accuracy</b>', '<b>Precisión promediada</b>', '<b>Precisión ponderada</b>', '<b>Recall promediado</b>', '<b>Recall ponderado</b>', '<b>Fall-off promediado</b>', '<b>Fall-off ponderado</b>', '<b>F-Measure promediada</b>', '<b>F-Measure ponderado</b>']
    if model == 'Arbol' or model == 'Bosque':
        paramsTable = ['<b>Indice</b>', '<b>Onehot</b>', '<b>Continuos</b>', '<b>Medida</b>'] + params
    elif model == 'Bayes':
        paramsTable = ['<b>Indice</b>', '<b>Onehot</b>', '<b>Continuos</b>', '<b>mEst</b>'] + params
    else: # KNN
        paramsTable = ['<b>Indice</b>', '<b>Onehot</b>', '<b>K</b>', '<b>Medida</b>', '<b>Norma</b>'] + params
    
    matrix_data = []
    matrix_data.append(paramsTable)

    index = []
    fall_off = []
    f_measure = []
    fall_off_g = []
    f_measure_g = []

    if dataset == 'Iris':
        if model == 'Arbol' or model == 'Bosque':
                for continuous in datosTrees[dataset][model][validation]:
                    for measure in datosTrees[dataset][model][validation][continuous]:
                        data = getData(datosTrees[dataset][model][validation][continuous][measure])
                        
                        fall_off.append(data[6])
                        f_measure.append(data[8])
                        fall_off_g.append(data[5])
                        f_measure_g.append(data[7])
                        index.append(len(f_measure))

                        paramsTable = [index[-1], 'No aplica', continuous, measure, '|']
                        paramsTable.extend(data)
                        matrix_data.append(paramsTable)
        elif model == 'Bayes':
            for continuous in datosBayes[dataset][model][validation]['Onehot']:
                for mEst in datosBayes[dataset][model][validation]['Onehot'][continuous]:
                    data = getData(datosBayes[dataset][model][validation]['Onehot'][continuous][mEst])
                        
                    fall_off.append(data[6])
                    f_measure.append(data[8])
                    fall_off_g.append(data[5])
                    f_measure_g.append(data[7])
                    index.append(len(f_measure))

                    paramsTable = [index[-1], 'No aplica', continuous, humanizeMEst[mEst], '|']
                    paramsTable.extend(data)
                    matrix_data.append(paramsTable)
        else: # KNN
            for k in datosKNN[dataset][model][validation]['Onehot']:
                for measure in datosKNN[dataset][model][validation]['Onehot'][k]:
                    for norm in datosKNN[dataset][model][validation]['Onehot'][k][measure]:
                        data = getData(datosKNN[dataset][model][validation]['No Onehot'][k][measure][norm])

                        
                        fall_off.append(data[6])
                        f_measure.append(data[8])
                        fall_off_g.append(data[5])
                        f_measure_g.append(data[7])
                        index.append(len(f_measure))

                        paramsTable = [index[-1], 'No aplica', humanizeK[k], measure, norm, '|']
                        paramsTable.extend(data)
                        matrix_data.append(paramsTable)
    else:
        if model == 'Arbol' or model == 'Bosque':
            for continuous in datosTrees[dataset][model][validation]:
                for measure in datosTrees[dataset][model][validation][continuous]:
                    data = getData(datosTrees[dataset][model][validation][continuous][measure])
                    
                    fall_off.append(data[6])
                    f_measure.append(data[8])
                    fall_off_g.append(data[5])
                    f_measure_g.append(data[7])
                    index.append(len(f_measure))

                    paramsTable = [index[-1], 'No', continuous, measure, '|']
                    paramsTable.extend(data)
                    matrix_data.append(paramsTable)
        elif model == 'Bayes':
            for onehot in datosBayes[dataset][model][validation]:
                for continuous in datosBayes[dataset][model][validation][onehot]:
                    for mEst in datosBayes[dataset][model][validation][onehot][continuous]:
                        data = getData(datosBayes[dataset][model][validation][onehot][continuous][mEst])
                        
                        fall_off.append(data[6])
                        f_measure.append(data[8])
                        fall_off_g.append(data[5])
                        f_measure_g.append(data[7])
                        index.append(len(f_measure))
                        
                        paramsTable = [index[-1], humanizeOnehot[onehot], continuous, humanizeMEst[mEst], '|']
                        paramsTable.extend(data)
                        matrix_data.append(paramsTable)
        else: # KNN
            for onehot in datosKNN[dataset][model][validation]:
                for k in datosKNN[dataset][model][validation][onehot]:
                    for measure in datosKNN[dataset][model][validation][onehot][k]:
                        for norm in datosKNN[dataset][model][validation][onehot][k][measure]:
                            data = getData(datosKNN[dataset][model][validation][onehot][k][measure][norm])

                            fall_off.append(data[6])
                            f_measure.append(data[8])
                            fall_off_g.append(data[5])
                            f_measure_g.append(data[7])
                            index.append(len(f_measure))

                            paramsTable = [index[-1], humanizeOnehot[onehot], humanizeK[k], measure, norm, '|']
                            paramsTable.extend(data)
                            matrix_data.append(paramsTable)

    # ACA

    showCharts(index, fall_off, f_measure, fall_off_g, f_measure_g)
    display(HTML(tabulate.tabulate(matrix_data, tablefmt='html')))

def showCharts(name, fall_off, f_measure, fall_off_g, f_measure_g):
    # data to plot
    n_groups = len(name)
    fall_off_data = fall_off
    f_measure_data = f_measure
    fall_off_g_data = fall_off_g
    f_measure_g_data = f_measure_g
    
    # create plot
    fig, ax = plt.subplots(figsize=(15,5))
    index = np.arange(n_groups)
    bar_width = 0.24
    opacity = 0.8
    
    rects1 = plt.bar(index, [float(x) for x in f_measure_data], bar_width,  
    alpha=opacity,
    color='#e1974c',
    label='F-measure ponderada')

    rects2 = plt.bar(index + bar_width, [float(x) for x in f_measure_g_data], bar_width,
    alpha=opacity,
    color='#84ba5e',
    label='f-measure genérica')

    rects3 = plt.bar(index + (2 * bar_width), [float(x) for x in fall_off_data], bar_width,
    alpha=opacity,
    color='#d35e60',
    label='Fall-Off ponderada')

    rects4 = plt.bar(index + (3 * bar_width), [float(x) for x in fall_off_g_data], bar_width,
    alpha=opacity,
    color='#7293cb',
    label='Fall-Off genérica')

    plt.title('Fall-off - F-Measure')
    
    plt.xticks(index + bar_width, name)
    plt.legend()
    plt.show()

def getData(fileName):
    hdir = os.path.dirname(__file__)
    matrix_data = os.path.join(hdir, 'matrix_data/' + fileName + '.csv')
    f = open(matrix_data, 'r')
    reader = csv.reader(f, delimiter=',')
    i = 0
    for r in reader:
        if i == 0:
            accuracy = r[0][:6]
        elif i == 1:
            precision = r[0][:6]
            recall = r[1][:6]
            falloff = r[2][:6]
            fmeaseure = r[3][:6]
        elif i == 2:
            precisionW = r[0][:6]
            recallW = r[1][:6]
            falloffW = r[2][:6]
            fmeaseureW = r[3][:6]
        else:
            break
        i += 1
    return [accuracy, precision, precisionW, recall, recallW, falloff, falloffW, fmeaseure, fmeaseureW]

def printNotFound():
    prffmw = '<h1>No se generaron resultados para esta configuración.</h1>'
    display(HTML(prffmw))

# Imprimir titulo
def printTitle():
    display(HTML('<h1 style="text-align: center;">Seleccione la evaluación que desee visualizar</h1>'))

def refreshMatrix(dropdown = None):
    clear_output()
    printTitle()
    display(main_box)
    try:
        printData(ConjuntoDict[Conjunto.value], ModeloDict[Modelo.value], ValidacionDict[Validacion.value])
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        printNotFound()

Conjunto.observe(refreshMatrix, names='value')
Modelo.observe(refreshMatrix, names='value')
Validacion.observe(refreshMatrix, names='value')

# Todo

refreshMatrix()