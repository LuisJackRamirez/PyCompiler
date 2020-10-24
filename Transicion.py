from Estado import Estado

class Transicion:
    simbolo = str
    edoDestino = Estado

    def __init__ (self, symb, destino):
        self.simbolo = symb
        self.edoDestino = destino

    def obtenerDestino (self):
        return self.edoDestino
