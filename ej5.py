import random
import copy
import math
class Tarea():
    def __init__(self,maquina, duracion=1, t_ini=0):
        self.maquina = maquina
        self.duracion = duracion
        self.t_ini = t_ini


def conflictos_(tarea, conficto, index_1, index_2):
    conflictos_maquina = []
    for numero_job, job in enumerate(conficto):
        for numero_tarea, tar in enumerate(job):
            if tar != tarea:
                    if tar.maquina == tarea.maquina:
                        if (tarea.t_ini < tar.t_ini) and (tar.t_ini < tarea.t_ini+tarea.duracion):
                            conflictos_maquina.append(tar)
                        elif (tarea.t_ini + tarea.duracion > tar.t_ini) and (tarea.t_ini < tar.t_ini + tar.duracion):
                            conflictos_maquina.append(tar)

    conflictos_tiempo = [tar for numero_tarea, tar in enumerate(conficto[index_1])
                         if (numero_tarea > index_2 and tar.t_ini < tarea.t_ini + tarea.duracion) or
                         (numero_tarea < index_2 and tar.t_ini + tar.duracion > tarea.t_ini)]
    conflictos_tarea = conflictos_maquina + conflictos_tiempo

    conflictos_tarea = set(conflictos_tarea)


    return list(conflictos_tarea)


def minimo_conflicto(tarea, conficto, index_1, index_2):

    #calculo energia inicial
    E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
    k=0


    while k < 100:
        if len(conflictos_(tarea, conficto, index_1, index_2)) == 0:

            return tarea
        #genero vecionos
        nuevo_vecino_1 = copy.deepcopy(tarea)
        nuevo_vecino_1.t_ini = k
        nuevo_vecino_2 = copy.deepcopy(tarea)
        nuevo_vecino_2.t_ini = nuevo_vecino_2.t_ini - 1
        if nuevo_vecino_2.t_ini < 0:
            E_vecino_2 = 100
        else:
            E_vecino_2 = len(conflictos_(nuevo_vecino_2, conficto, index_1, index_2))
        E_vecino_1 = len(conflictos_(nuevo_vecino_1, conficto, index_1, index_2))


        if E_vecino_1 < E_vecino_2 and E_vecino_1 < E_actual:
            tarea = nuevo_vecino_1
            E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
        elif E_vecino_2 < E_vecino_1 and E_vecino_2 < E_actual:
            tarea = nuevo_vecino_2
            E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
        elif E_vecino_1 == E_vecino_2 and E_vecino_1 < E_actual:
            tarea = random.choice([nuevo_vecino_1, nuevo_vecino_2])
            E_actual = len(conflictos_(tarea, conficto, index_1, index_2))


        k+=1



    return tarea


def calculo_E(estado_ac):
    E = 0
    conflictos = []
    for index_1,job in enumerate(estado_ac):
        for index_2, tarea in enumerate(job):
            E = E + tarea.t_ini + tarea.duracion
            confictos_tarea = conflictos_(tarea,estado_ac,index_1,index_2)

            conflictos = conflictos + confictos_tarea
    conflictos = set(conflictos)
    f = E * 0.1 + len(conflictos) * 0.9 #pondero mi camino
    return f


def calculo_T(t):
    alpha = 0.99
    return t*alpha


def recocido_simulado(estado_act, t=200000):

    mejor_nodo = copy.deepcopy(estado_act)
    E_mejor_nodo = calculo_E(mejor_nodo)
    E_actual = calculo_E(estado_act)
    while(1):
        T = calculo_T(t)
        if T < 0.001:
            return mejor_nodo



        nuevo_estado = copy.deepcopy(estado_act)
        #Escojo una tarea aleatoriamente
        pos_1 = random.randrange(0, len(estado_act))

        pos_2 = random.randrange(0, len(estado_act[pos_1][:]))


        tarea = copy.deepcopy(estado_act[pos_1][pos_2])



        nuevo_estado[pos_1][pos_2] = copy.deepcopy(minimo_conflicto(tarea, estado_act, pos_1, pos_2))


        E_nuevo = calculo_E(nuevo_estado)

        dE = E_nuevo - E_actual
        if dE < 0:

            estado_act = copy.deepcopy(nuevo_estado)
        elif dE > 0:
            if math.e ** (-dE / T) > random.random():

                estado_act = copy.deepcopy(nuevo_estado)
        if E_mejor_nodo > E_actual:

            mejor_nodo = copy.deepcopy(estado_act)
            E_mejor_nodo = calculo_E(mejor_nodo)

        E_actual = calculo_E(estado_act)

        t = T



def main():
    trabajos = [[Tarea(0, 2), Tarea(2, 3), Tarea(3, 1)],   #Maquina_n, duracion_t
                [Tarea(2, 4), Tarea(1, 1)],
                [Tarea(0, 4), Tarea(2, 1), Tarea(1, 2)]
                ]
    #Estado inicial aleatorio
    for i in trabajos:
        for j in i:
            j.t_ini = random.randint(1, 3)

    for en,job in enumerate(trabajos):
        print("trabajo ",en)
        for tar in job:
            print(tar.maquina, tar.t_ini, tar.duracion, end=' - ')
        print()

    solucion = recocido_simulado(trabajos)
    conflictos = 0
    conf = []
    for index_1,job in enumerate(solucion):
        for index_2, tarea in enumerate(job):
            confictos_tarea = conflictos_(tarea,solucion,index_1,index_2)

            conf = conf + confictos_tarea
            conflictos = conflictos + len(confictos_tarea)

    print("Conflictos")
    print(len(conf))
    print("La solucion es ")
    for index, job in enumerate(solucion):
        print("trabajo ",index)
        for tar in job:
            print(tar.maquina, tar.t_ini, tar.duracion, end=' - ')
        print()





if __name__ == '__main__':
     main()
