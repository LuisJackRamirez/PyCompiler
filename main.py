import time
import copy
from tabulate import tabulate
from Estado import Estado
from Transicion import Transicion
from AFN import AFN
from conjuntoAFN import conjuntoAFN
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

def menu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    time.sleep(2)
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
    print("\t10 - Convertir un AFN a un AFD")
    print("\t11 - Hacer una prueba con una cadena en un AF")
    print("\t12 - tablas AFD (tabla 1: AFD, tabla2: Transiciones de los estados del AFD)")
    print("\t13 - salir")

def TablaGeneral(conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AFN's por mostrar")
    else:
        ''' Como hay AFN, creamos primero variables de apoyo '''
        contador = 1
        ''' Como hay AFN, creamos primero variables de apoyo '''
        tabla = [['Id', 'Alfabeto', 'Estados', 'Estado inicial', 'Estados Finales', 'Expresión regular']]

        aux2 = copy.deepcopy(conjunto.con)

        ''' Ciclo para extraer cada AFN para mostrarlo en la tabla '''
        for i in aux2:
            ''' extraer id del estado inicial para la tabla '''
            Sfinal = str(i.S.identificador)
            todos = ""
            edosFinales = ""
            numTodos = []
            numFinales = []

            ''' Ciclo para saber cuales estados del AFN son finales,
                así como para saber cuántos hay '''
            for j in i.edosAFN:
                numTodos.append(j.identificador)
                if j.edoFinal == True:
                    numFinales.append(j.identificador)

            ''' Regresando estados al AFN "aux", así como ordenar los id's para la tabla '''
            numTodos = sorted(numTodos)
            numFinales = sorted(numFinales)

            ''' obteniendo los id's de todos los estados '''
            for j in range(0, len(numTodos) - 1):
                todos += str(numTodos[j]) + ", "
            todos += str(numTodos[len(numTodos) - 1])

            ''' obteniendo los id's de todos los estados finales '''
            for j in range(0, len(numFinales) - 1):
                edosFinales += str(numFinales[j]) + ", "
            edosFinales += str(numFinales[len(numFinales) - 1])

            ''' Imprimiendo tabla '''
            afs = [str(i.idAFN), repr(i.E), todos, Sfinal, edosFinales, str(i.ER)]
            tabla.insert(contador, afs)
            contador += 1

        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def TablaAFN(id, conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AFN's por mostrar")
    else:
        aux3 = copy.deepcopy(conjunto.con)

        for i in aux3:
            if i.idAFN == id:
                afn = i

        contador2 = 1
        ''' Como hay AFN, creamos primero variables de apoyo '''
        tabla = [['Id del Estado', 'Transiciones (símbolo,edoDestino)', '¿Es estado inicial?', '¿Es estado Final?', 'Token']]

        for i in afn.edosAFN:
            if i.edoInicial == True:
                var1 = "Verdadero"
            else:
                var1 = "Falso"
            if i.edoFinal == True:
                var2 = "Verdadero"
            else:
                var2 = "Falso"

            ''' Imprimiendo tabla '''
            try:
                cad = ""
                contador = 1
                for j in i.transiciones:
                    if contador != 1:
                        cad += ","
                    if j.simbolo == None:
                        afs = [str(i.identificador), "No hay transiciones", var1, var2, i.token]
                    else:
                        if j.simbolo == " ":
                            cad2 = "Epsilon"
                        else:
                            cad2 = str(j.simbolo)
                        aux3 = j.edoDestino
                        cad += "(" + cad2 + "," + str(aux3.identificador) + ")"
                    contador += 1
                afs = [str(i.identificador), cad, var1, var2, i.token]
            except:
                aux = i.transiciones
                if aux == None:
                    afs = [str(i.identificador), "No hay transiciones", var1, var2, i.token]
                else:
                    if aux.simbolo == " ":
                        cad2 = "Epsilon"
                    else:
                        cad2 = str(aux.simbolo)
                    aux2 = aux.edoDestino
                    cad = "(" + cad2 + "," + str(aux2.identificador) + ")"
                    afs = [str(i.identificador), cad, var1, var2, i.token]

            tabla.insert(contador2, afs)
            contador2 += 1

        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def Crear(symbol, conjunto, conteoDeEdos, numCrear):
    x1 = Estado(conteoDeEdos+1, None, False, True, (numCrear+1)*10)
    transicion1 = Transicion(symbol, x1)
    x = Estado(conteoDeEdos, transicion1, True, False, 0)

    ''' Revisar si "conjunto" tiene estados o no '''
    if len(conjunto.con) >= 1:
        ''' "conjunto" tiene estados, por tanto se añade al final el nuevo AFN '''
        conjunto.con.insert(numCrear, AFN(x, symbol, {x, x1}, {x1}, 1 + numCrear, symbol))
    else:
        ''' "conjunto" no tiene estados, por tanto se añade al principio '''
        conjunto.con = [AFN(x, symbol, {x, x1}, {x1}, 1 + numCrear, symbol)]
    print("creando AFN...")
    time.sleep(1)
    print("¡AFN creado con éxito!\n")

def Unir(id1, id2, conjunto):
    ''' El siguiente ciclo es para vaciar "conjunto.con", sacando cada AFN, para así buscar los 2 AFN a unir,
                si se encuentran, se almacenan en "af1" y "af2", sino, se van guardando en "aux2" para después volver a
                guardar en conjunto.con todos los AFN sacados '''

    for i in conjunto.con:
        if i.idAFN == id1:
            af1 = copy.deepcopy(i)
            r1 = i
            tam = len(i.edosAFN)
        elif i.idAFN == id2:
            af2 = copy.deepcopy(i)
            r2 = i
            tam2 = len(i.edosAFN)

    conjunto.con.remove(r1)
    conjunto.con.remove(r2)

    contador = 1
    contador2 = 1

    for i in conjunto.con:
        i.idAFN = contador
        for j in i.edosAFN:
            j.identificador = contador2 - 1
            contador2 += 1
        contador += 1

    contador3 = 1
    ''' Añadiendo el estado inicial "x" de la operación unión '''
    transicion1 = [Transicion(" ", af1.S), Transicion(" ", af2.S)]
    x = Estado(contador2-1, transicion1, True, False, 0)
    ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
    noms = []
    noms.insert(contador3 - 1, x)
    contador3 += 1
    contador2 += 1

    ''' Añadiendo el estado final al AFN "noms" '''
    x1 = Estado(tam + tam2 + contador2 - 1, None, False, True, (numCrear - 1) * 10)

    afx = []
    afx.insert(0,af1)
    afx.insert(1,af2)

    for i in afx:
        for j in i.edosAFN:
            if j.edoFinal == False:
                j.identificador = contador2 - 1
                j.edoFinal = False
                j.edoInicial = False
                j.token = 0
                noms.insert(contador3, j)
                contador3 += 1
                contador2 += 1
            else:
                j.identificador = contador2 - 1
                j.edoFinal = False
                j.edoInicial = False
                j.token = 0
                transicion1 = Transicion(" ", x1)
                j.transiciones = transicion1
                noms.insert(contador3, j)
                contador3 += 1
                contador2 += 1

    noms.insert(contador3, x1)

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
        er = af1.ER + " | " + af2.ER
    elif len(af1.ER) != 1 and len(af2.ER) == 1:
        er = "\(" + af1.ER + "\)" + " | " + af2.ER
    elif len(af1.ER) == 1 and len(af2.ER) != 1:
        er = af1.ER + " | " + "\(" + af2.ER + "\)"
    else:
        er = "\(" + af1.ER + "\)" + " | " + "\(" + af2.ER + "\)"

    ''' Añadiendo el nuevo AFN a "conjunto.con" '''
    conjunto.con.insert(contador - 1, AFN(x, symbol, noms, {x1}, contador, er))

def CerrKleene (id1, conjunto):
    '''Función que transforma el AFN a la operación Cerradura de Kleene'''
    af1 = operacionTransitiva (id1, conjunto)
    if af1 == -1:
        return -1

    for i in af1.F:
        af1.S.addTransicion (Transicion (" ", i))

    # Cambiando la expresion regular
    ex = "\(" + str(af1.ER) + "\)\*"
    af1.ER = ex

def operacionTransitiva(id1, conjunto):
    '''Función que transforma el AFN a la operación Cerradura Transitiva'''
    af1 = None
    for i in conjunto.con:  # Buscar y obtener los
        if i.idAFN == id1:  # AFN solicitados
            af1 = i
            break

    if af1 == None:
        return -1

    global conteoDeEdos

    # Creación de los estados requeridos para la cerradura Transitiva
    x = Estado(af1.S.identificador, set(), True, False, 10)
    x1 = Estado(conteoDeEdos + 1, None, False, True, 20)

    conteoDeEdos += 2

    # Creada la transición épsilon para x
    y = Transicion(" ", af1.S)
    x.addTransicion(y)

    # Añadir la transición épsilon hacia x1 a los estados
    # finales, y de regreso al estado inicial
    for i in af1.F:
        if i.transiciones == None:
            i.transiciones = {y}
        else:
            i.addTransicion(y)

        i.addTransicion(Transicion(" ", x1))
        i.edoFinal = False

    # Aumentando el id de todos los estados para añadir el inicial
    for i in af1.edosAFN:
        if i.edoFinal == False:
            i.identificador = i.identificador + 1
            i.edoInicial = False

    # Finalmente, adición de los nuevos estados al AFN,
    # y modificación del estado inicial y final
    af1.F = {x1}
    try:
        af1.edosAFN.add(x)
        af1.edosAFN.add(x1)
    except:
        af1.edosAFN.insert(len(af1.edosAFN), x)
        af1.edosAFN.insert(len(af1.edosAFN), x1)
    af1.S = x

    return af1

def CerrTransitiva (id1, conjunto):
    '''Función que transforma el AFN a la operación Cerradura de Kleene'''
    af1 = operacionTransitiva(id1, conjunto)
    if af1 == -1:
        return -1

    #Cambiando la expresion regular
    ex = "\(" + str(af1.ER) + "\)\+"
    af1.ER = ex

def Concatenar(id1, id2, conjunto):
    '''Función que realiza la operación concatenar con dos AFNs
       Recibe los ids de los AFN, el conjunto de AFN, y el contador de AFN creados'''
    af1 = -1
    af2 = -1
    for i in conjunto.con:                  #Buscar y obtener los
        if i.idAFN == id1:                  #AFN solicitados
            af1 = i
        elif i.idAFN == id2:
            af2 = i

    if af1 == -1 or af2 == -1:
        return -1

    aux=[]                                  #Para ver qué estados deberemos de quitar

    for i in af1.edosAFN:                           #Por cada estado del autómata 1,
        if i.transiciones != None:
            try:
                for j in i.transiciones:                    #por cada transición del estado,
                    if j.edoDestino in af1.F:               #si encontramos un estado final
                        aux.append (j.edoDestino)
                        af1.F.remove (j.edoDestino)         #lo eliminamos de la lista y lo reemplazamos
                        j.edoDestino = af2.S                #por la id inicial del AFN2
            except:
                if i.transiciones.edoDestino in af1.F:  # si encontramos un estado final
                    aux.append(i.transiciones.edoDestino)
                    af1.F.remove(i.transiciones.edoDestino)  # lo eliminamos de la lista y lo reemplazamos
                    i.transiciones.edoDestino = af2.S  # por la id inicial del AFN2

    '''Eliminamos los estados finales de AF1 de su conjunto de estados'''
    for i in aux:
        af1.edosAFN.remove (i)

    for i in af2.edosAFN:
        i.edoInicial = False

    '''Juntamos el set de estados de AF2 con el de AF1,
    y eliminamos AF2 de la lista de AFN'''
    af1.edosAFN.update (af2.edosAFN)
    af1.F = af2.F
    conjunto.con.remove (af2)

    '''Ajustando los id de los edos'''
    for i in af1.edosAFN:
        if i.edoInicial == False:
            i.identificador = i.identificador - 1

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
    ex = "\(" + str(af1.ER) + "\)•\(" + str(af2.ER) + "\)"
    af1.ER = ex

def Opcional (id1, conjunto):
    '''Función que transforma el AFN a la operación Opcional'''
    af1 = None
    for i in conjunto.con:                  #Buscar y obtener los
        if i.idAFN == id1:                  #AFN solicitados
            af1 = i
            break

    if af1 == None:
        return -1

    global conteoDeEdos

    #Creación de los estados requeridos para la cerradura Transitiva
    x = Estado(af1.S.identificador, set(), True, False, 10)
    x1 = Estado(conteoDeEdos + 1, None, False, True, 20)

    conteoDeEdos += 2

    #Creada la transición epsilon para x
    x.addTransicion(Transicion(" ", af1.S))
    x.addTransicion(Transicion(" ", x1))
    y = Transicion(" ", x1)

    #Añadir la transición épsilon hacia x1 a los estados
    #finales, y de regreso al estado inicial
    for i in af1.F:
        if i.transiciones == None:
            i.transiciones = {y}
        else:
            i.addTransicion (y)
        i.edoFinal = False

    #Aumentando el id de todos los estados para añadir el inicial
    for i in af1.edosAFN:
        if i.edoFinal == False:
            i.identificador = i.identificador + 1
            i.edoInicial = False

    # Finalmente, adición de los nuevos estados al AFN,
    # y modificación del estado inicial y final
    af1.F = {x1}
    try:
        af1.edosAFN.add(x)
        af1.edosAFN.add(x1)
    except:
        af1.edosAFN.insert(len(af1.edosAFN), x)
        af1.edosAFN.insert(len(af1.edosAFN), x1)
    af1.S = x

    # Cambiando la expresion regular
    ex = "\(" + str(af1.ER) + "\)?"
    af1.ER = ex

def prepararAnalisis(conjunto):
    if len(conjunto.con) <= 1:
        print("No se puede realizar la unión, hay menos de 2 AFN en la base de datos")
        time.sleep(1)
    else:
        contador = 1
        transicion1 = []

        ''' Añadiendo el estado inicial "x" de la operación unión '''
        for i in conjunto.con:
            for j in i.edosAFN:
                j.identificador = j.identificador + 1
                if j.edoInicial == True:
                    transicion1 += [Transicion(" ", j)]

        x = Estado(0, transicion1, True, False, 0)
        ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
        noms = []
        auxFinal = []
        noms.insert(contador - 1, x)
        contador += 1
        contador3 = 1

        ''' Sacando cada estado de los afn para modificarlos, cambiando sus transiciones '''
        symbol = ""
        er = ""

        for i in conjunto.con:
            ''' Definiendo el alfabeto de noms '''
            flag = 0
            for j in range(0, len(i.E)):
                for k in range(0, len(symbol)):
                    if (i.E[j] == symbol[k]):
                        flag = 1
                if flag == 0 and contador != 2:
                    symbol += ", " + i.E[j]
                elif flag == 0:
                    symbol += i.E[j]

            for j in i.edosAFN:
                if j.edoFinal == False:
                    j.edoInicial = False
                else:
                    auxFinal.insert(contador3, j)
                    contador3 += 1
                noms.insert(contador, j)
                contador += 1

            ''' Definiendo la expresión regular del afn final '''
            if er != "":
                er += " | " + "\(" + i.ER + "\)"
            else:
                er = "\(" + i.ER + "\)"

        conjunto.con.clear()

        ''' Añadiendo el nuevo AFN a "conjunto.con" '''
        conjunto.con.insert(contador - 1, AFN(x, symbol, noms, auxFinal, 1, er))
        print("uniendo AFN...")
        time.sleep(1)
        print("¡Nuevo AFN creado con éxito!\n")

def TablaGeneralAFD(conjunto, numCrear):
    ''' Se verifica primero si hay AFD o no '''
    if numCrear == 0:
        print("\nNo hay AFD's por mostrar")
    else:
        ''' Como hay AFD, creamos primero variables de apoyo '''
        contador = 1
        tabla = [['Id', 'Alfabeto', 'Estados', 'Estado inicial', 'Estados Finales', 'Expresión regular']]

        aux2 = copy.deepcopy(conjunto.con)

        contador = 1
        ''' Ciclo para extraer cada AFD para mostrarlo en la tabla '''
        for i in aux2:
            ''' extraer id del estado inicial para la tabla '''
            Sfinal = str(i.S.identificador)
            todos = ""
            edosFinales = ""
            numTodos = []
            numFinales = []

            ''' Ciclo para saber cuales estados del AFD son finales,
                así como para saber cuántos hay '''
            for j in i.edosAFN:
                numTodos.append(j.identificador)
                if j.edoFinal == True:
                    numFinales.append(j.identificador)

            ''' Regresando estados al AFD "aux", así como ordenar los id's para la tabla '''
            numTodos = sorted(numTodos)
            numFinales = sorted(numFinales)

            ''' obteniendo los id's de todos los estados '''
            for j in range(0, len(numTodos) - 1):
                todos += str(numTodos[j]) + ", "
            todos += str(numTodos[len(numTodos) - 1])

            ''' obteniendo los id's de todos los estados finales '''
            for j in range(0, len(numFinales) - 1):
                edosFinales += str(numFinales[j]) + ", "
            edosFinales += str(numFinales[len(numFinales) - 1])

            ''' Imprimiendo tabla '''
            afs = [str(i.idAFN), repr(i.E), todos, Sfinal, edosFinales, str(i.ER)]
            tabla.insert(contador, afs)
            contador += 1

        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def TablaAFD(id, conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AFD's por mostrar")
    else:
        aux3 = copy.deepcopy(conjunto.con)

        for i in aux3:
            if i.idAFN == id:
                afd = i

        contador2 = 1
        ''' Como hay AFN, creamos primero variables de apoyo '''
        tabla = [['Id del Estado', 'Transiciones (símbolo,edoDestino)', '¿Es estado inicial?', '¿Es estado Final?', 'Token']]

        for i in afd.edosAFN:
            if i.edoInicial == True:
                var1 = "Verdadero"
            else:
                var1 = "Falso"
            if i.edoFinal == True:
                var2 = "Verdadero"
            else:
                var2 = "Falso"

            ''' Imprimiendo tabla '''
            try:
                cad = ""
                contador = 1
                for j in i.transiciones:
                    if contador != 1:
                        cad += ","
                    if j.simbolo == None:
                        afs = [str(i.identificador), "No hay transiciones", var1, var2, i.token]
                    else:
                        cad2 = str(j.simbolo)
                        aux3 = j.edoDestino
                        cad += "(" + cad2 + "," + str(aux3.identificador) + ")"
                    contador += 1
                afs = [str(i.identificador), cad, var1, var2, i.token]
            except:
                aux = i.transiciones
                if aux == None:
                    afs = [str(i.identificador), "No hay transiciones", var1, var2, i.token]
                else:
                    cad2 = str(aux.simbolo)
                    aux2 = aux.edoDestino
                    cad = "(" + cad2 + "," + str(aux2.identificador) + ")"
                    afs = [str(i.identificador), cad, var1, var2, i.token]

            tabla.insert(contador2, afs)
            contador2 += 1

        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def afn_AFD(idA, conjunto, bandera):
    if idA in afn_api.keys() and idA not in afn_convertidos:
        afn = afn_api[idA].copy()
    else:
        aux3 = copy.deepcopy(conjunto.con)

        for i in aux3:
            if i.idAFN == idA:
                afn = i
        # estados

        edosId = set()
        edosfinales = set()
        edosinicial = set()
        ##Obtener transiciones
        dictrans = {}
        alfabeto = set()
        estadoinicial = ""
        for i in afn.edosAFN:
            if (i.edoInicial == True):
                edosinicial.add(str(i.identificador))
                estadoinicial = str(i.identificador)
                if (len(edosinicial) > 1):
                    print("ERROR, HAY MAS DE UN ESTADO INICIAL")
                    break
            if (i.edoFinal == True):
                edosfinales.add(str(i.identificador))
            edosId.add(str(i.identificador))
            try:
                for j in i.transiciones:
                    var1 = str(j.simbolo)

                    if j.simbolo == None or j.simbolo == " ":
                        var1 = ''
                    else:
                        alfabeto.add(var1)
                    var2 = str(j.edoDestino.identificador)
                    agregardiccionario(var1, var2)
                dictrans[str(i.identificador)] = devolverdiccionario()

            except:
                auxtran = i.transiciones
                if auxtran == None:
                    print(str(i.identificador))
                    agregardiccionario('', str(i.identificador))
                    dictrans[str(i.identificador)] = devolverdiccionario()
                else:
                    if auxtran.simbolo == " ":
                        var1 = ''
                    else:
                        var1 = str(auxtran.simbolo)
                        alfabeto.add(var1)
                    agregardiccionario(var1, str(auxtran.edoDestino.identificador))
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
    print("¿CONVERSION CORRECTA?")
    print(afd.validate())
    for k, i in afd.transitions.items():

        for clave, valor in i.items():
            if clave == '{}' or clave == None or valor == '{}' or valor == None:
                del transicionesafd[k]
    for clave in afd.transitions.keys():
        if clave == None or clave == '{}':
            try:
                del transicionesafd[clave]
            except:
                pass
    print("TRANSICIONES AFD")
    print(str(transicionesafd))
    afd_api[idA] = afd

def agregardiccionario(key, valor):
    diccionarioauxiliar[key] = valor

def devolverdiccionario():
    aux = diccionarioauxiliar.copy()
    diccionarioauxiliar.clear()
    return aux

def comprobar_AFN(idA, conjunto, cadena):
    bandera = 1
    afn_comprbacion = afn_AFD(idA, conjunto, bandera).copy()

    try:
        if afn_comprbacion.accepts_input(cadena):
            print("cadena aceptada")
        else:
            print("cadena no aceptada")
    except:
        print("cadeno aceptada")

afn_convertidos = []
diccionarioauxiliar ={}
afd_api={}
afn_api={}
dictrans = {}
conjunto = conjuntoAFN
conjunto2 = conjuntoAFN
numAFNCreados = 1
numCrear = 0
numCrear2 = 0
conteoDeEdos = 0
print("\n¡Hola!, Bienvenido al programa de análisis léxico")

while True:
    menu()
    opcionMenu = input("")

    if opcionMenu == "1":
        TablaGeneral(conjunto, numCrear)

    elif opcionMenu == "2":
        try:
            print("\nPara mostrar la tabla de un AFN, escribe el id del AFN:")
            num = int(input(""))
            TablaAFN(num, conjunto, numCrear)
        except:
            print("No se encontró la ID de dicho autómata\n")

    elif opcionMenu == "3":
        print("\nPara crear el AFN, escribe el carácter al cual crearle el AFN:")
        symbol = str(input(""))[0]
        Crear(symbol, conjunto, conteoDeEdos, numCrear)
        conteoDeEdos += 2
        numCrear += 1
        numAFNCreados += 1

    elif opcionMenu == "4":
        try:
            print("\nIngresa el id del primer AFN a unir:")
            id1 = int(input(""))
            print("\nIngresa el id del segundo AFN a unir:")
            id2 = int(input(""))
            Unir(id1, id2, conjunto)
            numCrear -= 1
            numAFNCreados -= 1
            conteoDeEdos += 2
            print("uniendo AFN...")
            time.sleep(1)
            print("¡Nuevo AFN creado con éxito!\n")
        except:
            print("No se encontró la ID de dichos autómatas\n")

    elif opcionMenu == "5":
        try:
            print("\nIngresa el id del primer AFN a concatenar:")
            id1 = int(input(""))
            print("\nIngresa el id del segundo AFN a concatenar:")
            id2 = int(input(""))
            a = Concatenar(id1, id2, conjunto)
            print("concatenando AFN...")
            time.sleep(1)
            print("¡Nuevo AFN creado con éxito!\n")
            numCrear =- 1
            numAFNCreados =- 1
        except:
            print("No se encontró la ID de dichos autómatas\n")

    elif opcionMenu == "6":
        print("\nIngresa el id del AFN al cual obtener la cerradura transitiva:")
        id1 = int(input(""))
        a = CerrTransitiva(id1, conjunto)

        if a == -1:
            print("No se encontró el AFN\n")
        else:
            print("obteniendo cerradura transitiva...")
            time.sleep(1)
            print("¡Nuevo AFN creado con éxito!\n")
            conteoDeEdos += 2

    elif opcionMenu == "7":
        print("\nIngresa el id del AFN al cual obtener la cerradura de kleene:")
        id1 = int(input(""))
        a = CerrKleene(id1, conjunto)

        if a == -1:
            print("No se encontró el AFN\n")
        else:
            print("obteniendo cerradura de kleene...")
            time.sleep(1)
            print("¡Nuevo AFN creado con éxito!\n")
            conteoDeEdos += 2

    elif opcionMenu == "8":
        print("\nIngresa el id del AFN al cual obtener la operación opcional:")
        id1 = int(input(""))
        a = Opcional(id1, conjunto)

        if a == -1:
            print("No se encontró el AFN\n")
        else:
            print("obteniendo operación opcional...")
            time.sleep(1)
            print("¡Nuevo AFN creado con éxito!\n")
            conteoDeEdos += 2

    elif opcionMenu == "9":
        print("\nTodos los AFN del sistema se van a unir, ¿Deseas continuar? (S/N)")
        resp = str(input(""))[0]
        if resp == "S" or resp == "s":
            prepararAnalisis(conjunto)
            numAFNCreados = 2
            conteoDeEdos += 1
            numCrear = 1
        else:
            time.sleep(1)
    elif opcionMenu == "10":
            print("\nIngresa el id del AFN a convertir a un AFD:")
            #
            # Tienes que usar la variable conjunto2 para almacenar los AFD
            #
            numCrear2 += 1

            idA = int(input())
            afn_convertidos.append(idA)
            afn_AFD(idA, conjunto, 0)
            print("¡Nuevo AFD creado con éxito!\n")
    elif opcionMenu == "11":
        print("\nIngresa el id del AF a introducir una cadena:")
        idA = int(input())
        print("Ingresa la cadena a comprobar")
        cadena = input()
        comprobar_AFN(idA, conjunto, cadena)
        time.sleep(1)
        print("¡Prueba concluida con éxito!\n")
    elif opcionMenu == "12":
        TablaGeneralAFD(conjunto2, numCrear2)
        if numCrear2 != 0:
            try:
                print("\nPara mostrar la tabla de un AFD, escribe el id del AFD:")
                num = int(input(""))
                TablaAFD(num, conjunto2, numCrear2)
            except:
                print("No se encontró la ID de dicho autómata\n")
    elif opcionMenu == "13":
        break
    else:
        print("\nNo es una opción válida\npulsa una tecla para continuar...")
        input("")
