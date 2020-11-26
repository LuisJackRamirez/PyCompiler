
class conjuntoAFN:
    grupoAFN = set()    #aqui almacenamos los afn

    def __init__ (self, grupoAFN):
        self.grupoAFN = grupoAFN

    def clear(self):
        self.grupoAFN = set()

    def dameUnAfn(self, i):
        return self.grupoAFN[i]

    def eliminaUnAfn(self, id, conteoDeEdos):
        eliminar = self.dameUnAfn(id)
        self.grupoAFN.remove(eliminar)
        self.reescribirIdAFNsYsusEdos(1)

        return (conteoDeEdos - eliminar.cantidadDeEdos())

    def buscaAfn(self, id):
        for i in self.grupoAFN:
            if i.idAFN == id:
                return i
        return -1

    def ultimoIdAFN(self):
        return len(self.grupoAFN) + 1

    def aumentarIdEdos(self):
        contador = 1
        contador2 = 1
        for i in self.grupoAFN:
            i.idAFN = contador
            for j in i.edosAFN:
                j.identificador = contador2 - 1
                contador2 += 1
            contador += 1
        return contador2

    def reescribirIdAFNsYsusEdos(self, contador):
        contador2 = 1
        for i in self.grupoAFN:
            i.idAFN = contador
            i.actualizarIdEdos(contador2)
            contador2 += i.cantidadDeEdos()
            contador += 1
        return contador

    def cantidadDeAFN(self):
        return len(self.grupoAFN)

    def cantidadDeEdos(self):
        contador2 = 1
        for i in self.grupoAFN:
            contador2 += i.cantidadDeEdos()
        return contador2