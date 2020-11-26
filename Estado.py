import copy

class Estado:
    identificador = int
    transiciones = set ()
    edoInicial = bool
    edoFinal = bool
    token = int

    def __init__ (self, identificador, transiciones, edoInicial, edoFinal, token):
        self.identificador = identificador
        self.transiciones = transiciones
        self.edoInicial = edoInicial
        self.edoFinal = edoFinal
        self.token = token

    def addTransicion(self, T):
        if self.transiciones != None:
            aux = set()
            try:
                for i in self.transiciones:
                    aux.add(i)
                aux.add(T)
            except:
                aux.add(self.transiciones)
                aux.add(T)
            self.transiciones = aux
        else:
            self.transiciones = T