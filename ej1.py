import  copy
class Nodo():
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





def main():

    posicion_inicio = [0, 0, 0, 0, 0, 0]
    posicion_fin = [1, 2, 3, 4, 5, 6]
    g=0
    h=heuristica(posicion_inicio, posicion_fin)
    lista_abierta = list()
    lista_cerrada = list()
    vengo_de = list()
    list_hijos = list()
    lista_abierta.append(copy.deepcopy(Nodo(posicion_inicio,g,h)))
    k=0
    while(len(lista_abierta)>0):


        lista_abierta.sort(key=lambda nodo_: nodo_.f) # Ordeno el vector de menor a mayor f
        # print(lista_abierta[0].f)
        nodo_actual = copy.deepcopy(lista_abierta[0])

        if nodo_actual.posicion == posicion_fin:
            print("Tenemos solucion")
            break
        lista_abierta.clear()
        lista_cerrada.append(copy.deepcopy(nodo_actual))
        #lista_cerrada.append(copy.deepcopy(
        #    lista_abierta.pop(0)))  # Como esta ordenado es equivalente a mover el valor del min f

        pos_actual = nodo_actual.posicion
        pos_hijo = [0,0,0,0,0,0]


        for k in range(-1,2,2):
            for i in range(0,6,1):
                for j in range(0,6,1):
                    if i == j:
                        pos_hijo[i] = pos_actual[i]+k
                    else:
                        pos_hijo[j] = pos_actual[j]
                list_hijos.append(copy.deepcopy(pos_hijo))
        print(len(list_hijos))
        g_t = nodo_actual.g + 1
        for i in range(len(list_hijos)):

            if list_hijos[i] in lista_cerrada:

                continue


            if list_hijos[i] not in lista_abierta:

              h = heuristica(list_hijos[i], posicion_fin)
              lista_abierta.append(copy.deepcopy(Nodo(list_hijos[i], g_t, h)))
            elif g_t>= lista_abierta[len(lista_abierta)-1].g:
                continue
        vengo_de.append(copy.deepcopy(min(lista_abierta)))

        list_hijos.clear()

    print("El camino es")
    for j in vengo_de:
        print(j.posicion)


if __name__ == '__main__':
        main()
