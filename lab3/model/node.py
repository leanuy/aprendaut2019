### DEPENDENCIAS
### ------------------

### CLASE PRINCIPAL
### -------------------

class Node:

    ### CONSTRUCTOR
    ### -------------------
    
    def __init__(self, attribute, children = None):

        # Nombre y tipo del atributo
        (self.attribute, self.attributeType) = attribute

        # Diccionario con los valores del atributo como claves
        # Si no es una hoja, 'options' tiene los nodos hijo
        # Si es una hoja, 'options' tiene los posibles valores
        if children is None:
            self.options = {}
        else:
            self.options = children

    ### METODOS AUXILIARES
    ### -------------------

    # Imprime el nodo actual y sus hijos
    def printTree(self, n):

        for x in range(0,n):
            print ('-', end="")
        print (self.attribute)

        for key, value in self.options.items():

            for x in range(0, n+1):
                print ('-', end="")
            print(key)

            if type(value) == Node:
                value.printTree(n+2)

            else:
                for x in range(0, n+2):
                    print('-', end="")
                print(value)
                