import copy
from math import fabs
class Nodo:
    def __init__(self, posicion=None, padre=None, g=0, h=0):
        self.posicion = posicion  #es la posicion actual
        self.padre = padre  #es un objeto nodo
        self.g = g
        self.h = h
        self.f = g+h

    def __lt__(self, nodo_):
        return self.f < nodo_.f


    def __eq__(self, nodo_):
        return self.posicion == nodo_


def heuristica(pos_ac, pos_fin):
    h = 0
    for i in range(0, len(pos_ac)):
        h = h + fabs(pos_fin[i]-pos_ac[i])
    return h


def hacer_mapa(largo, ancho):

    lista_de_cajas = []
    lista_de_cajas_2 = []
    columna=[None] * ancho
    fila = [None] * largo

    for k in range(0,ancho):
        lista_de_cajas.append(k*4)

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




def a_estrella(mapa, inicio, fin):
    lista_abierta = []
    lista_cerrada = []
    nodo_inicio = Nodo(inicio, None, 0, heuristica(inicio, fin))
    lista_abierta.append(nodo_inicio)
    while len(lista_abierta) > 0:
        lista_abierta.sort(key=lambda nodo: nodo.f)
        nodo_actual = lista_abierta[0]

        if nodo_actual.posicion == fin:
            camino = []
            actual = nodo_actual
            while actual.padre is not None:
                camino.append(actual.posicion)
                actual = actual.padre
            camino.append(actual.posicion) #agrego el nodo inicial al camino
            camino.reverse()
            return camino

        lista_abierta.pop(0)
        lista_cerrada.append(nodo_actual)

        #Genero vecinos

        hijos = []
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            posicion = (nodo_actual.posicion[0]+i[0], nodo_actual.posicion[1]+i[1])

            if posicion[0] > (len(mapa)-1) or posicion[0] < 0 or posicion[1] > (len(mapa[0])-1) or posicion[1] < 0:
                continue
            if mapa[posicion[0]][posicion[1]] == 1:
                continue
            nueva_posicion = Nodo(posicion, nodo_actual)
            hijos.append(nueva_posicion)
        for vecino in hijos:
            if vecino in lista_cerrada:
                continue
            if vecino not in lista_abierta:
                vecino.g = nodo_actual.g + 1
                vecino.h = heuristica(vecino.posicion,fin)
                vecino.f = vecino.g + vecino.h
                lista_abierta.append(vecino)
            elif vecino.g < lista_abierta[lista_abierta.index(vecino.posicion)].g: #si esta en la lista y el valor de g para llegar a ese nodo es menor, lo remplazo
                lista_abierta[lista_abierta.index(vecino.posicion)] = vecino






def main():

    #mapa = hacer_mapa(6, 4)
    #inicio = (0, 0)
    #fin = (4, 3)
    objetivo = a_estrella(mapa, inicio, fin)

    print("El mapa del deposito es:")
    for i in range(0,len(mapa)):
        print(mapa[i])
    print("El recorrido al objetivo es:")
    print(objetivo)

if __name__ == '__main__':
   main()