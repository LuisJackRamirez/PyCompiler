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
    print("\t5 - Cerradura transitiva de un AFN")
    print("\t6 - Cerradura de kleene de un AFN")
    print("\t7 - operación opcional de un AFN")
    print("\t8 - Unión 2 o más AFN para el análisis léxico")
    print("\t9 - Convertir un AFN a un AFD")
    print("\t10 - Hacer una prueba con una cadena en un AF")
    print("\t11 - salir")

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

conjunto = conjuntoAFN
contador = 1
numCrear = 0
print("\n¡Hola!, Bienvenido al programa de análisis léxico")

while True:
    menu()

    opcionMenu = input("")

    if opcionMenu == "1":
        if numCrear == 0:
            print("\nNo hay AF's por mostrar")
        else:
            edos = ""
            f = ""
            tabla = [['Id', 'Alfabeto', 'Estados','Estado inicial', 'Estados Finales']]
            nuevaLista = []
            contador2 = 1
            final = []
            aux2 = []
            '''Se debe extraer los AF antes de la tabla, pues si no, saldrán al final todos al revés'''
            while(len(conjunto.con) >= 1):
                aux = conjunto.con.pop()
                aux2.insert(contador2, aux)
                contador2 += 1
            contador2 = 1
            while (len(aux2) >= 1):
                aux = aux2.pop()
                '''extraer id del estado inicial'''
                Sfinal = str(aux.S.identificador)
                '''extraer id de todos los edos del AFN'''
                todo = []
                todoFinal = ""
                edosFinales = ""
                num = []
                num2 = []

                while (len(aux.edosAFN) >= 1):
                    # for j in aux.edosAFN:
                    finales = aux.edosAFN.pop()
                    num.append(finales.identificador)
                    if finales.edoFinal == True:
                        num2.append(finales.identificador)
                    todo.insert(contador, finales)
                    contador += 1

                contador = 1
                aux.edosAFN = todo
                num = sorted(num)
                num2 = sorted(num2)

                for i in range(0, len(num) - 1):
                    todoFinal += str(num[i]) + ", "
                todoFinal += str(num[len(num)-1])
                for i in range(0, len(num2) - 1):
                    edosFinales += str(num2[i]) + ", "
                edosFinales += str(num2[len(num2)-1])

                afs = [str(aux.idAFN), repr(aux.E), todoFinal, Sfinal, edosFinales]
                tabla.append(afs)
                nuevaLista.insert(contador2 ,aux)
                contador2 += 1

            conjunto.con = nuevaLista
            print(tabulate(tabla, headers='firstrow', stralign='center', tablefmt='fancy_grid'))
    elif opcionMenu == "2":
        print("\nPara crear el AFN, escribe el carácter al cual crearle el AFN:")
        symbol = str(input(""))[0]
        x = Estado(0, set(), True, False, 10)
        x1 = Estado(1, set(), False, True, 20)

        if len(conjunto.con) >= 1:
            conjunto.con.insert(numCrear + 1, AFN(x, symbol, {x, x1}, {x1}, 1+numCrear))
        else:
            conjunto.con = [AFN(x, symbol, {x, x1}, {x1}, 1+numCrear)]
        numCrear += 1
        print("creando AFN...")
        time.sleep(1)
        print("¡AFN creado con éxito!\n")
    elif opcionMenu == "3":
        print("\nIngresa el id del primer AFN a unir:")
        id1 = int(input(""))
        print("\nIngresa el id del segundo AFN a unir:")
        id2 = int(input(""))

        aux2 = []
        lista = []
        while (len(conjunto.con) >= 1):
            aux = conjunto.con.pop()
            lista.append(aux.idAFN)
            if aux.idAFN == id1:
                af1 = aux
            elif aux.idAFN == id2:
                af2 = aux
            else:
                aux2.insert(contador, aux)
                contador += 1
        contador = 1
        lista = sorted(lista)

        x = Estado(0, set(), True, False, 10)
        noms = []
        noms.insert(contador-1,x)
        contador += 1
        flg = 0

        while(len(af1.edosAFN) >= 1):
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

        x1 = Estado(contador-1, set(), False, True, 20)
        symbol = af1.E + "," + af2.E

        noms.insert(contador, x1)
        contador = 1

        if af1.idAFN <= af2.idAFN:
            identif = af1.idAFN
        else:
            identif = af2.idAFN

        flag = 0
        while (len(aux2) >= 1):
            aux = aux2.pop()
            if aux.idAFN != lista[contador-1]:
                conjunto.con.insert(contador-1, AFN(x, symbol, noms, {x1}, identif))
                flag = 1
                contador += 1
                conjunto.con.insert(contador - 1, aux)
            else:
                conjunto.con.insert(contador-1, aux)
            contador += 1
        if flag == 0:
            conjunto.con.insert(contador - 1, AFN(x, symbol, noms, {x1}, identif))
        contador = 1
        numCrear -= 1
        print("uniendo AFN...")
        time.sleep(1)
        print("¡Nuevo AFN creado con éxito!\n")
    elif opcionMenu == "4":
        print("\nIngresa el id del primer AFN a concatenar:")
        print("¡Nuevo AFN creado con éxito!\n")
    elif opcionMenu == "5":
        print("\nIngresa el id del AFN al cual obtener la cerradura transitiva:")
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
