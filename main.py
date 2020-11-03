import os
import time
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
    print("\t1 - mostrar tabla de AF's")
    print("\t2 - Crear AFN")
    print("\t3 - Unir 2 AFN")
    print("\t4 - Concatenar 2 AFN")
    print("\t5 - Cerradura transitiva de un AFN")           #A+
    print("\t6 - Cerradura de kleene de un AFN")            #A*
    print("\t7 - operación opcional de un AFN")             #A?
    print("\t8 - Unión 2 o más AFN para el análisis léxico")
    print("\t9 - Convertir un AFN a un AFD")
    print("\t10 - Hacer una prueba con una cadena en un AF")
    print("\t11 - salir")

def Tabla1(conjunto, numCrear):
    ''' Se verifica primero si hay AFN o no '''
    if numCrear == 0:
        print("\nNo hay AF's por mostrar")
    else:
        ''' Como no hay AFN, creamos primero variables de apoyo '''
        contador = 1
        tabla = [['Id', 'Alfabeto', 'Estados', 'Estado inicial', 'Estados Finales']]
        nuevaLista = []
        contador2 = 1
        aux2 = []
        ''' Se debe extraer los AF antes de la tabla, pues si no, saldrán al final todos al revés '''
        while (len(conjunto.con) >= 1):
            aux = conjunto.con.pop()
            aux2.insert(contador2, aux)
            contador2 += 1
        contador2 = 1
        ''' Ciclo para extraer cada AFN para mostrarlo en la tabla '''
        while (len(aux2) >= 1):
            aux = aux2.pop()
            ''' extraer id del estado inicial para la tabla '''
            Sfinal = str(aux.S.identificador)
            ''' variables de apoyo
            
                aux3 = se guardan aquí los estados sacados, para después devolverlos al AFN "aux"
                todos = mostrar todos los estados existentes en la tabla
                edosFinales = mostrar estados finales en la tabla
                numTodos = saber cuántos estados hay y ordenarlos de forma ascendente (1, 2, ...)
                numFinales = saber donde se encuentran los estados finales '''
            aux3 = []
            todos = ""
            edosFinales = ""
            numTodos = []
            numFinales = []

            ''' Ciclo para saber cuales estados del AFN son finales,
                así como para saber cuántos hay '''
            while (len(aux.edosAFN) >= 1):
                finales = aux.edosAFN.pop()
                numTodos.append(finales.identificador)
                if finales.edoFinal == True:
                    numFinales.append(finales.identificador)
                aux3.insert(contador, finales)
                contador += 1

            ''' Regresando estados al AFN "aux", así como ordenar los id's para la tabla '''
            contador = 1
            aux.edosAFN = aux3
            numTodos = sorted(numTodos)
            num2 = sorted(numFinales)

            ''' obteniendo los id's de todos los estados '''
            for i in range(0, len(numTodos) - 1):
                todos += str(numTodos[i]) + ", "
            todos += str(numTodos[len(numTodos) - 1])

            ''' obteniendo los id's de todos los estados finales '''
            for i in range(0, len(numFinales) - 1):
                edosFinales += str(numFinales[i]) + ", "
            edosFinales += str(numFinales[len(numFinales) - 1])

            ''' Imprimiendo tabla '''
            afs = [str(aux.idAFN), repr(aux.E), todos, Sfinal, edosFinales]
            tabla.append(afs)

            ''' "nuevaLista" es para guardar de nuevo los AFN al final en "conjunto" '''
            nuevaLista.insert(contador2, aux)
            contador2 += 1

        conjunto.con = nuevaLista
        print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))

    '''Función que transforma el AFN a la operación Cerradura Transitiva'''
