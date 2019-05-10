### DEPENDENCIAS
### ------------------

import numpy as np

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

# Dado un candidato, devuelve su partido en caso de no encontrarse en parsedParties
def getParty(parsedParties, candidate):
    if candidate == 7: # Partido Nacional???
        return 6 # Partido Nacional
    if candidate == 30: # ??????
        return 0 # Frente Amplio
    for party, partyName, partyCandidates in parsedParties:
        if candidate in partyCandidates:
            return party