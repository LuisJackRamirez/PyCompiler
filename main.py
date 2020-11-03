import time
import copy
from tabulate import tabulate
from Estado import Estado
from Transicion import Transicion
from AFN import AFN
from conjuntoAFN import conjuntoAFN

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
    print("\t12 - salir")

def TablaGeneral(conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AF's por mostrar")
    else:
        ''' Como no hay AFN, creamos primero variables de apoyo '''
        tabla = [['Id', 'Alfabeto', 'Estados', 'Estado inicial', 'Estados Finales', 'Expresión regular']]
        aux2 = copy.deepcopy(conjunto.con)

        aux2.reverse()

        ''' Ciclo para extraer cada AFN para mostrarlo en la tabla '''
        while (len(aux2) >= 1):
            aux = aux2.pop()
            ''' extraer id del estado inicial para la tabla '''
            Sfinal = str(aux.S.identificador)
            ''' variables de apoyo
            
                aux3 = se guardan aquí los estados sacados
                todos = mostrar todos los estados existentes en la tabla
                edosFinales = mostrar estados finales en la tabla
                numTodos = saber cuántos estados hay y ordenarlos de forma ascendente (1, 2, ...)
                numFinales = saber donde se encuentran los estados finales '''
            aux3 = copy.deepcopy(aux)
            todos = ""
            edosFinales = ""
            numTodos = []
            numFinales = []

            ''' Ciclo para saber cuales estados del AFN son finales,
                así como para saber cuántos hay '''
            while (len(aux3.edosAFN) >= 1):
                finales = aux3.edosAFN.pop()
                numTodos.append(finales.identificador)
                if finales.edoFinal == True:
                    numFinales.append(finales.identificador)

            ''' Regresando estados al AFN "aux", así como ordenar los id's para la tabla '''
            numTodos = sorted(numTodos)
            numFinales = sorted(numFinales)

            ''' obteniendo los id's de todos los estados '''
            for i in range(0, len(numTodos) - 1):
                todos += str(numTodos[i]) + ", "
            todos += str(numTodos[len(numTodos) - 1])

            ''' obteniendo los id's de todos los estados finales '''
            for i in range(0, len(numFinales) - 1):
                edosFinales += str(numFinales[i]) + ", "
            edosFinales += str(numFinales[len(numFinales) - 1])

            ''' Imprimiendo tabla '''
            afs = [str(aux.idAFN), repr(aux.E), todos, Sfinal, edosFinales, str(aux.ER)]
            tabla.append(afs)

        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def TablaAFN(id, conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AF's por mostrar")
    else:
        ''' Como no hay AFN, creamos primero variables de apoyo '''
        contador = 1
        arreglo = []
        tabla = [['Id del Estado', 'Transiciones (símbolo,edoDestino)', '¿Es estado inicial?', '¿Es estado Final?', 'Token']]
        aux3 = copy.deepcopy(conjunto.con)

        while(len(aux3) >= 1):
            aux = aux3.pop()
            if aux.idAFN == id:
                afn = aux

        afn.edosAFN.reverse()

        while(len(afn.edosAFN) >= 1):
            edo = afn.edosAFN.pop()

            if edo.edoInicial == True:
                var1 = "Verdadero"
            else:
                var1 = "Falso"
            if edo.edoFinal == True:
                var2 = "Verdadero"
            else:
                var2 = "Falso"

            ''' Imprimiendo tabla '''
            if edo.transiciones[0] == '(':
                afs = [str(edo.identificador), edo.transiciones, var1, var2, edo.token]
            elif edo.transiciones[0] == ' ':
                afs = [str(edo.identificador), "Epsilon", var1, var2, edo.token]
            else:
                cad = ""
                while(len(edo.transiciones) >= 1):
                    aux = edo.transiciones.pop()
                    for i in range(0, len(aux)):
                        cad += aux[i]
                    if(len(edo.transiciones) >= 1):
                        cad += ","
                afs = [str(edo.identificador), cad, var1, var2, edo.token]

            tabla.append(afs)

        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

def Crear(symbol, conjunto, conteoDeEdos, numCrear):
    transicion1 = "(" + symbol + "," + str(conteoDeEdos+1) + ")"
    x = Estado(conteoDeEdos, transicion1, True, False, 0)
    x1 = Estado(conteoDeEdos+1, " ", False, True, (numCrear+1)*10)

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
    aux2 = []
    contador = 1
    while (len(conjunto.con) >= 1):
        aux = conjunto.con.pop()
        if aux.idAFN == id1:
            af1 = aux
            aux4 = copy.deepcopy(aux.S)
            idx1 = aux4.identificador
            tam = len(aux.edosAFN)
        elif aux.idAFN == id2:
            af2 = aux
            aux4 = copy.deepcopy(aux.S)
            idx2 = aux4.identificador
            tam2 = len(aux.edosAFN)
        else:
            aux2.insert(contador, aux)
            contador += 1

    contador = 1

    if idx1 <= idx2:
        id3 = idx1
        id4 = idx2
    else:
        id3 = idx2
        id4 = idx1

    ''' Añadiendo el estado inicial "x" de la operación unión '''
    transicion1 = ["( ," + str(id3+1) + ")", "( ," + str(id4+1) + ")"]
    x = Estado(id3, transicion1, True, False, 0)
    ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
    noms = []
    noms.insert(contador - 1, x)
    contador += 1

    afx = []
    afx.insert(0,af1)
    afx.insert(1,af2)

    while(len(afx) >= 1):
        af = afx.pop()
        while (len(af.edosAFN) >= 1):
            val = af.edosAFN.pop()
            if val.edoFinal == False:
                val.identificador = val.identificador + 1
                val.edoFinal = False
                val.edoInicial = False
                if val.transiciones[0] == '(':
                    cad = ""
                    for i in range(0, len(val.transiciones)):
                        if val.transiciones[i] == ",":
                            j = 1
                            while (val.transiciones[i + j] != ")"):
                                cad += val.transiciones[i + j]
                                j += 1
                    val.transiciones = "(" + val.transiciones[1] + "," + str(int(cad) + 1) + ")"
                else:
                    aux3 = []
                    contador2 = 1
                    while (len(val.transiciones) >= 1):
                        aux = val.transiciones.pop()
                        cad2 = ""
                        for i in range(0, len(aux)):
                            if aux[i] == ",":
                                j = 1
                                while (aux[i + j] != ")"):
                                    cad2 += aux[i + j]
                                    j += 1
                        cad = "(" + aux[1] + "," + str(int(cad2) + 1) + ")"
                        aux3.insert(contador2, cad)
                        contador2 += 1
                    val.transiciones = aux3
                val.token = 0
                noms.insert(contador, val)
                contador += 1
            else:
                val.identificador = val.identificador + 1
                val.edoFinal = False
                val.edoInicial = False
                val.token = 0
                val.transiciones = "( ," + str(tam + tam2 + 1 + id3) + ")"
                noms.insert(contador, val)
                contador += 1

    ''' Añadiendo el estado final al AFN "noms" '''
    x1 = Estado(tam+tam2+1+id3, " ", False, True, (numCrear-1)*10)
    noms.insert(contador, x1)
    contador = 1

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
        er = "(" + af1.ER + ")" + " | " + af2.ER
    elif len(af1.ER) == 1 and len(af2.ER) != 1:
        er = af1.ER + " | " + "(" + af2.ER + ")"
    else:
        er = "(" + af1.ER + ")" + " | " + "(" + af2.ER + ")"

    ''' Regresando los AFN que no se ocuparon a "conjunto.con" '''
    while (len(aux2) >= 1):
        aux = aux2.pop()
        aux.idAFN = contador
        conjunto.con.insert(contador - 1, aux)
        contador += 1

    ''' Añadiendo el nuevo AFN a "conjunto.con" '''
    conjunto.con.insert(contador - 1, AFN(x, symbol, noms, x1, contador, er))

def CerrKleene (id1, conjunto):
    '''Función que transforma el AFN a la operación Cerradura de Kleene'''
    af1 = CerrTransitiva (id1, conjunto)
    for i in af1.F:
        af1.S.addTransicion (Transicion ("", i))

def CerrTransitiva (id1, conjunto):
    '''Función que transforma el AFN a la operación Cerradura Transitiva'''
    af1 = AFN
    for i in conjunto.con:                  #Buscar y obtener los
        if i.idAFN == id1:                  #AFN solicitados
            af1 = i
            break

    global numCrear

    #Creación de los estados requeridos para la cerradura Transitiva
    x = Estado(numCrear, set(), True, False, 10)
    x1 = Estado(numCrear + 1, set(), False, True, 20)

    numCrear += 2

    #Creada la transición épsilon para x
    y = Transicion ("", af1.S)
    x.addTransicion (y)

    #Añadir la transición épsilon hacia x1 a los estados
    #finales, y de regreso al estado inicial
    for i in af1.F:
        i.addTransicion (y)
        i.addTransicion (Transicion ("", x1))
        i.edoFinal = False

    #Finalmente, adición de los nuevos estados al AFN,
    #y modificación del estado inicial y final
    af1.F = {x1}
    af1.edosAFN.add (x)
    af1.edosAFN.add (x1)
    af1.S = x

    return af1

def Concatenar(id1, id2, conjunto):
    '''Función que realiza la operación concatenar con dos AFNs
       Recibe los ids de los AFN, el conjunto de AFN, y el contador de AFN creados'''
    af1 = AFN
    af2 = AFN
    for i in conjunto.con:                  #Buscar y obtener los
        if i.idAFN == id1:                  #AFN solicitados
            af1 = i
        elif i.idAFN == id2:
            af2 = i

    aux=[]                                  #Para ver qué estados deberemos de quitar

    for i in af1.edosAFN:                           #Por cada estado del autómata 1,
        for j in i.transiciones:                    #por cada transición del estado,
            if j.edoDestino in af1.F:               #si encontramos un estado final
                aux.append (j.edoDestino)
                af1.F.remove (j.edoDestino)         #lo eliminamos de la lista y lo reemplazamos
                j.edoDestino = af2.S                #por la id inicial del AFN2

    '''Eliminamos los estados finales de AF1 de su conjunto de estados'''
    for i in aux:
        af1.edosAFN.remove (i)

    '''Juntamos el set de estados de AF2 con el de AF1,
    y eliminamos AF2 de la lista de AFN'''
    af1.edosAFN.update (af2.edosAFN)
    af1.F = af2.F
    conjunto.con.remove (af2)

    '''Aquí unimos los dos alfabetos y eliminamos los caracteres repetidos'''
    af1.E = af1.E + af2.E
    af1.E = "".join (set (af1.E))

def Opcional (id1, conjunto):
    '''Función que transforma el AFN a la operación Opcional'''
    af1 = AFN
    for i in conjunto.con:                  #Buscar y obtener los
        if i.idAFN == id1:                  #AFN solicitados
            af1 = i
            break

    global numCrear

    #Creación de los estados requeridos para la cerradura Transitiva
    x = Estado(numCrear, set(), True, False, 10)
    x1 = Estado(numCrear + 1, set(), False, True, 20)

    numCrear += 2

    #Creada la transición epsilon para x
    x.addTransicion (Transicion ("", af1.S))
    x.addTransicion (Transicion ("", x1))

    #Añadir la transición épsilon hacia x1 a los estados
    #finales, y de regreso al estado inicial
    for i in af1.F:
        i.addTransicion (Transicion ("", x1))
        i.edoFinal = False

    #Finalmente, adición de los nuevos estados al AFN,
    #y modificación del estado inicial y final
    af1.F = {x1}
    af1.edosAFN.add (x)
    af1.edosAFN.add (x1)
    af1.S = x

def prepararAnalisis(conjunto):
    if len(conjunto.con) <= 1:
        print("No se puede realizar la unión, hay menos de 2 AFN en la base de datos")
        time.sleep(1)
    else:
        contador = 1
        transicion1 = []
        aux = copy.deepcopy(conjunto.con)
        ''' Añadiendo el estado inicial "x" de la operación unión '''
        while(len(aux) >= 1):
            aux2 = aux.pop()
            while(len(aux2.edosAFN) >= 1):
                aux3 = aux2.edosAFN.pop()
                transicion1 += ["( ," + str(aux3.identificador+ 1) + ")"]

        x = Estado(0, transicion1, True, False, 0)
        ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
        noms = []
        auxFinal = []
        noms.insert(contador - 1, x)
        contador += 1
        contador3 = 1

        final = conjunto.con
        final.reverse()

        ''' Sacando cada estado de los afn para modificarlos, cambiando sus transiciones '''
        symbol = ""
        er = ""
        while(len(final) >= 1):
            af1 = final.pop()

            ''' Definiendo el alfabeto de noms '''
            flag = 0
            for i in range(0, len(af1.E)):
                for j in range(0, len(symbol)):
                    if (af1.E[i] == symbol[j]):
                        flag = 1
                if flag == 0 and contador != 2:
                    symbol += ", " + af1.E[i]
                elif flag == 0:
                    symbol += af1.E[i]

            while (len(af1.edosAFN) >= 1):
                val = af1.edosAFN.pop()
                val.identificador = val.identificador + 1
                if val.edoFinal == False:
                    val.edoInicial = False
                    if val.transiciones[0] == '(':
                        cad = ""
                        for i in range(0, len(val.transiciones)):
                            if val.transiciones[i] == ",":
                                j = 1
                                while (val.transiciones[i + j] != ")"):
                                    cad += val.transiciones[i + j]
                                    j += 1
                        val.transiciones = "(" + val.transiciones[1] + "," + str(int(cad) + 1) + ")"
                    else:
                        aux3 = []
                        contador2 = 1
                        while (len(val.transiciones) >= 1):
                            aux = val.transiciones.pop()
                            cad2 = ""
                            for i in range(0, len(aux)):
                                if aux[i] == ",":
                                    j = 1
                                    while (aux[i + j] != ")"):
                                        cad2 += aux[i + j]
                                        j += 1
                            cad = "(" + aux[1] + "," + str(int(cad2) + 1) + ")"
                            aux3.insert(contador2, cad)
                            contador2 += 1
                        val.transiciones = aux3
                    val.token = 0
                else:
                    auxFinal.insert(contador3, val)
                    contador3 += 1

                noms.insert(contador, val)
                contador += 1

            ''' Definiendo la expresión regular del afn final '''
            if er != "":
                er += " | " + "(" + af1.ER + ")"
            else:
                er = "(" + af1.ER + ")"

        ''' Añadiendo el nuevo AFN a "conjunto.con" '''
        conjunto.con.insert(contador - 1, AFN(x, symbol, noms, auxFinal, 1, er))
        print("uniendo AFN...")
        time.sleep(1)
        print("¡Nuevo AFN creado con éxito!\n")

conjunto = conjuntoAFN
numAFNCreados = 1
numCrear = 0
conteoDeEdos = 0
print("\n¡Hola!, Bienvenido al programa de análisis léxico")

while True:
    menu()
    opcionMenu = input("")

    if opcionMenu == "1":
        TablaGeneral(conjunto, numCrear)

    elif opcionMenu == "2":
        print("\nPara mostrar la tabla de un AFN, escribe el id del AFN:")
        num = int(input(""))
        TablaAFN(num, conjunto, numCrear)

    elif opcionMenu == "3":
        print("\nPara crear el AFN, escribe el carácter al cual crearle el AFN:")
        symbol = str(input(""))[0]
        Crear(symbol, conjunto, conteoDeEdos, numCrear)
        conteoDeEdos += 2
        numCrear += 1
        numAFNCreados += 1

    elif opcionMenu == "4":
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

    elif opcionMenu == "5":
        print("\nIngresa el id del primer AFN a concatenar:")
        id1 = int(input(""))
        print("\nIngresa el id del segundo AFN a concatenar:")
        id2 = int(input(""))
        Concatenar(id1, id2, conjunto)
        print("¡Nuevo AFN creado con éxito!\n")

    elif opcionMenu == "6":
        print("\nIngresa el id del AFN al cual obtener la cerradura transitiva:")
        id1 = int(input(""))
        CerrTransitiva(id1, conjunto)
        print("¡Nuevo AFN creado con éxito!\n")

    elif opcionMenu == "7":
        print("\nIngresa el id del AFN al cual obtener la cerradura de kleene:")
        id1 = int(input(""))
        CerrKleene(id1, conjunto)
        print("¡Nuevo AFN creado con éxito!\n")

    elif opcionMenu == "8":
        print("\nIngresa el id del AFN al cual obtener la operación opcional:")
        id1 = int(input(""))
        Opcional(id1, conjunto)
        print("¡Nuevo AFN creado con éxito!\n")

    elif opcionMenu == "9":
        print("\nTodos los AFN del sistema se van a unir, ¿Deseas continuar? (S/N)")
        resp = str(input(""))[0]
        if resp == "S" or resp == "s":
            prepararAnalisis(conjunto)
        else:
            time.sleep(1)

    elif opcionMenu == "10":
        print("\nIngresa el id del AFN a convertir a un AFD:")
        print("¡Nuevo AFD creado con éxito!\n")

    elif opcionMenu == "11":
        print("\nIngresa el id del AF a introducir una cadena:")
        print("¡Prueba concluida con éxito!\n")

    elif opcionMenu == "12":
        break
    else:
        print("\nNo es una opción válida\npulsa una tecla para continuar...")
        input("")
