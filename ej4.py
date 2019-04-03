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
    f = 0
    estado_actual = []
    # print(individuo)
    for index, ordenes in enumerate(lista_ordenes):
        for ind, orden in enumerate(ordenes):
            for lugar, producto in enumerate(lista_productos):
                if orden.tipo == producto.tipo:
                    orden.ubicacion = producto.ubicacion
                    # print("orden ---- producto")
                # print(orden.tipo, orden.ubicacion, producto.tipo, producto.ubicacion)
            estado_actual.append(copy.deepcopy(orden.ubicacion))
        # print("estado actual")
        # print(estado_actual)
        solucion = simulated_annealing.recocido_simulado(simulated_annealing.Nodo(estado_actual), mapa)
        f = f + solucion.E
        estado_actual.clear()

    return f


def AG(tamaño_poblacion,cant_interaciones, lista_productos, lista_ordenes, mapa):
    print("En algo genetico")
    poblacion = []
    semilla = []
    k=0
    #Poblacion Inicial
    for index in range(0, len(lista_productos)):
        semilla.append(copy.deepcopy(lista_productos[index].ubicacion))

    for i in range(0, tamaño_poblacion):
        random.shuffle(semilla)
        poblacion.append(copy.deepcopy(Individuo(semilla)))

    vector_fitness = []
    while k < cant_interaciones:
        #Calculo la idoneidad de mi poblacion

        promedio_fitness = 0
        for index, item in enumerate(poblacion):
            poblacion[index].idoneidad = fitness(item.estado, lista_productos, lista_ordenes, mapa)
            promedio_fitness = promedio_fitness + poblacion[index].idoneidad
        promedio_fitness = promedio_fitness /tamaño_poblacion
        poblacion.sort(key=lambda Individuo: Individuo.idoneidad)
        vector_fitness.append(promedio_fitness)
        print(promedio_fitness)
        del poblacion[int(tamaño_poblacion/2+1):]#elijo los n/2 mejores padres

        nueva_generacion = []
        #Realizo crossover debo cambiarlo
        for i in range(0, len(poblacion)-1):
            index_1 = random.randint(1, len(poblacion[i].estado)-1)
            index_2 = random.randint(1, len(poblacion[i].estado)-1)
            if index_1 > index_2:
                auxx = index_1
                index_1 = index_2
                index_2 = auxx
            elif index_1 == index_2:
                index_1 -= 1

            hijo_1 = []
            hijo_2 = []
            hijo_1 = poblacion[i+1].estado[index_1:index_2]#[index_1, index_2)
            hijo_2 = poblacion[i].estado[index_1:index_2]
            # print(hijo_1)
            # print(hijo_2)
            estado_aux_derecha = [n for n in poblacion[i].estado if n not in hijo_1] #incluye index_2
            estado_aux_derecha_2 = [n for n in poblacion[i + 1].estado if n not in hijo_2]  # incluye index_2

            estado_aux_izquierda = estado_aux_derecha[len(estado_aux_derecha[index_1:]):] #[index2,fin]
            estado_aux_izquierda_2 = estado_aux_derecha_2[len(estado_aux_derecha_2[index_1:]):]
            del estado_aux_derecha[len(estado_aux_derecha[index_1:]):]
            del estado_aux_derecha_2[len(estado_aux_derecha_2[index_1:]):]
            hijo_1 = estado_aux_izquierda + hijo_1 + estado_aux_derecha
            hijo_2 = estado_aux_izquierda_2 + hijo_2 + estado_aux_derecha_2

            nueva_generacion.append(Individuo(copy.deepcopy(hijo_1)))
            nueva_generacion.append(Individuo(copy.deepcopy(hijo_2)))
            hijo_2.clear()
            hijo_1.clear()
            estado_aux_derecha.clear()
            estado_aux_derecha_2.clear()

            estado_aux_izquierda.clear()
            estado_aux_izquierda_2.clear()

            # print("crossover")
            # print(index_1, index_2)
            # print("padres")
            # print(poblacion[i].estado)
            # print(poblacion[i+1].estado)
            # print("hijo_1")
            # print(nueva_generacion[i*2].estado)
            # print("hijo_2")
            # print(nueva_generacion[(2*i+1)].estado)
            # print("valores izq_, derecha_")
            # print( estado_aux_izquierda,estado_aux_derecha)

        #Mutaciones por Intercambio con probabilidad del 15%

        for index, hijo in enumerate(nueva_generacion):
            # print("Epoca de mutacion")
            if random.random() < 0.01:
                # print("El individuo ", index, "esta mutando")
                # print(hijo.estado)
                pos_1 = random.randint(0, len(hijo.estado) - 1)
                pos_2 = random.randint(0, len(hijo.estado) - 1)
                if pos_1 == pos_2:
                    pos_1 = random.randint(0, len(hijo.estado) - 1)
                auxiliar = hijo.estado[pos_1]
                nueva_generacion[index].estado[pos_1] = hijo.estado[pos_2]
                nueva_generacion[index].estado[pos_2] = auxiliar
                # print("El resultado de la mutacion es")
                # print(nueva_generacion[index].estado)
        # print(len(poblacion), len(nueva_generacion))
        poblacion.clear()
        poblacion = copy.deepcopy(nueva_generacion)
        nueva_generacion.clear()
        k+=1
    print(vector_fitness)
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

    solucion = AG(20, 20, lista_productos, lista_ordenes, mapa)
    print(solucion.estado, solucion.idoneidad)
if __name__ == '__main__':
           main()