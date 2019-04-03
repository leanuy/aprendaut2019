import csv
import os

# Dependencias de IPython
from IPython.display import display, clear_output, HTML
import tabulate
from ipywidgets import Button, Box, Layout

descriptions_iris = ['Arbol del conjunto Iris, Ganancia como medida, atributos continuos partiendo en intervalos fijos. Validación cruzada .',
  'Arbol del conjunto Iris, GainRatio como medida, trata atributos continuos partiendo en intervalos fijos. Validación cruzada ',
  'Arbol del conjunto Iris, Impurity Reduction como medida, atributos continuos partiendo en intervalos fijos. Validación cruzada ',
  'Arbol del conjunto Iris, Ganancia como medida, atributos continuos partiendo en intervalos variables. Validación cruzada ',
  'Arbol del conjunto Iris, GainRatio como medida, atributos continuos partiendo en intervalos variables. Validación cruzada ',
  'Arbol del conjunto Iris, Impurity Reduction como medida, atributos continuos partiendo en intervalos variables. Validación cruzada ',
  'Arbol del conjunto Iris, Ganancia como medida, atributos continuos maximizando ganancia local (C4.5). Validación cruzada ',
  'Arbol del conjunto Iris, GainRatio como medida, atributos continuos maximizando ganancia local (C4.5). Validación cruzada ',
  'Arbol del conjunto Iris, Impurity Reduction como medida, atributos continuos maximizando ganancia local (C4.5). Validación cruzada ',
  'Bosque del conjunto Iris, Ganancia como medida, atributos continuos partiendo en intervalos fijos. Validación cruzada ',
  'Bosque del conjunto Iris, GainRatio como medida, atributos continuos partiendo en intervalos fijos. Validación cruzada ',
  'Bosque del conjunto Iris, Impurity Reduction como medida, atributos continuos partiendo en intervalos fijos. Validación cruzada ',
  'Bosque del conjunto Iris, Ganancia como medida, atributos continuos partiendo en intervalos variables. Validación cruzada ',
  'Bosque del conjunto Iris, GainRatio como medida, atributos continuos partiendo en intervalos variables. Validación cruzada ',
  'Bosque del conjunto Iris, Impurity Reduction como medida, atributos continuos partiendo en intervalos variables. Validación cruzada ',
  'Bosque del conjunto Iris, Ganancia como medida, atributos continuos maximizando ganancia local (C4.5). Validación cruzada ',
  'Bosque del conjunto Iris, GainRatio como medida, atributos continuos maximizando ganancia local (C4.5). Validación cruzada ',
  'Bosque del conjunto Iris, Impurity Reduction como medida, atributos continuos maximizando ganancia local (C4.5). Validación cruzada ',
  ]

descriptions_covertye = ['Arbol del conjunto CoverType, Ganancia como medida, atributos continuos partiendo en intervalos fijos. Validación 80/20.',
  'Arbol del conjunto CoverType, GainRatio como medida, atributos continuos partiendo en intervalos fijos. Validación 80/20',
  'Arbol del conjunto CoverType, Impurity Reduction como medida, atributos continuos partiendo en intervalos fijos. Validación 80/20',
  'Arbol del conjunto CoverType, Ganancia como medida, atributos continuos maximizando ganancia local (C4.5). Validación 80/20',
  'Arbol del conjunto CoverType, GainRatio como medida, atributos continuos maximizando ganancia local (C4.5). Validación 80/20',
  'Arbol del conjunto CoverType, Impurity Reduction como medida, atributos continuos maximizando ganancia local (C4.5). Validación 80/20',
  'Bosque del conjunto CoverType, Ganancia como medida, atributos continuos partiendo en intervalos fijos. Validación 80/20',
  'Bosque del conjunto CoverType, GainRatio como medida, atributos continuos partiendo en intervalos fijos. Validación 80/20',
  'Bosque del conjunto CoverType, Impurity Reduction como medida, atributos continuos partiendo en intervalos fijos. Validación 80/20',
  'Bosque del conjunto CoverType, Ganancia como medida, atributos continuos maximizando ganancia local (C4.5). Validación 80/20',
  'Bosque del conjunto CoverType, GainRatio como medida, atributos continuos maximizando ganancia local (C4.5). Validación 80/20',
  'Bosque del conjunto CoverType, Impurity Reduction como medida, atributos continuos maximizando ganancia local (C4.5). Validación 80/20',
  ]


