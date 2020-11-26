from Estado import Estado
import copy

class AFN:
    S = Estado  # Estado inicial
    E = set()  # Alfabeto: conjunto de cadenas de tamaño 1
    edosAFN = set()  # Conjunto de estados del automata
    F = set()  # Conjunto de estados de aceptacion
    idAFN = int
    ER = set()

    def __init__(self, S, E, edosAFN, F, idAFN, ER):
        self.S = S
        self.E = E
        self.edosAFN = edosAFN
        self.F = F
        self.idAFN = idAFN
        self.ER = ER

    def añadirFinal(self, edo):
        self.F = edo
        self.edosAFN.insert(len(self.edosAFN), edo)

    def añadirInicial(self, edo):
        self.S = edo
        self.edosAFN.insert(0, edo)

    def aumentarIdEdos(self):
        for i in self.edosAFN:
            i.identificador = i.identificador + 1

    def cantidadDeEdos(self):
        return len(self.edosAFN)

    def actualizarIdEdos(self, contador):
        for i in self.edosAFN:
            i.identificador = contador - 1
            contador += 1

    def convFinalesAEdos(self, transicion1):
        for i in self.edosAFN:
            if i.edoFinal == True:
                i.edoFinal = False
                i.token = 0
                if i.transiciones == None:
                    i.transiciones = transicion1
                else:
                    i.addTransicion(transicion1)

    def quitarIniciales(self):
        for i in self.edosAFN:
            if i.edoInicial == True:
                i.edoInicial = False

    def quitarFinales(self):
        for i in self.edosAFN:
            if i.edoFinal == True:
                i.edoFinal = False
                i.token = 0

    def quitarInicialesYFinales(self):
        for i in self.edosAFN:
            if i.edoInicial == True:
                i.edoInicial = False
            elif i.edoFinal == True:
                i.edoFinal = False
                i.token = 0

    def cambiarTransiciones(self, af, conteoEdos):
        aux = []
        x = copy.deepcopy(self.edosAFN)
        self.edosAFN = set()

        for i in x:
            if i.edoFinal != True:
                try:
                    for j in i.transiciones:
                        if j.edoDestino.edoFinal == True:
                            try:
                                for k in af.edosAFN:
                                    if k.edoInicial == True:
                                        j.edoDestino = k
                            except:
                                if af.edosAFN.edoInicial == True:
                                    j.edoDestino = af.edosAFN
                            conteoEdos -= 1
                except:
                    if i.transiciones.edoDestino.edoFinal == True:
                        try:
                            for k in af.edosAFN:
                                if k.edoInicial == True:
                                    i.transiciones.edoDestino = k
                        except:
                            if af.edosAFN.edoInicial == True:
                                i.transiciones.edoDestino = af.edosAFN
                        conteoEdos -= 1
                aux.insert(len(aux), i)

        for i in af.edosAFN:
            if i.edoInicial == True:
                i.edoInicial = False
            aux.insert(len(aux), i)

        self.F = af.F

        self.edosAFN = aux

        return conteoEdos