def CerrTransitiva (id1, conjunto):
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
    y = Transicion ("\u03C3", af1.S)
    x.addTransicion (y)

    #Añadir la transición épsilon hacia x1 a los estados
    #finales, y de regreso al estado inicial
    for i in af1.F:
        i.addTransicion (y)
        i.addTransicion (Transicion ("\u03C3", x1))
        i.edoFinal = False

    #Finalmente, adición de los nuevos estados al AFN,
    #y modificación del estado inicial y final
    af1.F = {x1}
    af1.edosAFN.add (x)
    af1.edosAFN.add (x1)
    af1.S = x

    return af1


    '''Función que realiza la operación unión con dos AFNs
            Recibe los ids de los AFN, el conjunto de AFN, y el contador de AFN creados'''
def Concatenar(id1, id2, conjunto):
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

def Crear(symbol, conjunto, numCrear):
    global numAFNCreados

    x = Estado(numCrear, set(), True, False, 10)
    x1 = Estado(numCrear + 1, set(), False, True, 20)

    '''Se añade la transicion del estado x al estado x1 con el símbolo symbol'''
    y = Transicion (symbol, x1)
    x.addTransicion (y)

    ''' Revisar si "conjunto" tiene estados o no '''
    if len(conjunto.con) >= 1:
        ''' "conjunto" tiene estados, por tanto se añade al final el nuevo AFN '''
        conjunto.con.insert(numCrear + 1, AFN(x, symbol, {x, x1}, {x1}, numAFNCreados))
    else:
        ''' "conjunto" no tiene estados, por tanto se añade al principio '''
        conjunto.con = [AFN(x, symbol, {x, x1}, {x1}, numAFNCreados)]

    numCrear += 2
    print("creando AFN...")
    time.sleep(1)
    print("¡AFN creado con éxito!\n")

    return numCrear

def Unir(id1, id2, conjunto, numCrear):
    ''' El siguiente ciclo es para vaciar "conjunto.con", sacando cada AFN, para así buscar los 2 AFN a unir,
                si se encuentran, se almacenan en "af1" y "af2", sino, se van guardando en "aux2" para después volver a
                guardar en conjunto.con todos los AFN sacados '''
    aux2 = []
    contador = 1
    while (len(conjunto.con) >= 1):
        aux = conjunto.con.pop()
        if aux.idAFN == id1:
            af1 = aux
        elif aux.idAFN == id2:
            af2 = aux
        else:
            aux2.insert(contador, aux)
            contador += 1

    contador = 1
    ''' Añadiendo el estado inicial "x" de la operación unión '''
    x = Estado(0, set(), True, False, 10)
    ''' Creando AFN "noms" que será la unión de af1 y af2, con estado inicial "x" '''
    noms = []
    noms.insert(contador - 1, x)
    contador += 1

    ''' Sacando cada estado del af1 y luego del af2 para tenerlos en el nuevo AFN "noms" '''
    while (len(af1.edosAFN) >= 1):
        val = af1.edosAFN.pop()
        val.identificador = contador - 1
        val.edoFinal = False
        val.edoInicial = False
        noms.insert(contador, val)
        contador += 1
    while (len(af2.edosAFN) >= 1):
        val = af2.edosAFN.pop()
        val.identificador = contador - 1
        val.edoFinal = False
        val.edoInicial = False
        noms.insert(contador, val)
        contador += 1

    ''' Añadiendo el estado final al AFN "noms" '''
    x1 = Estado(contador - 1, set(), False, True, 20)
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

    ''' Regresando los AFN que no se ocuparon a "conjunto.con" '''
    while (len(aux2) >= 1):
        aux = aux2.pop()
        aux.idAFN = contador
        conjunto.con.insert(contador - 1, aux)
        contador += 1

    ''' Añadiendo el nuevo AFN a "conjunto.con" '''
    conjunto.con.insert(contador - 1, AFN(x, symbol, noms, {x1}, contador))
    contador = 1
    numCrear -= 1

    print("uniendo AFN...")
    time.sleep(1)
    print("¡Nuevo AFN creado con éxito!\n")

    return numCrear

