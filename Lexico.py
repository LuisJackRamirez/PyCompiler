import pickle
import copy
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

def checkTransicion(caracter, edoActual):
    try:
        return edoActual.read_input(caracter)
    except:
        return -1

def getToken(idEdoActual, tokens):
    for clave, valor in tokens.items():
        if idEdoActual in clave :
            #print ("valor encontrado")
            return valor
    else:
        #print ("Token no encontrado")
        return -1

def isAcceptingState(idEdoActual, prueba1):
    if idEdoActual in prueba1.final_states:
        return True
    else:
        return False

class Lexico:
    er = set()
    yyText = None
    idEdoActual = 0
    inicioLexema = 0
    indiceActual = 0
    finLexema = 0
    lastToken = -1
    edoAceptacionVisitadoPreviamente = False
    #stackInicioLex = []
    #stackFinLex = []
    stackIndiceActual = []

    estados_source = open("lexEdos.pickle", "rb")
    estados = pickle.load(estados_source)
    estados_source.close()

    alfabeto_source = open("lexAlfa.pickle", "rb")
    alfabeto = pickle.load(alfabeto_source)
    alfabeto_source.close()

    transiciones_source = open("lexTransitions.pickle", "rb")
    transiciones = pickle.load(transiciones_source)
    transiciones_source.close()

    edoInicial_source = open("lexEdoIni.pickle", "rb")
    edoInicial = pickle.load(edoInicial_source)
    edoInicial_source.close()

    finalstates_source = open("lexEdoFin.pickle", "rb")
    finalstates = pickle.load(finalstates_source)
    finalstates_source.close()

    token_soruce = open("lexToken.pickle", "rb")
    tokens = pickle.load(token_soruce)
    token_soruce.close()

    prueba1 = DFA(
        states=estados,
        input_symbols=alfabeto,
        transitions=transiciones,
        initial_state=edoInicial,
        final_states=finalstates
    )

    def __init__ (self, expresion):
        self.er = expresion

    def yylex(self):
        self.idEdoActual = 0
        self.edoAceptacionVisitadoPreviamente = False
        self.inicioLexema = self.indiceActual

        if self.indiceActual is len(self.er):
            return -1


        while self.indiceActual < len(self.er):
            siguienteEdo = checkTransicion(self.er[self.inicioLexema : self.indiceActual + 1], self.prueba1)

            if siguienteEdo != -1:
                self.idEdoActual = siguienteEdo
                self.indiceActual = self.indiceActual + 1

                if isAcceptingState(str(self.idEdoActual), self.prueba1) is True:
                    self.edoAceptacionVisitadoPreviamente = True
                    aux = self.idEdoActual[1: len(self.idEdoActual) - 1]
                    self.lastToken = int(getToken(str(aux), self.tokens))
                    self.finLexema = self.indiceActual - 1

            else:
                self.indiceActual = self.finLexema + 1
                self.stackIndiceActual.append(self.inicioLexema)
                self.yyText = self.er[self.inicioLexema: self.finLexema + 1]
                self.inicioLexema = self.indiceActual
                self.finLexema = self.indiceActual

                if self.edoAceptacionVisitadoPreviamente is False:
                    return -1
                else:
                    return self.lastToken

        if self.indiceActual == len(self.er):
            self.indiceActual = self.finLexema + 1
            self.stackIndiceActual.append(self.inicioLexema)
            self.yyText = self.er[self.inicioLexema: self.finLexema + 1]
            self.inicioLexema = self.indiceActual
            self.finLexema = self.indiceActual

            if self.edoAceptacionVisitadoPreviamente is False:
                return -1
            else:
                return self.lastToken

    def yytex(self):
        return self.yyText

    def regresarToken(self):
        self.indiceActual = self.stackIndiceActual.pop()
        self.inicioLexema = self.indiceActual
        self.finLexema= self.indiceActual