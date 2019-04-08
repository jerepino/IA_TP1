import random
import math
import copy
import ej2 as a_star
class Nodo:
    def __init__(self, estado=None, E = 0):
        self.estado = estado
        self.E = E


def calculo_E(estado, mapa):
    E = 0
    # print("Calculo E")
    for index in range(0, len(estado)-1):
        aux_1 = estado[index]
        aux_2 = estado[index + 1]
        mapa[aux_2[0]][aux_2[1]] = 0
        E = E + len(a_star.a_estrella(mapa, aux_1, aux_2))
        # print(E)
        mapa[aux_2[0]][aux_2[1]] = 1
    return E


def calculo_T(t):
    alpha = 0.99
    return t*alpha

def recocido_simulado(actual, mapa,t=200):
    bahia_carga = (5, 0)
    actual.estado.insert(0, bahia_carga)
    actual.estado.append(bahia_carga)
    actual.E = calculo_E(actual.estado, mapa)

    mejor_nodo = copy.deepcopy(actual)
    while (1):
        T = calculo_T(t)
        if T <= 0.01:
            return mejor_nodo

        #Para generar vecinos permuto 2 valores aleatoriamente
        nuevo = Nodo(copy.deepcopy(actual.estado))
        index_1 = random.randint(1, len(nuevo.estado) - 2) #El ultimo y el primer punto son la bahia de carga
        index_2 = random.randint(1, len(nuevo.estado) - 2)
        aux = nuevo.estado[index_1]
        nuevo.estado[index_1] = nuevo.estado[index_2]
        nuevo.estado[index_2] = aux
        nuevo.E = calculo_E(nuevo.estado, mapa)

        dE = nuevo.E-actual.E

        if dE < 0:
            actual = nuevo

        elif dE > 0:
            if math.e**(-dE/T) > random.random():
                # print("Salto a peor estado")
                actual = nuevo
        # print("E Acutal")
        # print(actual.E)
        if mejor_nodo.E > actual.E:
            mejor_nodo = actual
        # print("E Mejor nodo")
        # print(mejor_nodo.E)

        t = T

#Agregar print para demostrar que va disminuyendo la energia
def main():
    posicion_paquetes = []
    mapa = a_star.hacer_mapa(11, 9)
    print("El mapa del deposito es:")
    for i in range(0, len(mapa)):
        print(mapa[i])
    for y, valor in enumerate(mapa):
        for x, val in enumerate(valor):
            if x%2 != 0:
                if val == 1 or valor == 1:
                    posicion_paquetes.append((y, x))


    # posicion_paquetes = random.sample(posicion_paquetes, k=random.randint(0,len(posicion_paquetes)))

    posicion_paquetes = [(1,1), (8,7), (2,5), (8,3), (2,3), (9,5), (1,1), (1,1), (6,5), (1,1), (4,5), (1,1)]
    print(posicion_paquetes)
    inicio = Nodo(posicion_paquetes)
    # print(inicio.estado)
    solucion = recocido_simulado(inicio, mapa)


    print("la solucion")
    print(solucion.estado)
    print(solucion.E)
    for i in range(0, len(mapa)):
        for index, item in enumerate(solucion.estado):
            mapa[item[0]][item[1]] = index

    print("El mapa solucion es:")
    for i in range(0, len(mapa)):
        print(mapa[i])


if __name__ == '__main__':
    main()
