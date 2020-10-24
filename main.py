from Estado import Estado
from Transicion import Transicion
from AFN import AFN

x = Estado (1, set (), True, False, 10)
x1 = Estado (2, set (), False, False, 11)
y = Transicion ('c', x1)
z = AFN (x, 'abcdef', {x, x1}, {}, 1)

x.addTransicion (y)

print (x)
print (x1)
print (y)
print (z)
