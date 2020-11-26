from Estado import Estado

class Transicion:
    simbolo = str
    simbolo2 = str
    edoDestino = Estado

    def __init__ (self, symb, symb2, destino):
        self.simbolo = symb
        self.simbolo2 = symb2
        self.edoDestino = destino

    def obtenerDestino (self):
        return self.edoDestino