# Imprimir matrices de iris
def printIrisData(filename, file_number):
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
        i += 1

    print()
    print('Descripción: ', end='')
    print(descriptions_iris[file_number - 1])
    print()
    display(HTML('<p><strong>Accuracy</strong>: ' + accuracy + '</p>'))

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
              <th class="tg-0pky"><strong>Precision mean</strong></th> \
              <th class="tg-0pky"><strong>Recall mean</strong></th> \
              <th class="tg-0pky"><strong>Fall-off mean</strong></th> \
              <th class="tg-0pky"><strong>F-Measure mean</strong></th> \
            </tr> \
            <tr> \
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
              <th class="tg-0pky"><strong>Precision weighted mean</strong></th> \
              <th class="tg-0pky"><strong>Recall weighted mean</strong></th> \
              <th class="tg-0pky"><strong>Fall-off weighted mean</strong></th> \
              <th class="tg-0pky"><strong>F-Measure weighted mean</strong></th> \
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

    display(HTML('<h2>Métricas</h2>'))
    display(HTML(tabulate.tabulate(params_table, tablefmt='html')))

# Imprimir matrices de covertype
def printCovertypeData(filename):
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

    print()
    print('Descripción: ', end='')
    print(descriptions_covertye[ord(filename[-1]) - 97])
    print()
    display(HTML('<p><strong>Accuracy</strong>: ' + accuracy + '</p>'))

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
              <th class="tg-0pky"><strong>Precision mean</strong></th> \
              <th class="tg-0pky"><strong>Recall mean</strong></th> \
              <th class="tg-0pky"><strong>Fall-off mean</strong></th> \
              <th class="tg-0pky"><strong>F-Measure mean</strong></th> \
            </tr> \
            <tr> \
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
              <th class="tg-0pky"><strong>Precision weighted mean</strong></th> \
              <th class="tg-0pky"><strong>Recall weighted mean</strong></th> \
              <th class="tg-0pky"><strong>Fall-off weighted mean</strong></th> \
              <th class="tg-0pky"><strong>F-Measure weighted mean</strong></th> \
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

    display(HTML('<h2>Matriz de confusión</h2>'))
    display(HTML(tabulate.tabulate(matrix_rows, tablefmt='html')))

    display(HTML('<h2>Métricas</h2>'))
    display(HTML(tabulate.tabulate(params_table, tablefmt='html')))

# Imprimir titulo
def printTitle():
    display(HTML('<h1 style="text-align: center;">Seleccione un caso para visualizar de la botonera</h1>'))

# Imprimir tabla de indices
def printButtonDescriptions():

    buttonDescriptions = ' \
        <div> \
          <style type="text/css"> \
          .tg  {border-collapse:collapse;border-spacing:0;} \
          .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;} \
          .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top} \
          </style> \
          <table class="tg"> \
            <tr> \
              <th class="tg-0pky"><strong>Botón</strong></th> \
              <th class="tg-0pky" style="text-align: center;"><strong>Descripción</strong></th> \
            </tr> \
            <tr> \
              <td class="tg-0pky">1</td> \
              <td class="tg-0pky">' + descriptions_iris[0] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">2</td> \
              <td class="tg-0pky">' + descriptions_iris[1] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">3</td> \
              <td class="tg-0pky">' + descriptions_iris[2] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">4</td> \
              <td class="tg-0pky">' + descriptions_iris[3] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">5</td> \
              <td class="tg-0pky">' + descriptions_iris[4] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">6</td> \
              <td class="tg-0pky">' + descriptions_iris[5] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">7</td> \
              <td class="tg-0pky">' + descriptions_iris[6] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">8</td> \
              <td class="tg-0pky">' + descriptions_iris[7] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">9</td> \
              <td class="tg-0pky">' + descriptions_iris[8] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">10</td> \
              <td class="tg-0pky">' + descriptions_iris[9] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">11</td> \
              <td class="tg-0pky">' + descriptions_iris[10] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">12</td> \
              <td class="tg-0pky">' + descriptions_iris[11] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">13</td> \
              <td class="tg-0pky">' + descriptions_iris[12] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">14</td> \
              <td class="tg-0pky">' + descriptions_iris[13] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">15</td> \
              <td class="tg-0pky">' + descriptions_iris[14] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">16</td> \
              <td class="tg-0pky">' + descriptions_iris[15] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">17</td> \
              <td class="tg-0pky">' + descriptions_iris[16] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">18</td> \
              <td class="tg-0pky">' + descriptions_iris[17] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">a</td> \
              <td class="tg-0pky">' + descriptions_covertye[0] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">b</td> \
              <td class="tg-0pky">' + descriptions_covertye[1] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">c</td> \
              <td class="tg-0pky">' + descriptions_covertye[2] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">d</td> \
              <td class="tg-0pky">' + descriptions_covertye[3] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">e</td> \
              <td class="tg-0pky">' + descriptions_covertye[4] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">f</td> \
              <td class="tg-0pky">' + descriptions_covertye[5] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">g</td> \
              <td class="tg-0pky">' + descriptions_covertye[6] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">h</td> \
              <td class="tg-0pky">' + descriptions_covertye[7] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">i</td> \
              <td class="tg-0pky">' + descriptions_covertye[8] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">j</td> \
              <td class="tg-0pky">' + descriptions_covertye[9] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">k</td> \
              <td class="tg-0pky">' + descriptions_covertye[10] + '</td> \
            </tr> \
            <tr> \
              <td class="tg-0pky">l</td> \
              <td class="tg-0pky">' + descriptions_covertye[11] + '</td> \
            </tr> \
          </table> \
        </div>'

    display(HTML(buttonDescriptions))

