import copy
import random
import matplotlib.pyplot as plt
import ej3 as simulated_annealing
from time import time
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
    # print("en fitnes")
    for index in range(0, len(lista_productos)):
        lista_productos[index].ubicacion = individuo[index]
    f = 0
    estado_actual = []
    # print(individuo)
    for index, ordenes in enumerate(lista_ordenes):
        for ind, orden in enumerate(ordenes):
            for lugar, producto in enumerate(lista_productos):
                if orden.tipo == producto.tipo:
                    orden.ubicacion = producto.ubicacion
                #     print("orden ---- producto")
                # print(orden.tipo, orden.ubicacion, producto.tipo, producto.ubicacion)
            estado_actual.append(copy.deepcopy(orden.ubicacion))
        # print("estado actual")
        # print(estado_actual)
        solucion = simulated_annealing.recocido_simulado(simulated_annealing.Nodo(estado_actual), mapa)


        f = f + solucion.E
        # print("En fitnes: f , iteracion",f,index)
        estado_actual.clear()
    f = f/len(lista_ordenes)
    # print(f)
    return f


def AG(tamaño_poblacion,cant_interaciones, lista_productos, lista_ordenes, mapa,arc):
    print("En algo genetico")
    poblacion = []
    semilla = []
    k=0
    #Poblacion Inicial

    au = lista_productos[0].ubicacion
    lista_productos[0].ubicacion = lista_productos[1].ubicacion
    lista_productos[1].ubicacion = au
    # print(lista_productos[0].tipo, lista_productos[0].ubicacion, lista_productos[-1].ubicacion)

    for index in range(1, len(lista_productos)):
        semilla.append(copy.deepcopy(lista_productos[index].ubicacion))

    for i in range(0, tamaño_poblacion):
        random.shuffle(semilla)
        semilla.insert(0, lista_productos[0].ubicacion)

        poblacion.append(copy.deepcopy(Individuo(semilla)))
        del semilla[0]

    vector_fitness = []
    vector_fitness_mejor_hijo = []
    while 1:
        #Calculo la idoneidad de mi poblacion

        promedio_fitness = 0
        for index, item in enumerate(poblacion):
            #print(len(item.estado))
            # print(item.idoneidad)
            poblacion[index].idoneidad = fitness(item.estado, lista_productos, lista_ordenes, mapa)
            # print(poblacion[index].idoneidad)
            promedio_fitness = promedio_fitness + poblacion[index].idoneidad
        promedio_fitness = promedio_fitness /tamaño_poblacion
        poblacion.sort(key=lambda Individuo: Individuo.idoneidad)
        vector_fitness_mejor_hijo.append(copy.deepcopy(poblacion[0].idoneidad))
        vector_fitness.append(promedio_fitness)
        # print("promedio fitness")
        # print(promedio_fitness)
        # print("individuo 1")
        # print(poblacion[0].estado)
        # print("fitness individuo 1")
        # print(poblacion[0].idoneidad)
        # print("iteracion")
        # print(k)
        # print(" posicion producto 0")
        # print(poblacion[0].estado[0])

        # print("largo pobracion")
        # print(len(poblacion))
        # print("la poblacion es")
        # for i in poblacion:
        #     print(i.estado, i.idoneidad)
        # print("-----------------")
        if k%4 == 0:
            arc.write("fitness mejor individuo: \n")
            arc.write(str(poblacion[0].idoneidad))
            arc.write("\n")
            arc.write("Iteracion \n")
            arc.write(str(k))
            arc.write("Posicion producto 0: \n")
            arc.write(str(poblacion[0].estado[0]))
            arc.write("\n")
        if k >= cant_interaciones:
            break
        del poblacion[int(tamaño_poblacion/2+1):]#elijo los n/2 mejores padres

        # nueva_generacion = []

        #Paso los primeros 4 padres a la otra generacion
        nueva_generacion = [n for j, n in enumerate(poblacion) if j < 4]

        #Realizo crossover debo cambiarlo
        for i in range(2, len(poblacion)-1):
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
            # print("crossover .......................")
            # print(estado_aux_derecha)
            # print(estado_aux_izquierda)



            estado_aux_izquierda_2 = estado_aux_derecha_2[len(estado_aux_derecha_2[index_1:]):]
            del estado_aux_derecha[len(estado_aux_derecha[index_1:]):]
            del estado_aux_derecha_2[len(estado_aux_derecha_2[index_1:]):]
            hijo_1 = estado_aux_izquierda + hijo_1 + estado_aux_derecha
            hijo_2 = estado_aux_izquierda_2 + hijo_2 + estado_aux_derecha_2

            # print("valores izq_, derecha_")
            # print(estado_aux_izquierda, estado_aux_derecha)

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



        #Mutaciones por Intercambio con probabilidad del 15%

        for index, hijo in enumerate(nueva_generacion):
            # print("Epoca de mutacion")
            if random.random() < 0.2:
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

        poblacion.clear()
        # print("nueva gene",len(nueva_generacion))
        poblacion = copy.deepcopy(nueva_generacion)
        # print(len(poblacion))
        nueva_generacion.clear()

        k+=1
    arc.write("El vector de promedio de fitness: \n")
    arc.write(str(vector_fitness))
    arc.write("\n")
    arc.write(str(vector_fitness_mejor_hijo))
    arc.write("\n")



    fig, axes = plt.subplots()

    axes.set_xlabel('Iteraciones')

    axes.set_ylabel('Fitness')

    axes.set_title('Fitness almacen')

    plt.plot([n for n in range(0, len(vector_fitness))],vector_fitness, label="Fitness promedio")

    plt.plot([n for n in range(0, len(vector_fitness_mejor_hijo))],vector_fitness_mejor_hijo, label="Mejor Fitness")

    plt.legend()

    plt.show()
    return poblacion[0]








def main():
    t_ini = time()
    arc = open("AG.txt", "w")
    #Genero layout
    mapa = simulated_annealing.a_star.hacer_mapa(6, 5)
    arc.write("El mapa del deposito es:\n")
    for i in range(0, len(mapa)):
        arc.write(str(mapa[i]))
        arc.write("\n")
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
    # orden = [n for index, n in enumerate(lista_productos) if index < 4]
    # lista_ordenes.append(orden)
    for j in range(0, 1):
        for i in range(0, random.randint(5, 12)):
            if random.random() < 0.30:
                orden.append(copy.deepcopy(lista_productos[0])) #El producto 0 tiene 35% de probabilidad de ser elegido
            else:
                orden.append(copy.deepcopy(random.choice(lista_productos)))
        random.shuffle(orden)
        lista_ordenes.append(copy.deepcopy(orden))
        orden.clear()

    arc.write("Las ordenes del ultimo año fueron:\n")
    for index, valor in enumerate(lista_ordenes):
        # print("[", end=' ')
        arc.write("[ ")
        for ind, valo in enumerate(valor):
            if ind == (len(valor)-1):
                # print(valo.tipo, end=' ')
                arc.write(str(valo.tipo))
            else:
                # print(valo.tipo, end=' -> ')
                arc.write(str(valo.tipo))
                arc.write("-> ")
        arc.write("] \n")

    solucion = AG(6, 26, lista_productos, lista_ordenes, mapa,arc)

    print(solucion.estado, solucion.idoneidad)
    arc.write("La solucion es: \n")
    arc.write(str(solucion.estado))
    arc.write(", ")
    arc.write(str(solucion.idoneidad))
    arc.write("\n")
    t_fin = time()
    arc.write("Tiempo de ejecucion \n")
    t__ = t_fin-t_ini
    arc.write(str(t__))
    arc.close()
if __name__ == '__main__':
    main()