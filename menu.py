import time
import copy
import os
import pickle
from tabulate import tabulate
from Estado import Estado
from Transicion import Transicion
from AFN import AFN
from conjuntoAFN import conjuntoAFN
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
from collections import OrderedDict
from Lexico import Lexico


def menu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    # time.sleep(2)
    print("¿Qué operación debo realizar?")
    print("\t1 - mostrar tabla de AFN's")
    print("\t2 - mostrar tabla de las transiciones de un AFN")
    print("\t3 - Crear AFN")
    print("\t4 - Unir 2 AFN")
    print("\t5 - Concatenar 2 AFN")
    print("\t6 - Cerradura transitiva de un AFN")
    print("\t7 - Cerradura de kleene de un AFN")
    print("\t8 - operación opcional de un AFN")
    print("\t9 - Unión de los AFN para el análisis léxico")
    print('\t10 - Construcción de la tabla "AFD.txt" a partir de "er.txt"')
    print("\t11 - Hacer una prueba con una cadena en un AF")
    print("\t12 - Crear AFN a partir de una expresión regular")
    print("\t13 - Crear AFN con varios símbolos ingresando el rango en ascii")
    print("\t14 - Eliminar AFN de la base de datos")
    print("\t15 - salir")

def TablaGeneral(conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AFN's por mostrar")
    else:
        ''' Cabecera de la tabla '''
        tabla = [['Id', 'Alfabeto', 'Estados', 'Estado inicial', 'Estados Finales', 'Expresión regular']]

        ''' Como hay AFN, creamos primero variables de apoyo '''
        contador = 1

        for i in conjunto.grupoAFN:
            ''' extraer id del estado inicial para la tabla '''
            Sfinal = str(i.S.identificador)

            ''' Creando variables de apoyo para cada afn, por eso están dentro del for '''
            todos = ""
            edosFinales = ""
            numTodos = []
            numFinales = []

            ''' Ciclo para saber cuales estados del AFN son finales, 
                así como para saber cuántos hay '''
            for j in i.edosAFN:
                try:
                    numTodos.append(j.identificador)
                    if j.edoFinal == True:
                        numFinales.append(j.identificador)
                except:
                    for k in j:
                        numTodos.append(k.identificador)
                        if k.edoFinal == True:
                            numFinales.append(k.identificador)

            ''' ordenando los id's para la tabla '''
            numTodos = sorted(numTodos)
            numFinales = sorted(numFinales)

            ''' pasando a string los id's de todos los estados '''
            for j in range(0, len(numTodos) - 1):
                todos += str(numTodos[j]) + ", "
            todos += str(numTodos[len(numTodos) - 1])

            ''' pasando a string los id's de los estados finales '''
            for j in range(0, len(numFinales) - 1):
                edosFinales += str(numFinales[j]) + ", "
            edosFinales += str(numFinales[len(numFinales) - 1])

            ''' Añadiendo afn a la tabla '''
            afs = [str(i.idAFN), repr(i.E), todos, Sfinal, edosFinales, str(i.ER)]
            tabla.insert(contador, afs)
            contador += 1

        ''' Imprimiendo tabla completa '''
        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def TablaAFN(id, conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AFN's por mostrar")
    else:
        ''' Cabecera de la tabla '''
        tabla = [
            ['Id del Estado', 'Transiciones (símbolo,edoDestino)', '¿Es estado inicial?', '¿Es estado Final?', 'Token']]

        ''' Como hay AFN, creamos primero variables de apoyo '''
        contador2 = 1

        ''' Obteniendo el AFN a mostrar '''
        afn = conjunto.buscaAfn(id)

        ''' Obteniendo toda la información del afn '''
        for i in afn.edosAFN:
            ''' Variable para mostrar en la tabla si un estado es inicial '''
            if i.edoInicial == True:
                var1 = "Verdadero"
            else:
                var1 = "Falso"

            ''' Variable para mostrar en la tabla si un estado es final '''
            if i.edoFinal == True:
                var2 = "Verdadero"
            else:
                var2 = "Falso"

            ''' Obteniendo transiciones '''
            ''' try = en caso de que ser más de una transición 
                except = en caso de ser una sólo transición '''
            try:
                cad = ""
                contador = 1
                for j in i.transiciones:
                    ''' Colocar una coma entre transiciones '''
                    if contador != 1:
                        cad += ","

                    ''' Comparando, si es None, es porque no contiene transiciones '''
                    if j == None:
                        afs = [str(i.identificador), "No hay transiciones", var1, var2, i.token]
                    else:
                        ''' Comparando, si la transición tiene un espacio en el símbolo, hace referencia a epsilon
                            en caso contrario, se añade el símbolo de la transición '''
                        if ord(j.simbolo) == ord(j.simbolo2):
                            if j.simbolo == " ":
                                cad2 = "Epsilon"
                            else:
                                cad2 = str(j.simbolo)
                        else:
                            cad2 = "[" + str(j.simbolo) + "-" + str(j.simbolo2) + "]"

                        ''' Creando otros datos del estado '''
                        aux3 = j.edoDestino
                        cad += "(" + cad2 + "," + str(aux3.identificador) + ")"
                    contador += 1

                afs = [str(i.identificador), cad, var1, var2, i.token]
            except:
                aux = i.transiciones

                ''' Comparando, si es None, es porque no contiene transiciones '''
                if aux == None:
                    afs = [str(i.identificador), "No hay transiciones", var1, var2, i.token]
                else:
                    ''' Comparando, si la transición tiene un espacio en el símbolo, hace referencia a epsilon
                        en caso contrario, se añade el símbolo de la transición '''
                    if ord(aux.simbolo) == ord(aux.simbolo2):
                        if aux.simbolo == " ":
                            cad2 = "Epsilon"
                        else:
                            cad2 = str(aux.simbolo)
                    else:
                        cad2 = "[" + str(aux.simbolo) + "-" + str(aux.simbolo2) + "]"

                    ''' Creando otros datos del estado '''
                    aux2 = aux.edoDestino
                    cad = "(" + cad2 + "," + str(aux2.identificador) + ")"
                    afs = [str(i.identificador), cad, var1, var2, i.token]

            ''' Añadiendo estado con sus transiciones a la tabla '''
            tabla.insert(contador2, afs)
            contador2 += 1

        ''' Imprimiendo la tabla completa '''
        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def Crear(symbol, symbol2, token, conjunto, conteoDeEdos, numCrear):
    try:
        if ((symbol >= 33 and symbol <= 91) or (symbol >= 93 and symbol <= 126)) and symbol < symbol2:
            alfa = chr(symbol)
            for i in range(symbol + 1, symbol2 + 1):
                alfa += ", " + chr(i)
            car = "[" + chr(symbol) + "-" + chr(symbol2) + "]"
        elif ((symbol2 >= 33 and symbol2 <= 91) or (symbol2 >= 93 and symbol2 <= 126)) and symbol2 < symbol:
            alfa = chr(symbol2)
            for i in range(symbol2 + 1, symbol + 1):
                alfa += ", " + chr(i)
            car = "[" + chr(symbol2) + "-" + chr(symbol) + "]"
        else:
            car = chr(symbol)
            alfa = chr(symbol)

        x1 = Estado(conteoDeEdos + 1, None, False, True, token)
        transicion1 = Transicion(chr(symbol), chr(symbol2), x1)
        x = Estado(conteoDeEdos, transicion1, True, False, -1)
        edos = [x, x1]
    except:
        x1 = Estado(conteoDeEdos + 1, None, False, True, token)
        transicion1 = Transicion(symbol, symbol2, x1)
        x = Estado(conteoDeEdos, transicion1, True, False, -1)

        edos = [x, x1]
        if ord(symbol) != ord(symbol2):
            if (ord(symbol) >= 65 and ord(symbol) <= 90 and ord(symbol2) >= 65 and ord(symbol2) <= 90) or \
                    (ord(symbol) >= 97 and ord(symbol) <= 122 and ord(symbol2) >= 97 and ord(symbol2) <= 122) or \
                    (ord(symbol) >= 48 and ord(symbol) <= 57 and ord(symbol2) >= 48 and ord(symbol2) <= 57):
                if ord(symbol) < ord(symbol2):
                    alfa = symbol
                    for i in range(ord(symbol) + 1, ord(symbol2) + 1):
                        alfa += ", " + chr(i)
                    car = "[" + symbol + "-" + symbol2 + "]"
                else:
                    alfa = symbol2
                    for i in range(ord(symbol2) + 1, ord(symbol) + 1):
                        alfa += ", " + chr(i)
                    car = "[" + symbol2 + "-" + symbol + "]"
            elif ord(symbol) == 92 and \
                    ((ord(symbol2) >= 33 and ord(symbol2) <= 91) or (ord(symbol2) >= 93 and ord(symbol2) <= 126)):
                alfa = chr(92) + symbol2
                alfa = "".join(OrderedDict.fromkeys(alfa))
                car = chr(92) + symbol2
            else:
                return -1
        else:
            car = symbol
            alfa = symbol

    ''' Revisar si "conjunto" tiene estados o no '''
    if conjunto.grupoAFN != None:
        ''' "conjunto" tiene estados, por tanto se añade al final el nuevo AFN '''
        conjunto.grupoAFN.insert(numCrear, AFN(x, alfa, edos, x1, 1 + numCrear, car))
    else:
        ''' "conjunto" no tiene estados, por tanto se añade al principio '''
        conjunto.grupoAFN = [AFN(x, alfa, edos, x1, 1 + numCrear, car)]

    return 0

def Unir(id1, id2, conjunto, token):
    ''' Obteniendo los afn a unir '''
    af1 = conjunto.buscaAfn(id1)
    af2 = conjunto.buscaAfn(id2)

    ''' Obteniendo la cantidad de estados que tienen los 2 afn '''
    tam = len(af1.edosAFN)
    tam2 = len(af2.edosAFN)

    ''' Eliminando los afn del grupo de afn '''
    conjunto.grupoAFN.remove(af1)
    conjunto.grupoAFN.remove(af2)

    ''' Creando variables de apoyo '''
    contador2 = 1

    ''' Actualizando los id de todos los afn '''
    contador = conjunto.aumentarIdEdos()

    ''' creando el estado inicial "x" de la operación unión '''
    transicion1 = [Transicion(" ", " ", af1.S), Transicion(" ", " ", af2.S)]
    x = Estado(contador - 1, transicion1, True, False, -1)

    ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
    noms = []
    noms.insert(contador2 - 1, x)
    contador2 += 1
    contador += 1

    ''' creando el estado final '''
    x1 = Estado(tam + tam2 + contador - 1, None, False, True, token)

    transicion1 = Transicion(" ", " ", x1)

    ''' Actualizando en el af1 los edos y quitando los edos iniciales y finales '''
    af1.actualizarIdEdos(contador)
    af1.convFinalesAEdos(transicion1)
    af1.quitarInicialesYFinales()

    ''' Añadiendo af1 a noms '''
    for i in af1.edosAFN:
        noms.insert(contador2, i)
        contador2 += 1
        contador += 1

    ''' Actualizando en el af2 los edos y quitando los edos iniciales y finales '''
    af2.actualizarIdEdos(contador)
    af2.convFinalesAEdos(transicion1)
    af2.quitarInicialesYFinales()

    ''' Añadiendo af2 a noms '''
    for i in af2.edosAFN:
        noms.insert(contador2, i)
        contador2 += 1
        contador += 1

    ''' Añadiendo el edo final a noms '''
    noms.insert(contador2, x1)

    ''' Definiendo el alfabeto de noms, juntando el de af1 y af2 
        el ciclo for es para revisar que las letras del alfabeto 
        af2 no se encuentren ya en el alfabeto para noms'''
    symbol = af1.E
    flag = 0
    for i in range(0, len(af2.E)):
        for j in range(0, len(symbol)):
            if (af2.E[i] == symbol[j]):
                flag = 1
        if flag == 0:
            symbol += ", " + af2.E[i]
        flag = 0

    ''' Definiendo la expresión regular del afn '''
    if len(af1.ER) == 1 and len(af2.ER) == 1:
        er = af1.ER + " or " + af2.ER
    elif len(af1.ER) != 1 and len(af2.ER) == 1:
        er = "(" + af1.ER + ")" + " or " + af2.ER
    elif len(af1.ER) == 1 and len(af2.ER) != 1:
        er = af1.ER + " or " + "(" + af2.ER + ")"
    else:
        er = "(" + af1.ER + ")" + " or " + "(" + af2.ER + ")"

    ''' Añadiendo el nuevo AFN a "conjunto" '''
    idAFN = conjunto.ultimoIdAFN()
    conjunto.grupoAFN.insert(len(conjunto.grupoAFN), AFN(x, symbol, noms, x1, idAFN, er))


def CerrKleene(id1, conjunto, conteoDeEdos, token):
    '''Función que transforma el AFN a la operación Cerradura de Kleene'''
    af1 = operacionTransitiva(id1, conjunto, conteoDeEdos, token)
    if af1 == -1:
        return -1

    af1.S.addTransicion(Transicion(" ", " ", af1.F))

    # Cambiando la expresion regular
    ex = "(" + str(af1.ER) + ")*"
    af1.ER = ex


def operacionTransitiva(id1, conjunto, conteoDeEdos, token):
    '''Función que transforma el AFN a la operación Cerradura Transitiva'''

    # buscando el afn
    af1 = conjunto.buscaAfn(id1)

    if af1 == None:
        return -1

    conjunto.grupoAFN.remove(af1)
    conteoDeEdos -= af1.cantidadDeEdos()

    contador = 1

    contador = conjunto.reescribirIdAFNsYsusEdos(contador)
    contador2 = conjunto.cantidadDeEdos()

    af1.idAFN = contador
    af1.actualizarIdEdos(contador2)
    contador2 += af1.cantidadDeEdos()

    # Creación de los estados requeridos para la cerradura Transitiva
    x = Estado(af1.S.identificador, None, True, False, -1)
    x1 = Estado(contador2, None, False, True, token)

    # Creada la transición épsilon para x
    x.addTransicion(Transicion(" ", " ", af1.S))

    # Añadir la transición épsilon hacia x1 a los estados
    # finales, y de regreso al estado inicial
    y = [Transicion(" ", " ", af1.S), Transicion(" ", " ", x1)]
    af1.convFinalesAEdos(y)

    # Aumentando el id de todos los estados para añadir el inicial
    af1.quitarIniciales()
    af1.aumentarIdEdos()

    # Finalmente, adición de los nuevos estados al AFN,
    # y modificación del estado inicial y final
    af1.añadirInicial(x)
    af1.añadirFinal(x1)

    conjunto.grupoAFN.insert(len(conjunto.grupoAFN), af1)

    return af1


def CerrTransitiva(id1, conjunto, conteoDeEdos, token):
    '''Función que transforma el AFN a la operación Cerradura de Kleene'''
    af1 = operacionTransitiva(id1, conjunto, conteoDeEdos, token)
    if af1 == -1:
        return -1

    # Cambiando la expresion regular
    ex = "(" + str(af1.ER) + ")+"
    af1.ER = ex


def Concatenar(id1, id2, conjunto, conteoDeEdos):
    '''Función que realiza la operación concatenar con dos AFNs
       Recibe los ids de los AFN, el conjunto de AFN, y el contador de AFN creados'''
    af1 = conjunto.buscaAfn(id1)
    af2 = conjunto.buscaAfn(id2)

    if af1 == -1 or af2 == -1:
        return -1

    conjunto.grupoAFN.remove(af1)
    conjunto.grupoAFN.remove(af2)

    contador = 1
    contador = conjunto.reescribirIdAFNsYsusEdos(contador)
    contador2 = conjunto.cantidadDeEdos()

    af1.idAFN = contador
    af1.actualizarIdEdos(contador2)
    contador2 += af1.cantidadDeEdos()

    af2.actualizarIdEdos(contador2 - 1)

    conteoDeEdos = af1.cambiarTransiciones(af2, conteoDeEdos)

    '''Aquí unimos los dos alfabetos y eliminamos los caracteres repetidos'''
    symbol = af1.E
    flag = 0
    for i in range(0, len(af2.E)):
        for j in range(0, len(symbol)):
            if (af2.E[i] == symbol[j]):
                flag = 1
        if flag == 0:
            symbol += ", " + af2.E[i]
        flag = 0
    af1.E = symbol

    # Cambiando la expresion regular
    ex = "(" + str(af1.ER) + ")&(" + str(af2.ER) + ")"
    af1.ER = ex

    conjunto.grupoAFN.insert(len(conjunto.grupoAFN), af1)

    return conteoDeEdos


def Opcional(id1, conjunto, conteoDeEdos, token):
    '''Función que transforma el AFN a la operación Opcional'''
    af1 = conjunto.buscaAfn(id1)

    if af1 == -1:
        return -1

    conjunto.grupoAFN.remove(af1)

    contador = 1
    contador = conjunto.reescribirIdAFNsYsusEdos(contador)
    contador2 = conjunto.cantidadDeEdos()

    af1.idAFN = contador
    var = contador2 - 1
    af1.actualizarIdEdos(contador2)
    contador2 += af1.cantidadDeEdos()

    x = Estado(var, set(), True, False, -1)
    x1 = Estado(conteoDeEdos + 1, None, False, True, token)

    conteoDeEdos += 2

    # Creada la transición epsilon para x
    x.addTransicion(Transicion(" ", " ", af1.S))
    x.addTransicion(Transicion(" ", " ", x1))

    # Añadir la transición épsilon hacia x1 a los estados
    # finales, y de regreso al estado inicial
    y = Transicion(" ", " ", x1)
    af1.convFinalesAEdos(y)

    # Aumentando el id de todos los estados para añadir el inicial
    af1.quitarIniciales()
    af1.aumentarIdEdos()

    # Finalmente, adición de los nuevos estados al AFN,
    # y modificación del estado inicial y final
    af1.añadirInicial(x)
    af1.añadirFinal(x1)

    # Cambiando la expresion regular
    ex = "(" + str(af1.ER) + ")?"
    af1.ER = ex

    conjunto.grupoAFN.insert(len(conjunto.grupoAFN), af1)


def prepararAnalisis(conjunto):
    if len(conjunto.grupoAFN) <= 1:
        print("No se puede realizar la unión, hay menos de 2 AFN en la base de datos")
        time.sleep(1)
    else:
        contador = 1
        transicion1 = []

        ''' Añadiendo el estado inicial "x" de la operación unión '''
        for i in conjunto.grupoAFN:
            i.aumentarIdEdos()
            for j in i.edosAFN:
                if j.edoInicial == True:
                    transicion1 += [Transicion(" ", " ", j)]

        x = Estado(0, transicion1, True, False, -1)
        ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
        noms = []
        auxFinal = []
        noms.insert(contador - 1, x)
        contador += 1
        contador3 = 1

        ''' Sacando cada estado de los afn para modificarlos, cambiando sus transiciones '''
        symbol = (conjunto.buscaAfn(1)).E
        er = ""

        for i in conjunto.grupoAFN:
            ''' Definiendo el alfabeto de noms '''
            flag = 0
            for j in range(0, len(i.E)):
                for k in range(0, len(symbol)):
                    if (i.E[j] == symbol[k]):
                        flag = 1
                if flag == 0:
                    symbol += ", " + i.E[j]
                flag = 0

            i.quitarIniciales()
            for j in i.edosAFN:
                if j.edoFinal == True:
                    auxFinal.insert(contador3, j)
                    contador3 += 1
                noms.insert(contador, j)
                contador += 1

            ''' Definiendo la expresión regular del afn final '''
            if er != "":
                er += " or " + "(" + i.ER + ")"
            else:
                er = "(" + i.ER + ")"

        conjunto.grupoAFN.clear()

        ''' Añadiendo el nuevo AFN a "conjunto.con" '''
        conjunto.grupoAFN.insert(contador - 1, AFN(x, symbol, noms, auxFinal, 1, er))

def afn_AFD(idA, conjunto, bandera):
    if idA in afn_api.keys() and idA not in afn_convertidos:
        afn = afn_api[idA].copy()
    else:
        afn = conjunto.buscaAfn(idA)

        edosId = set()
        edosfinales = set()
        edosinicial = set()
        ##Obtener transiciones
        dictrans = {}
        alfabeto = set()
        estadoinicial = ""
        for i in afn.edosAFN:
            # print(str(i.identificador))
            if (i.edoInicial == True):

                edosinicial.add(str(i.identificador))
                estadoinicial = str(i.identificador)
                if (len(edosinicial) > 1):
                    try:
                        os.system("cls")
                    except:
                        os.system("clear")
                    print("ERROR, HAY MAS DE UN ESTADO INICIAL")
                    print("ESTADOS INICIALES: " + str(edosinicial))

                    break
            if (i.edoFinal == True):
                edosfinales.add(str(i.identificador))
                agregarTokenEstado(str(i.identificador), str(i.token))
                ##agregardiccionario('',i.identificador)
            edosId.add(str(i.identificador))
            try:
                for j in i.transiciones:
                    var1 = str(j.simbolo)
                    var2 = str(j.simbolo2)
                    var3 = str(j.edoDestino.identificador)
                    elements_transiciones = elementos_transiciones(var1, var2)
                    for letra in elements_transiciones:

                        agregardiccionario(letra, var3)
                        if letra not in alfabeto:
                            if letra != '':
                                alfabeto.add(letra)

                dictrans[str(i.identificador)] = devolverdiccionario()

            except:

                auxtran = i.transiciones
                if auxtran == None:
                    agregardiccionario('', str(i.identificador))
                    dictrans[str(i.identificador)] = devolverdiccionario()
                else:
                    elements_transiciones = elementos_transiciones(str(auxtran.simbolo), str(auxtran.simbolo2))
                    for letra in elements_transiciones:
                        agregardiccionario(letra, str(auxtran.edoDestino.identificador))
                        if letra not in alfabeto:
                            if letra != '':
                                alfabeto.add(letra)
                    dictrans[str(i.identificador)] = devolverdiccionario()

        afn = NFA(
            states=edosId,
            input_symbols=alfabeto,
            transitions=dictrans,
            initial_state=estadoinicial,
            final_states=edosfinales
        )
        afn_api[idA] = afn
    afd = DFA.from_nfa(afn)
    transicionesafd = afd.transitions.copy()
    if bandera == 1:
        return afn
    else:
        pass
    #print("¿CONVERSION CORRECTA?")
    #print(afd.validate())
    # print(str(devolverTokens()))
    transicionesafd = afd.transitions.copy()
    diccionario_tokens = devolverTokens()
    a_borar = []
    for clave,valor in afd.transitions.items():
        if valor == '{}' or clave == '{}' or valor == None or clave == None or len(afd.transitions[clave])==0:
            try:
                del transicionesafd[clave]
                continue
            except:
                pass
        for j,h in valor.items():
            if h == '{}' or h == None or j == '{}':
                a_borar.append(j)
        for k in a_borar:
            try:
                del transicionesafd[clave][k]
            except:
                continue
        a_borar.clear()
    '''for clave in afd.transitions.keys():
        if clave == None or clave == '{}':
            try:
                del transicionesafd[clave]
            except:
                pass'''
    afd_api[idA] = afd
    archivoAFD = open("AFD.txt", "w")
    archivoAFD.write("ESTADOS              :" + str(afd.states).replace("'{}',", '').replace(",'{}'", '') + "\n")
    archivoAFD.write("SIMBOLOS DE ENTRADA  :" + str(afd.input_symbols).replace("'}'}, '{'", "}'}, '{\n") + "\n")
    archivoAFD.write("TRANSICIONES         :" + str(transicionesafd) + "\n")
    archivoAFD.write("ESTADO INICIAL       :" + str(afd.initial_state) + "\n")
    archivoAFD.write("ESTADO(S) FINAL(ES)  :" + str(afd.final_states) + "\n")
    archivoAFD.write("TOKENS (CLAVE, VALOR):" + str(diccionario_tokens))
    archivoAFD.close()
    # VAMONOS CON RICK
    estados_rick = open("estados.pickle", "wb")
    #estados_rick = open("lexEdos.pickle", "wb")
    pickle.dump(afd.states, estados_rick)
    estados_rick.close()

    alfabeto_rick = open("alfabeto.pickle", "wb")
    #alfabeto_rick = open("lexAlfa.pickle", "wb")
    pickle.dump(afd.input_symbols, alfabeto_rick)
    alfabeto_rick.close()

    transiciones_rick = open("transiciones.pickle", "wb")
    #transiciones_rick = open("lexTransitions.pickle", "wb")
    pickle.dump(afd.transitions, transiciones_rick)
    transiciones_rick.close()

    edoInicial_rick = open("edosInicial.pickle", "wb")
    #edoInicial_rick = open("lexEdoIni.pickle", "wb")
    pickle.dump(afd.initial_state, edoInicial_rick)
    edoInicial_rick.close()

    edosFinales_rick = open("edosFinales.pickle", "wb")
    #edosFinales_rick = open("lexEdoFin.pickle", "wb")
    pickle.dump(afd.final_states, edosFinales_rick)
    edosFinales_rick.close()

    tokens_rick = open("token.pickle", "wb")
    #tokens_rick = open("lexToken.pickle", "wb")
    pickle.dump(diccionario_tokens, tokens_rick)
    tokens_rick.close()


def agregarTokenEstado(key, valor):
    if key in diccionario_estados:
        print("YA EXISTE ESE VALOR, COMPROBAR OPERACIONES")
        exit()
    else:
        diccionario_estados[key] = valor


def devolverTokens():
    auxiliar_nuevo = diccionario_estados.copy()
    diccionario_estados.clear()
    return auxiliar_nuevo


def agregardiccionario(key, valor):
    mas_transiciones.add(valor)
    diccionarioauxiliar[key] = mas_transiciones.copy()


def devolverdiccionario():
    aux = diccionarioauxiliar.copy()
    diccionarioauxiliar.clear()
    mas_transiciones.clear()
    ##print (str (aux))
    return aux


def elementos_transiciones(valor1, valor2):
    if valor1 == " " and valor2 == " ":
        valor = ''
        lista_alfabeto.append(valor)
    elif valor2 == "" or valor2 == None and valor1 != None and valor1 != "":
        lista_alfabeto.append(valor1)
    elif valor2 == " " and valor1 != None and valor1 != " ":
        lista_alfabeto.append(valor1)
        valor2 = ''
        lista_alfabeto.append(valor2)
    elif valor1 == " " and valor2 != None and valor2 != '':
        lista_alfabeto.append(valor2)
        valor1 = ""
        lista_alfabeto.append(valor1)
    elif valor1 == "" or valor1 == None and valor2 != None and valor2 != '':
        lista_alfabeto.append(valor2)
    else:
        if ord(valor2) > ord(valor1):
            for i in range(ord(valor1), ord(valor2) + 1):
                lista_alfabeto.append(chr(i))
        elif ord(valor1) == ord(valor2):
            lista_alfabeto.append(valor1)
        else:
            for i in range(ord(valor2), ord(valor1) + 1):
                lista_alfabeto.append(chr(i))

    aux = lista_alfabeto.copy()

    lista_alfabeto.clear()
    return aux


def crearConjunto(valor):
    mas_transiciones.add(valor)


def devolverConjunto():
    aux = mas_transiciones.copy()
    mas_transiciones.clear()
    return aux


def comprobar_AFN(idA, conjunto2, cadena):
    bandera = 1
    afn_comprbacion = afn_AFD(idA, conjunto2, bandera).copy()

    try:
        if afn_comprbacion.accepts_input(cadena):
            print("cadena aceptada")
        else:
            print("cadena no aceptada")
    except:
        print("cadeno aceptada")


def E(conjunto2, tk):
    if T(conjunto2, tk):
        if Ep(conjunto2, tk):
            return True
    return False


def Ep(conjunto2, tk):
    global conteoDeEdos2
    global numCrear2
    token = lexic.yylex()
    if token == 10:  # OR de unir
        if T(conjunto2, tk):
            Unir(len(conjunto2.grupoAFN) - 1, len(conjunto2.grupoAFN), conjunto2, tk)
            numCrear2 -= 1
            conteoDeEdos2 += 2
            if Ep(conjunto2, tk):
                return True
        return False
    lexic.regresarToken()
    return True


def T(conjunto2, tk):
    if C(conjunto2, tk):
        if Tp(conjunto2, tk):
            return True
    return False


def Tp(conjunto2, tk):
    global conteoDeEdos2
    global numCrear2
    token = lexic.yylex()
    if token == 20:  # & de Concatenar
        if C(conjunto2, tk):
            conteoDeEdos2 = Concatenar(len(conjunto2.grupoAFN) - 1, len(conjunto2.grupoAFN), conjunto2, conteoDeEdos2)
            numCrear2 -= 1
            if Tp(conjunto2, tk):
                return True
        return False
    lexic.regresarToken()
    return True


def C(conjunto2, tk):
    if F(conjunto2, tk):
        if Cp(conjunto2, tk):
            return True
    return False


def Cp(conjunto2, tk):
    global conteoDeEdos2
    token = lexic.yylex()
    if token == 30:  # + de cerradura transitiva
        CerrTransitiva(len(conjunto2.grupoAFN), conjunto2, conteoDeEdos2, tk)
        conteoDeEdos2 += 2
        if Cp(conjunto2, tk):
            return True
        return False
    elif token == 40:  # * de cerradura de kleene
        CerrKleene(len(conjunto2.grupoAFN), conjunto2, conteoDeEdos2, tk)
        conteoDeEdos2 += 2
        if Cp(conjunto2, tk):
            return True
        return False
    elif token == 50:  # ? de opcional
        Opcional(len(conjunto2.grupoAFN), conjunto2, conteoDeEdos2, tk)
        conteoDeEdos2 += 2
        if Cp(conjunto2, tk):
            return True
        return False

    lexic.regresarToken()
    return True


def F(conjunto2, tk):
    global conteoDeEdos2
    global numCrear2
    token1 = lexic.yylex()
    if token1 == 60:  # ( de paréntesis izquierdo
        if E(conjunto2, tk):
            token1 = lexic.yylex()
            if token1 == 70:  # ) de paréntesis derecho
                return True
        return False
    elif token1 == 80:  # [ de corchete izquierdo
        token1 = lexic.yylex()
        if token1 == 90:  # símbolos de letras o números
            lexema1 = lexic.yytex()
            token1 = lexic.yylex()
            if token1 == 100:  # - de guión
                token1 = lexic.yylex()
                if token1 == 90:  # símbolos de letras o números
                    lexema2 = lexic.yytex()
                    token1 = lexic.yylex()
                    if token1 == 110:  # ] de corchete derecho
                        Crear(lexema1, lexema2, tk, conjunto2, conteoDeEdos2, numCrear2)
                        numCrear2 += 1
                        conteoDeEdos2 += 2
                        return True
        return False
    elif token1 == 90:
        lexema1 = lexic.yytex()
        Crear(lexema1, lexema1, tk, conjunto2, conteoDeEdos2, numCrear2)
        numCrear2 += 1
        conteoDeEdos2 += 2
        return True
    elif token1 == 120: #simbolo de \
        token1 = lexic.yylex()
        if (token1 >= 20 and token1 <= 110) or token1 == 130:  # símbolos de letras o números o cualquier caracter
            lexema1 = lexic.yytex()
            Crear(chr(92), lexema1, tk, conjunto2, conteoDeEdos2, numCrear2)
            numCrear2 += 1
            conteoDeEdos2 += 2
            return True

    return False


diccionario_estados = {}
lista_alfabeto = []
mas_transiciones = set()
afn_convertidos = []
diccionarioauxiliar = {}
afd_api = {}
afn_api = {}
dictrans = {}
conjunto = conjuntoAFN(None)
numCrear = 0
numCrear2 = 0
conteoDeEdos = 0
conteoDeEdos2 = 0
print("\n¡Hola!, Bienvenido al programa de análisis léxico")

while True:
    menu()
    opcionMenu = input("")

    if opcionMenu == "1":
        TablaGeneral(conjunto, numCrear)
        time.sleep(1)

    elif opcionMenu == "2":
        try:
            print("\nPara mostrar la tabla de un AFN, escribe el id del AFN:")
            num = int(input(""))
            TablaAFN(num, conjunto, numCrear)
            time.sleep(1)
        except:
            print("No se encontró la ID de dicho autómata\n")

    elif opcionMenu == "3":
        try:
            print("\nPara crear el AFN, escribe el carácter(es) al cual crearle el AFN:")
            symbol = str(input(""))
            print("\nAhora escribe su token (0 en adelante):")
            token = int(input(""))
            if token < 0:
                print("\nNo es un token válido")
            else:
                if (len(symbol) == 1) or (ord(symbol[0]) == 92 and len(symbol) == 2):
                    if len(symbol) == 2:
                        error = Crear(symbol[0], symbol[1], token, conjunto, conteoDeEdos, numCrear)
                    else:
                        error = Crear(symbol[0], symbol[0], token, conjunto, conteoDeEdos, numCrear)
                    if error != -1:
                        conteoDeEdos += 2
                        numCrear += 1
                        print("creando AFN...")
                        time.sleep(1)
                        print("¡AFN creado con éxito!\n")
                    else:
                        print("Error, el rango no tiene la estructura adecuada")
                        time.sleep(1)
                        print("(puras mayúsculas, minúsculas o números)")
                        time.sleep(1)
                elif symbol[0] == '[' and len(symbol) == 5:
                    if symbol[2] == '-' and symbol[4] == ']':
                        error = Crear(symbol[1], symbol[3], token, conjunto, conteoDeEdos, numCrear)
                        if error != -1:
                            conteoDeEdos += 2
                            numCrear += 1
                            print("creando AFN...")
                            time.sleep(1)
                            print("¡AFN creado con éxito!\n")
                        else:
                            print("Error, el rango no tiene la estructura adecuada")
                            time.sleep(1)
                            print("(puras mayúsculas, minúsculas o números)")
                            time.sleep(1)
                    else:
                        print("El rango que ingresaste no tiene la estructura adecuada (ej. [a-z],[0-9])\n")
                else:
                    print("El rango que ingresaste no tiene la estructura adecuada (ej. [a-z],[0-9])\n")
            time.sleep(1)
        except:
            print("Error, datos incorrectos\n")
            time.sleep(1)

    elif opcionMenu == "4":
        try:
            print("\nIngresa el id del primer AFN a unir:")
            id1 = int(input(""))
            print("\nIngresa el id del segundo AFN a unir:")
            id2 = int(input(""))
            print("\nIngresa el nuevo valor del token del estado de aceptación:")
            token = int(input(""))
            if token > 0:
                Unir(id1, id2, conjunto, token)
                numCrear -= 1
                conteoDeEdos += 2
                print("uniendo AFN...")
                print("¡Nuevo AFN creado con éxito!\n")
            else:
                print("No es un token válido\n")
            time.sleep(1)
        except:
            print("No se encontró la ID de dichos autómatas\n")

    elif opcionMenu == "5":
        try:
            print("\nIngresa el id del primer AFN a concatenar:")
            id1 = int(input(""))
            print("\nIngresa el id del segundo AFN a concatenar:")
            id2 = int(input(""))
            a = Concatenar(id1, id2, conjunto, conteoDeEdos)
            if a == -1:
                print("No se encontró la ID de dichos autómatas\n")
            else:
                print("concatenando AFN...")
                time.sleep(1)
                print("¡Nuevo AFN creado con éxito!\n")
                numCrear -= 1
                conteoDeEdos = a
        except:
            print("Error en la concatenación de autómatas\n")

    elif opcionMenu == "6":
        print("\nIngresa el id del AFN al cual obtener la cerradura transitiva:")
        id1 = int(input(""))
        print("\nIngresa el nuevo valor del token del estado de aceptación:")
        token = int(input(""))
        if token > 0:
            a = CerrTransitiva(id1, conjunto, conteoDeEdos, token)
            if a == -1:
                print("No se encontró el AFN\n")
            else:
                print("obteniendo cerradura transitiva...")
                time.sleep(1)
                print("¡Nuevo AFN creado con éxito!\n")
                conteoDeEdos += 2
        else:
            print("No es un token válido\n")
        time.sleep(1)

    elif opcionMenu == "7":
        print("\nIngresa el id del AFN al cual obtener la cerradura de kleene:")
        id1 = int(input(""))
        print("\nIngresa el nuevo valor del token del estado de aceptación:")
        token = int(input(""))
        if token > 0:
            a = CerrKleene(id1, conjunto, conteoDeEdos, token)
            if a == -1:
                print("No se encontró el AFN\n")
            else:
                print("obteniendo cerradura de kleene...")
                time.sleep(1)
                print("¡Nuevo AFN creado con éxito!\n")
                conteoDeEdos += 2
        else:
            print("No es un token válido\n")
        time.sleep(1)

    elif opcionMenu == "8":
        print("\nIngresa el id del AFN al cual obtener la operación opcional:")
        id1 = int(input(""))
        print("\nIngresa el nuevo valor del token del estado de aceptación:")
        token = int(input(""))
        if token > 0:
            a = Opcional(id1, conjunto, conteoDeEdos, token)

            if a == -1:
                print("No se encontró el AFN\n")
            else:
                print("obteniendo operación opcional...")
                time.sleep(1)
                print("¡Nuevo AFN creado con éxito!\n")
                conteoDeEdos += 2
        else:
            print("No es un token válido\n")
        time.sleep(1)

    elif opcionMenu == "9":
        try:
            print("\nTodos los AFN del sistema se van a unir, ¿Deseas continuar? (S/N)")
            resp = str(input(""))[0]
            if resp == "S" or resp == "s":
                prepararAnalisis(conjunto)
                print("uniendo AFN...")
                time.sleep(1)
                print("¡Nuevo AFN creado con éxito!\n")
                conteoDeEdos += 1
                numCrear = 1
            else:
                time.sleep(1)
        except:
            print("Error, esa no es una respuesta válida\n")

    elif opcionMenu == "10":
        lista = []
        with open ("ER.txt", "r") as f:
            for i in f:
                if i != '\n':
                    lista.append(i)
        f.close()

        if len(lista) != 0:
            for i in lista:
                cad = i
                cad = cad.lstrip()
                cad = cad.rstrip()

                aux = ""
                flag = 0
                er = ""

                try:
                    indice = "".join(cad).rindex(' ')
                    for i in range(indice + 1, len(cad)):
                        aux += cad[i]

                    er = cad[0: indice].replace(' ', '')
                    tk = int(aux)

                    lexic = Lexico(er)

                    numCrear2 = 0
                    conteoDeEdos2 = 0
                    conjunto2 = conjuntoAFN(None)
                    result = E(conjunto2, tk)
                except:
                    print("Error, una de las expresiones del txt que ingresaste es errónea\n")
                    time.sleep(1)
                    result = False

                if result == False:
                    break
                else:
                    if conjunto.grupoAFN != None:
                        conjunto.grupoAFN.insert(numCrear, copy.deepcopy(conjunto2.grupoAFN.pop()))
                    else:
                        conjunto.grupoAFN = copy.deepcopy(conjunto2.grupoAFN)
                    numCrear += 1
                    conteoDeEdos += conteoDeEdos2
                    conjunto.reescribirIdAFNsYsusEdos(1)

            if result == True:
                prepararAnalisis(conjunto)
                afn_convertidos.append(1)
                afn_AFD(1, conjunto, 0)
                print("¡Nuevo AFD creado con éxito!\n")
                time.sleep(1)
            else:
                print('Error, una de las expreiones de "ER.txt" no contiene token o no contiene expresión regular\n')
                time.sleep(1)
        else:
            print('Error, el archivo "ER.txt" se encuentra vacío\n')
            time.sleep(1)

    elif opcionMenu == "11":
        print("\nIngresa el id del AF a introducir una cadena:")
        idA = int(input())
        print("Ingresa la cadena a comprobar")
        cadena = input()
        comprobar_AFN(idA, conjunto, cadena)
        time.sleep(1)
        print("¡Prueba concluida con éxito!\n")

    elif opcionMenu == "12":
        print("\nPara crear el AFN, escribe la expresión regular:")
        cad = str(input(""))
        cad = cad.lstrip()
        cad = cad.rstrip()

        aux = ""
        flag = 0
        er = ""

        try:
            indice = "".join(cad).rindex(' ')
            for i in range(indice + 1, len(cad)):
                aux += cad[i]

            er = cad[0: indice].replace(' ', '')
            tk = int(aux)

            lexic = Lexico(er)

            conjunto2 = conjuntoAFN(None)
            result = E(conjunto2, tk)
        except:
            print("Error, la er que ingresaste es errónea\n")
            time.sleep(1)
            result = False

        if result == False:
            print("No se pudo crear el AFN\n")
        else:
            if conjunto.grupoAFN != None:
                conjunto.grupoAFN.insert(numCrear, copy.deepcopy(conjunto2.grupoAFN.pop()))
            else:
                conjunto.grupoAFN = copy.deepcopy(conjunto2.grupoAFN)
            numCrear += 1
            # conteoDeEdos += conjunto2.grupoAFN.cantidadDeEdos()
            print("creando AFN...")
            time.sleep(1)
            print("¡AFN creado con éxito!\n")
        time.sleep(1)

    elif opcionMenu == "13":
        print("\nPara crear el AFN, escribe el primer valor en ascii:")
        cad = int(input(""))
        print("\nAhora escribe el segundo valor en ascii:")
        cad2 = int(input(""))
        print("\nAhora escribe su token (0 en adelante):")
        token = int(input(""))
        if token < 0:
            print("\nNo es un token válido\n")
        elif cad < 33 or cad > 126 or cad2 < 33 or cad2 > 126 or cad == 92 or cad2 == 92:
            print("\nNo son valores de ascii que se puedan usar para crear un AFN\n")
        else:
            error = Crear(cad, cad2, token, conjunto, conteoDeEdos, numCrear)
            conteoDeEdos += 2
            numCrear += 1
            print("creando AFN...")
            time.sleep(1)
            print("¡AFN creado con éxito!\n")

        time.sleep(1)

    elif opcionMenu == "14":
        try:
            print("\nEscribe el id del AFN a eliminar:")
            num = int(input(""))
            conteoDeEdos = conjunto.eliminaUnAfn(num-1, conteoDeEdos)
            numCrear -= 1
            print("AFN eliminado correctamente\n")
        except:
            print("No se encontró la ID de dicho autómata\n")
        time.sleep(1)

    elif opcionMenu == "15":
        break
    else:
        print("\nNo es una opción válida\npulsa una tecla para continuar...")
        input("")






