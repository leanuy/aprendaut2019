### DEPENDENCIAS
### ------------------
import os
import pickle

### METODOS PRINCIPALES
### -------------------

# Guarda jugador entrenado 'player' en 'filename'
def savePlayer(filename, player, from_notebook = False):
    if filename.strip():
        root = ''
        if from_notebook:
            root += '../'
        root += 'players/'
        filename = root + filename
        pickle_out = open(filename,"wb")
        pickle.dump(player, pickle_out)
        pickle_out.close()

# Carga un jugador entrenado desde 'filename'
def loadPlayer(filename, from_notebook = False):
    loaded_player = None
    if filename.strip():
        root = ''
        if from_notebook:
            root += '../'
        root += 'players/'
        filename = root + filename
        try:
            pickle_in = open(filename,"rb")
            loaded_player = pickle.load(pickle_in)
        except:
            print("Error! Archivo erroneo, por favor intente nuevamente.")
            input()
    return loaded_player

# Carga un subconjunto de jugadores en /players
def loadMassive(fileprefix, from_notebook = False):
    root = ''
    if from_notebook:
        root += '../'
    root += 'players/'

    players = []
    for filename in os.listdir(root):
        if fileprefix == '' or fileprefix in filename:
            try:
                pickle_in = open(root + filename,"rb")
                loaded_player = pickle.load(pickle_in)
                players.append(loaded_player)
            except Exception as e:
                print(str(e))
                print(f"Error al cargar archivo '{filename}'")

    return players

  