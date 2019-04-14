Para ejecutar el laboratorio, debe situarse en el mismo directorio que main.py y correr:
python main.py
Luego se le va a desplegar el siguiente menú, del cual puede elegir que acción realizar:

############################################################
#                                                          #
#        MENÚ - Laboratorio 2 (Árboles de Decisión)        #
#                                                          #
############################################################

Clasificadores actuales:

1. Entrenar
2. Clasificar
3. Evaluar
4. Mostrar
0. Salir

-> Elija una opción:

--------------------------------------------------------------------------------------------------------
Para correr varios entrenamientos de manera automática y obtener sus resultados, debe ir a la carpeta
autorun del proyecto y editar autorun.sh (en linux) o autorun.bat (en windows).

El formato de comandos a ejecutar es el siguiente:

# Para agregar códigos a correr agregan la cantidad de lineas:
# python3 automain.py dataset model continuous measure validation
# dataset = 1..2 (Iris, Covertype)
# model = 1..2 (Árbol, Bosque)
# continuous = 1..3 (Intervalos Fijos, Intervalos Variables, Maximizando Ganancia)
# measure = 1..3 (Ganancia, Ratio de Ganancia, Reducción de Impureza)
# validation = 1..2 (Validación Simple (80/20), Validación Cruzada)

Por ejemplo para ejecutar en iris(1), un bosque(2), usando intervalos fijos para atributos continuos(1),
una medida de gain ratio(2) y validación cruzada(2) debe agregar:
python automain.py 1 2 1 2 2

