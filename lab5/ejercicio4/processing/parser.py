### DEPENDENCIAS
### ------------------

import numpy as np
import pandas as pd

from utils.const import CandidateDivision

### METODOS PRINCIPALES
### -------------------

# Dada una lista de candidatos, devuelve sus respectivos partidos
def parseCandidates(candidates, partyJSON):

    # Preprocesamiento
    parties = []
    for i in range(0, len(partyJSON)):
        partyCandidates = []
        for candidate in partyJSON[i]['candidates']:
            partyCandidates.append(candidate['id'])
        parties.append((i, partyCandidates))

    return candidates.apply(lambda x: getCandidateParty(x, parties))

# Dado un candidato, devuelve su respectivo partido
def getCandidateParty(candidate, parties):
    for party, partyCandidates in parties:
        if candidate in partyCandidates:
            return party
    return 0
