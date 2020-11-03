from Estado import Estado

class AFN:
    S = Estado                  #Estado inicial
    E = set ()                  #Alfabeto: conjunto de cadenas de tamaño 1
    edosAFN = set ()            #Conjunto de estados del automata
    F = set ()                  #Conjunto de estados de aceptacion
    idAFN = int
    ER = set ()

    def __init__ (self, S, E, edosAFN, F, idAFN, ER):
        self.S = S
        self.E = E
        self.edosAFN = edosAFN
        self.F = F
        self.idAFN = idAFN
        self.ER = ER

    def addEstado (self, E):
        self.edosAFN.add (E)

    @staticmethod
    def crearBasico (c):
        pass
