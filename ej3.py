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
    for index in range(0, len(estado)-1):
        aux_1 = estado[index]
        aux_2 = estado[index + 1]

        mapa[aux_2[0]][aux_2[1]] = 0
        aaa = a_star.a_estrella(mapa, aux_1, aux_2)
        # print(aaa)
        E = E + len(aaa)
        aaa.clear()

        mapa[aux_2[0]][aux_2[1]] = 1
    return E


def calculo_T(t):
    alpha=0.99
    return t*alpha

def recocido_simulado(actual, mapa):
    actual.E = calculo_E(copy.deepcopy(actual.estado), mapa)
    t = 1000

    while (1):
        T = calculo_T(t)
        if T <= 0.1:
            return actual.estado
        #Para generar vecinos permuto 2 valores aleatoriamente
        nuevo_aux = Nodo(copy.deepcopy(actual.estado))
        index_1 = random.randint(0, len(nuevo_aux.estado) - 1)
        index_2 = random.randint(0, len(nuevo_aux.estado) - 1)
        aux = nuevo_aux.estado[index_1]
        nuevo_aux.estado[index_1] = nuevo_aux.estado[index_2]
        nuevo_aux.estado[index_2] = aux
        nuevo = Nodo(copy.deepcopy(nuevo_aux.estado))
        nuevo.E = calculo_E(copy.deepcopy(nuevo.estado), mapa)

        dE = actual.E-nuevo.E

        if dE > 0:

            actual = copy.deepcopy(nuevo)
        elif 1-math.e**(-dE/T) >= random.uniform(0, 1):

            actual = copy.deepcopy(nuevo)
        t = T


def main():
    posicion_paquetes = []
    mapa = a_star.hacer_mapa(6, 5)
    print("El mapa del deposito es:")
    for i in range(0, len(mapa)):
        print(mapa[i])
    for y, valor in enumerate(mapa):
        for x, val in enumerate(valor):
            if x%2 != 0:
                if val == 1 or valor == 1:
                    posicion_paquetes.append((y, x))
    inicio = Nodo(random.sample(posicion_paquetes, k=len(posicion_paquetes)))
    solucion = recocido_simulado(inicio, mapa)


    print("la solucion")
    print(solucion)



if __name__ == '__main__':
    main()

