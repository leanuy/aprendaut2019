### METODOS PRINCIPALES
### -------------------

def getParty(parsedParties, candidate):
    if candidate == 7: # Partido Nacional???
        return 6 # Partido Nacional
    if candidate == 30: # ??????
        return 0 # Frente Amplio
    for party, partyName, partyCandidates in parsedParties:
        if candidate in partyCandidates:
            return party