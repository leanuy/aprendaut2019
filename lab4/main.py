### DEPENDENCIAS
### ------------------

import sys
import os
import time
import matplotlib.pyplot as plt

import processing.reader as reader
from model import pca
import utils.gui as gui
from utils.const import DATA_ENCUESTAS, CANDIDATOS, MenuOps

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.PCA

    while op == MenuOps.PCA:

        gui.printMenu()
        op = gui.printMenuOption()

        if op == MenuOps.PCA:
            # Leer dataset de respuestas a encuesta
            dataset = reader.readDataset(DATA_ENCUESTAS)

            # Aplicar PCA para reducir a 2 dimensiones
            reduced = pca.pca(dataset.values, 2)

            print(reduced)

            # Graficar el resultado de PCA en 2-d
            # Valores para eje x.
            x_number_list = reduced[:, 0]

            # Valores para eje y.
            y_number_list = reduced[:, 1]

            # Graficamos los puntos en 2 dimensiones
            plt.scatter(x_number_list, y_number_list, s=1)
            plt.title("PCA a 2 Dimensiones")
            plt.show()

            input("-> Oprima enter para volver al menú")

