import copy
import random

import ej3 as simulated_annealing

class Producto():
    def __init__(self, tipo, ubicacion = None):
        self.tipo = tipo
        self.ubicacion = ubicacion
class Individuo():
    def __init__(self, estado=None, idoneidad=0):
        self.estado = estado
        self.idoneidad = idoneidad

    def __lt__(self, nodo_):
        return self.idoneidad < nodo_.idoneidad

def fitness(individuo, lista_productos, lista_ordenes, mapa):

    for index in range(0,len(lista_productos)):
        lista_productos[index].ubicacion = individuo[index]
    E = 0
    estado_actual = []
    for index, ordenes in enumerate(lista_ordenes):
        for ind, orden in enumerate(ordenes):
            for lugar, producto in enumerate(lista_productos):
                if orden.tipo == producto.tipo:
                    orden.ubicacion = producto.ubicacion

            estado_actual.append(copy.deepcopy(orden.ubicacion))
        solucion=simulated_annealing.recocido_simulado(simulated_annealing.Nodo(estado_actual), mapa)
        E = E + solucion.E
        estado_actual.clear()
    f = 1000 / E
    return f


def AG(tamaño_poblacion,cant_interaciones, lista_productos, lista_ordenes, mapa):
    print("En algo genetico")
    poblacion = []
    semilla = []
    k=0
    #Poblacion Inicial
    for index in range(0,len(lista_productos)):
        semilla.append(copy.deepcopy(lista_productos[index].ubicacion))

    for i in range(0, tamaño_poblacion):
        random.shuffle(semilla)
        poblacion.append(copy.deepcopy(Individuo(semilla)))



    while k < cant_interaciones:
        #Calculo la idoneidad de mi poblacion

        for index, item in enumerate(poblacion):
            poblacion[index].idoneidad = fitness(item.estado, lista_productos, lista_ordenes, mapa)

        poblacion.sort(key=lambda Individuo: Individuo.idoneidad, reverse=False)

        del poblacion[26:len(poblacion)] #elijo los n/2 mejores padres
        print(len(poblacion))
        nueva_generacion = []
        #Realizo crossover debo cambiarlo
        for i in range(0,len(poblacion)-1):
            nueva_generacion.append(copy.deepcopy(poblacion[i]))
            nueva_generacion.append(copy.deepcopy(poblacion[i+1]))
            inde = random.randint(0, len(poblacion[i].estado)-1)
            nueva_generacion[i].estado[inde:len(nueva_generacion[i].estado)] = copy.deepcopy(poblacion[i+1].estado[inde:len(poblacion[i+1].estado)])
            nueva_generacion[i+1].estado[inde:len(nueva_generacion[i+1].estado)] = copy.deepcopy(poblacion[i].estado[inde:len(poblacion[i].estado)])
        #Mutaciones con probabilidad del 15%
        for index, intem in enumerate(nueva_generacion):
            if random.random() < 0.15:
                index_1 = random.randint(1, len(item.estado) - 1)
                index_2 = random.randint(1, len(item.estado) - 1)
                aux = copy.deepcopy(item.estado[index_1])
                nueva_generacion[index].estado[index_1] = copy.deepcopy(item.estado[index_2])
                nueva_generacion[index].estado[index_2] = aux
        print(len(poblacion), len(nueva_generacion))
        poblacion.clear()
        poblacion = copy.deepcopy(nueva_generacion)
        nueva_generacion.clear()
        k+=1
    return poblacion[0]








def main():
    #Genero layout
    mapa = simulated_annealing.a_star.hacer_mapa(6,5)
    print("El mapa del deposito es:")
    for i in range(0, len(mapa)):
        print(mapa[i])

    #Genero lista de productos
    lista_productos = []
    tipo = 0
    for y, valor in enumerate(mapa):
        for x, val in enumerate(valor):
            if x%2 != 0:
                if val == 1 or valor == 1:
                    lista_productos.append(Producto(tipo, (y, x)))
                    tipo += 1
    #Genero ordenes del año pasado
    lista_ordenes = []
    orden = []
    for j in range(0, 10):
        for i in range(0, random.randint(1, 15)):
            orden.append(copy.deepcopy(random.choice(lista_productos)))
        random.shuffle(orden)
        lista_ordenes.append(copy.deepcopy(orden))
        orden.clear()

    print("Las ordenes del ultimo año fueron:")
    for index, valor in enumerate(lista_ordenes):
        print("[", end=' ')
        for ind, valo in enumerate(valor):
            if ind == (len(valor)-1):
                print(valo.tipo, end=' ')
            else:
                print(valo.tipo, end=' -> ')
        print("]")

    solucion = AG(50, 100, lista_productos, lista_ordenes, mapa)
    print(solucion.estado)
if __name__ == '__main__':
           main()