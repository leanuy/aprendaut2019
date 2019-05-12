### DEPENDENCIAS
### ------------------

import numpy as np

from utils.const import CandidateDivision

### METODOS PRINCIPALES
### -------------------

# Dada una lista de candidatos, devuelve sus respectivos partidos
# Se retorna una lista de tuplas (id, nombre, candidatos) para los partidos
# Y una lista de partidos asignados para cada candidato en 'candidates'
def parseCandidates(candidates, partyJSON):

    parties = np.zeros(len(candidates), dtype = int) 

    # Preprocesamiento
    pairs = []

    for i in range(0, len(partyJSON)):
        partyCandidates = []
        for candidate in partyJSON[i]['candidates']:
            partyCandidates.append(candidate['id'])

        pairs.append((i, partyJSON[i]['party'], partyCandidates))
    
    # Sustitucion
    index = 0
    for candidate in candidates:
        for party, partyName, partyCandidates in pairs:
            if candidate in partyCandidates:
                parties[index] = party
                index += 1
                break

    return pairs, parties

# El proceso inverso a la función anterior
def parseCandidatesFromParties(candidatesJSON, candidates):
    auxDict = {}
    for i in range(0, len(candidatesJSON)):
        auxDict[candidatesJSON[i]['id']] = candidatesJSON[i]['name']

    res = []
    for candidate in candidates:
        if not candidate in auxDict.keys():
            res.append((candidate, 'Candidato desconocido'))
        else:
            res.append((candidate, auxDict[candidate]))

    return res

# Dado un candidato, devuelve su partido en caso de no encontrarse en parsedParties
def getParty(parsedParties, candidate, division):
    if division == CandidateDivision.PARTIES:
        if candidate == 7: # Partido Nacional???
            return 6 # Partido Nacional
        if candidate == 30: # ??????
            return 0 # Frente Amplio
    elif division == CandidateDivision.SPECTRUM:
        if candidate == 7: # Partido Nacional???
            return 2 # Derecha
        if candidate == 30: # ??????
            return 0 # Izquierda
    elif division == CandidateDivision.NOLAN:
        if candidate == 7: # Partido Nacional???
            return 3 # Conservadurismo
        if candidate == 30: # ??????
            return 0 # Progresismo
    for party, partyName, partyCandidates, partyCount in parsedParties:
        if candidate in partyCandidates:
            return party