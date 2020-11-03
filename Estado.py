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

    def addTransicion (self, T):
        self.transiciones.add (T)
