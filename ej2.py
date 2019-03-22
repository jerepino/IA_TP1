import copy
from math import fabs
class Nodo():
    def __init__(self, posicion, g, h):
        self.posicion = posicion
        self.g = g
        self.h = h
        self.f = g+h


def heuristica(pos_ac, pos_fin):
    h = 0
    for i in range(0, len(pos_ac)):
        h = h + fabs(pos_fin[i]-pos_ac[i])
    return h


def hacer_mapa(ancho,largo):

    lista_de_cajas = []
    lista_de_cajas_2 = []
    columna=[None] * ancho
    fila = [None] * largo

    for k in range(0,ancho):
        lista_de_cajas.append(k*3)

    for k in range(0,largo):
        lista_de_cajas_2.append(k * 5)

    for j in range(0,largo):
        for i in range(0,ancho):
            if i in lista_de_cajas:

                columna[i] = 0
            elif j in lista_de_cajas_2:

                columna[i] = 0
            else:
                columna[i] = 1
        fila[j] = copy.deepcopy(columna)

    return fila


def main():

    mapa = hacer_mapa(10, 16)

    for i in range(0,len(mapa)):
        print(mapa[i])
if __name__ == '__main__':
   main()