def cerraduraEpsilon (y):
    k=0
    conjunto_estadosS = []
    conjunto_estadosR = [] #Resultados
    conjunto_estadosS.append(y)
    ##Mientras la lista no este vacia
    while ( conjunto_estadosS):
        #Hacemos la transicion en todos los estados entregados
        aux = conjunto_estadosS.pop()
        conjunto_estadosR.append(aux)
        while (1 <= len(totalestados)-1 ):
            #Sacamos un estado 
            z = totalestados.pop()
            #Obtenemos un estado de la lista
            if (x.transiciones=='' and z.transiciones == ''):
                if (z in conjunto_estadosR):
                    continue
                else:
                    conjunto_estadosR.append(z)
            else:
                continue
        k=0
    return conjunto_estadosR #RETONAMOS EL CONJUNTO DE ESTADOS

'''def cerraduraEpsilonconjuntos (y = []):
    conjunto_estadosC = y.copy()
    x=
    conjunto_estadosR = []
    while (con)'''

def opMover(e, y):
    conjuntoR = []
    transiciones = e.transiciones
    for z in transiciones:
        if (z == y):
            conjuntoR.append(z)
    return conjuntoR 

def opMoverconjunto(A, y):
    conjuntoR = []
    auxlista = A.copy()
    for z in auxlista:
        conjuntoR.append (opMover(z, y))
    return conjuntoR

'''
x = Estado (1, set (), True, False, 10)
x1 = Estado (2, set (), False, False, 11)
y = Transicion ('c', x1)
z = AFN (x, 'abcdef', {x, x1}, {}, 1)

x.addTransicion (y)

print (x)
print (x1)
print (y)
print (z)

totalEstados = [x, x1]

cerraduraEpsilon (x)'''

numAFNCreados = 1
conjunto = conjuntoAFN
numCrear = 0
print("\n¡Hola!, Bienvenido al programa de análisis léxico")

while True:
    menu()
    opcionMenu = input("")

    if opcionMenu == "1":
        Tabla1(conjunto, numCrear)

    elif opcionMenu == "2":
        print("\nPara crear el AFN, escribe el carácter al cual crearle el AFN:")
        symbol = str(input(""))[0]
        numCrear = Crear(symbol, conjunto, numCrear)
        numAFNCreados += 1

    elif opcionMenu == "3":
        print("\nIngresa el id del primer AFN a unir:")
        id1 = int(input(""))
        print("\nIngresa el id del segundo AFN a unir:")
        id2 = int(input(""))
        numCrear = Unir(id1, id2, conjunto, numCrear)

    elif opcionMenu == "4":
        print("\nIngresa el id del primer AFN a concatenar:")
        id1 = int(input(""))
        print("\nIngresa el id del segundo AFN a concatenar:")
        id2 = int(input(""))
        Concatenar (id1, id2, conjunto)
        print("¡Nuevo AFN creado con éxito!\n")

    elif opcionMenu == "5":
        print("\nIngresa el id del AFN al cual obtener la cerradura transitiva:")
        id1 = int(input(""))
        CerrTransitiva (id1, conjunto)
        print("¡Nuevo AFN creado con éxito!\n")

    elif opcionMenu == "6":
        print("\nIngresa el id del AFN al cual obtener la cerradura de kleene:")
        print("¡Nuevo AFN creado con éxito!\n")
    elif opcionMenu == "7":
        print("\nIngresa el id del AFN al cual obtener la operación opcional:")
        print("¡Nuevo AFN creado con éxito!\n")
    elif opcionMenu == "8":
        print("\nIngresa el id del primer AFN a unir para el análisis léxico:")
        print("¡Nuevo AFN creado con éxito!\n")
    elif opcionMenu == "9":
        print("\nIngresa el id del AFN a convertir a un AFD:")
        print("¡Nuevo AFD creado con éxito!\n")
    elif opcionMenu == "10":
        print("\nIngresa el id del AF a introducir una cadena:")
        print("¡Prueba concluida con éxito!\n")
    elif opcionMenu == "11":
        break
    else:
        print("\nNo es una opción válida\npulsa una tecla para continuar...")
        input("")