# Fila de botones para Covertype. 18 combinaciones
Comb1Button = Button(
    id='1',
    description='1',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb2Button = Button(
    description='2',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb3Button = Button(
    description='3',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb4Button = Button(
    description='4',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb5Button = Button(
    description='5',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb6Button = Button(
    description='6',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb7Button = Button(
    description='7',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb8Button = Button(
    description='8',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb9Button = Button(
    description='9',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb10Button = Button(
    description='10',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb11Button = Button(
    description='11',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb12Button = Button(
    description='12',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb13Button = Button(
    description='13',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb14Button = Button(
    description='14',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb15Button = Button(
    description='15',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb16Button = Button(
    description='16',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb17Button = Button(
    description='17',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
Comb18Button = Button(
    description='18',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
box1_layout = Layout(display='flex',
                    flex_flow='row',
                    margin='8px 0px 8px 0px',
                    width='100%')
box1 = Box(children=[Comb1Button, Comb2Button, Comb3Button, Comb4Button,
                     Comb5Button, Comb6Button, Comb7Button, Comb8Button,
                     Comb9Button, Comb10Button, Comb11Button, Comb12Button,
                     Comb13Button, Comb14Button, Comb15Button, Comb16Button,
                     Comb17Button, Comb18Button], layout=box1_layout)


# Fila de botones para Covertype. 12 combinaciones
CombAButton = Button(
    id='1',
    description='a',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombBButton = Button(
    description='b',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombCButton = Button(
    description='c',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombDButton = Button(
    description='d',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombEButton = Button(
    description='e',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombFButton = Button(
    description='f',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombGButton = Button(
    description='g',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombHButton = Button(
    description='h',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombIButton = Button(
    description='i',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombJButton = Button(
    description='j',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombKButton = Button(
    description='k',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
CombLButton = Button(
    description='l',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    layout=Layout(max_width='150px', margin='0px 16px 0px 0px')
)
box2_layout = Layout(display='flex',
                    flex_flow='row',
                    margin='8px 0px 8px 0px',
                    width='100%')
box2 = Box(children=[CombAButton, CombBButton, CombCButton, CombDButton,
                     CombEButton, CombFButton, CombGButton, CombHButton,
                     CombIButton, CombJButton, CombKButton, CombLButton], layout=box2_layout)


# Todo
main_box_layout = Layout(display='flex',
                        flex_flow='column',
                        width='100%')
main_box = Box(children=[box1, box2], layout=main_box_layout)

def changeMatrix(btn):
    clear_output()
    printTitle()
    try:
        file_number = int(btn.description)
        printIrisData('confusion_matrix_iris_' + btn.description, file_number)
    except:
        printCovertypeData('confusion_matrix_covertype_' + btn.description)
        
    display(main_box)
    printButtonDescriptions()

# Iris events
Comb1Button.on_click(changeMatrix)
Comb2Button.on_click(changeMatrix)
Comb3Button.on_click(changeMatrix)
Comb4Button.on_click(changeMatrix)
Comb5Button.on_click(changeMatrix)
Comb6Button.on_click(changeMatrix)
Comb7Button.on_click(changeMatrix)
Comb8Button.on_click(changeMatrix)
Comb9Button.on_click(changeMatrix)
Comb10Button.on_click(changeMatrix)
Comb11Button.on_click(changeMatrix)
Comb12Button.on_click(changeMatrix)
Comb13Button.on_click(changeMatrix)
Comb14Button.on_click(changeMatrix)
Comb15Button.on_click(changeMatrix)
Comb16Button.on_click(changeMatrix)
Comb17Button.on_click(changeMatrix)
Comb18Button.on_click(changeMatrix)
# CoverType events
CombAButton.on_click(changeMatrix)
CombBButton.on_click(changeMatrix)
CombCButton.on_click(changeMatrix)
CombDButton.on_click(changeMatrix)
CombEButton.on_click(changeMatrix)
CombFButton.on_click(changeMatrix)
CombGButton.on_click(changeMatrix)
CombHButton.on_click(changeMatrix)
CombIButton.on_click(changeMatrix)
CombJButton.on_click(changeMatrix)
CombKButton.on_click(changeMatrix)
CombLButton.on_click(changeMatrix)

printTitle()
display(main_box)
printButtonDescriptions()
