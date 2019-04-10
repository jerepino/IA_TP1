import  copy
import  random
import matplotlib.pyplot as plt
from math import fabs




class Nodo:
    def __init__(self, posicion_,g_,h_):
        self.posicion = posicion_
        self.g=g_
        self.h=h_
        self.f=g_+h_

    def __gt__(self, nodo_):
        return self.f > nodo_.f

    def __lt__(self, nodo_):
        return self.f < nodo_.f

    def __ge__(self, nodo_):
        return self.f >= nodo_.f

    def __le__(self, nodo_):
        return self.f <= nodo_.f

    def __eq__(self, nodo_):
        return self.f == nodo_.f

    def __eq__(self, nodo_):
        return self.posicion == nodo_


    def __ne__(self, nodo_):
        return self.f != nodo_.f

    def __ne__(self, nodo_):
        return self.posicion != nodo_

def heuristica(posicion_actual,posicion_fin):
        hh=0
        for i in range(0,len(posicion_actual),1):
                hh=(posicion_fin[i]-posicion_actual[i])**2+hh
        h=hh**0.5

        return h

"""
#DISTANCIA DE MANHATTAN
def heuristica(posicion_actual, posicion_fin):
    h = 0
    for i in range(0, len(posicion_actual)):
        h = h + fabs(posicion_fin[i]-posicion_actual[i])
    return h

# Chebyshev distance
def heuristica(posicion_actual, posicion_fin):
    h=0
    lista = []
    for i in range(0, len(posicion_actual)):

       lista.append(fabs(posicion_fin[i]-posicion_actual[i]))
       h=max(lista)

    return h

"""

def main():

    posicion_inicio = []
    posicion_fin = []
    obstaculos = []
    aux = []

    #Genero coordenadas de incio y fin aleatorias
    for index in range(0, 6):
        posicion_inicio.append(random.randint(0, 10))
        posicion_fin.append(random.randint(0, 10))
        #Genero obstaculos. Me aseguro de que los obstaculos esten entre la posicion inicial y final
        for p in range(0, 6):
            if posicion_inicio[index] > posicion_fin[index]:
                aux.append(random.randint(posicion_fin[index], posicion_inicio[index]))
            elif posicion_inicio[index] < posicion_fin[index]:
                aux.append(random.randint(posicion_inicio[index], posicion_fin[index]))
            else:  #Componentes iguales
                aux.append(random.randint(0, 10))   #Es un bucle anidado. => aux tiene 36 componentes
    #Agrego los obstaculos (son 6)
    for p in range(0, 6):
        obstaculos.append([aux[p],aux[p+6],aux[p+12],aux[p+18],aux[p+24],aux[p+30]])

    print("Posicion inicial:")
    print(posicion_inicio)
    print("Posiciion final:")
    print(posicion_fin)
    print("Los obstaculos son:")
    print(obstaculos)

    lista_abierta = []
    lista_cerrada = []
    vengo_de = []
    list_hijos = []


    g = 0
    h = heuristica(posicion_inicio, posicion_fin)
    lista_abierta.append(copy.deepcopy(Nodo(posicion_inicio, g, h)))
    vengo_de.append(copy.deepcopy(Nodo(posicion_inicio, g, h)))

    while(len(lista_abierta)>0):

        #key=lambda me permite declarar que atributo utilizo como referencia para ordenar la lista
        #En este caso la herustica

        lista_abierta.sort(key=lambda nodo_: nodo_.f) # Ordeno el vector de menor a mayor f

        nodo_actual = copy.deepcopy(lista_abierta[0]) #mejor nodo de mi lista abierta

        if nodo_actual.posicion == posicion_fin:
            print("Tenemos solucion")
            break
        lista_abierta.clear() # Vacio la lista abierta. Esto lo hago porque en esta lista coloco todos mis nodos hijos.
        lista_cerrada.append(copy.deepcopy(nodo_actual)) #Paso mi nodo actual (el mejor) a lista cerrada
        #lista_cerrada.append(copy.deepcopy(
        #    lista_abierta.pop(0)))  # Como esta ordenado es equivalente a mover el valor del min f

        pos_actual = nodo_actual.posicion
        pos_hijo = [0,0,0,0,0,0]

        #Genero mis hijos ( los genero  aumentando o disminuyendo 1° de a una a la vez todas las articulaciones del robot)
        for k in range(-1, 2, 2):
            for i in range(0, 6):
                for j in range(0, 6):
                    if i == j:
                        pos_hijo[i] = pos_actual[i]+k
                    else:
                        pos_hijo[j] = pos_actual[j]
                list_hijos.append(copy.deepcopy(pos_hijo))

        g_t = nodo_actual.g + 1 #El costo camino de todos los hijos va a ser 1+ que el del padre (supongo costo unitario)
        #Recorro mis hijos y si no los he explorado, los agrego a la lista abierta
        for i in range(len(list_hijos)):

            if list_hijos[i] in lista_cerrada: #si ya explore mi hijo, no lo agrego
                continue
            if (list_hijos[i] not in lista_abierta): #si no esta en la lista abierta lo agrego (ningun hijo al principio lo esta)
              if  list_hijos[i] in obstaculos: #verifico que no sea un obstaculo
                  continue

              h = heuristica(list_hijos[i], posicion_fin)
              lista_abierta.append(copy.deepcopy(Nodo(list_hijos[i], g_t, h)))
        vengo_de.append(copy.deepcopy(min(lista_abierta))) #Elijo el mejor de mis hijos y lo guardo en mi lista para encontrar el camino

        list_hijos.clear()

    print("El camino es")
    for j in vengo_de:
        print(j.posicion)

    #Graficamos
    a=[]
    b=[]
    for index, item in enumerate(vengo_de):
        a.append(index)
        b.append(item.f)

    figura = plt.plot(a,b)
    plt.show()



if __name__ == '__main__':
        main()
