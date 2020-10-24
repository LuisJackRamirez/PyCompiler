class Estado:
    identificador = int
    transiciones = set ()
    edoInicial = bool
    edoFinal = bool
    token = int

    def __init__ (self, identif, transic, edoI, edoF, tok):
        self.identificador = identif
        self.transiciones = transic
        self.edoInicial = edoI
        self.edoFinal = edoF
        self.token = tok

    def addTransicion (self, T):
        self.transiciones.add (T)
