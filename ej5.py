import random
import copy
import math
class Tarea():
    def __init__(self,maquina, duracion=1, t_ini=0):
        self.maquina = maquina
        self.duracion = duracion
        self.t_ini = t_ini


def conflictos_(tarea, conficto, index_1, index_2):
    if tarea.t_ini < 0:
        return [n for n in range(15)]
    conflictos_maquina = [tar for numero_job, job in enumerate(conficto)
                          for numero_tarea, tar in enumerate(job)
                          if(tar.maquina == tarea.maquina and (tar.t_ini + tar.duracion in
                                                               range(tarea.t_ini, tarea.t_ini + tarea.duracion+1)or
                                                               tar.t_ini == tarea.t_ini))]
    conflictos_tiempo = [tar for numero_tarea, tar in enumerate(conficto[index_1])
                         if (numero_tarea > index_2 and tar.t_ini <= tarea.t_ini + tarea.duracion) or
                         (numero_tarea < index_2 and tar.t_ini + tar.duracion >= tarea.t_ini)
                         ]
    conflictos_tarea = conflictos_maquina + conflictos_tiempo
    # confictos_tarea = [tar for numero_job, job in enumerate(conficto)
    #                    for numero_tarea, tar in enumerate(job)
    #                    if (numero_tarea > index_2 and tar.t_ini <= tarea.t_ini + tarea.duracion) or
    #                    (numero_tarea < index_2 and tar.t_ini + tar.duracion >= tarea.t_ini) or
    #                    (tar.maquina == tarea.maquina and (tar.t_ini + tar.duracion in
    #                                                       range(tarea.t_ini, tarea.t_ini + tarea.duracion))) or
    #                    (tar.maquina != tarea.maquina and tar.duracion != tarea.duracion and tar.t_ini != tarea.t_ini)]
    conflictos_tarea = set(conflictos_tarea)
    print("Conflictos")
    print("index del conflicto")
    print(index_1,index_2)
    for h in conflictos_tarea:
        print(h.maquina, h.t_ini,h.duracion)
    print("conflicto maquinas")
    for h in conflictos_maquina:
        print(h.maquina, h.t_ini,h.duracion)
    print("Conflictos con el tiempo ")
    for h in conflictos_tiempo:
        print(h.maquina,h.t_ini,h.duracion)
    # print(len(confictos_tarea))

    return list(conflictos_tarea)


def minimo_conflicto(tarea, conficto, index_1, index_2):

    #calculo energia inicial
    E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
    k=0


    while k < 20:
        if len(conflictos_(tarea, conficto, index_1, index_2)) == 0:
            print("No hay conflictos con la asignacion")
            return tarea
        #genero vecionos
        nuevo_vecino_1 = copy.deepcopy(tarea)
        nuevo_vecino_1.t_ini = nuevo_vecino_1.t_ini + 1
        nuevo_vecino_2 = copy.deepcopy(tarea)
        nuevo_vecino_2.t_ini = nuevo_vecino_2.t_ini - 1
        E_vecino_1 = len(conflictos_(nuevo_vecino_1, conficto, index_1, index_2))
        E_vecino_2 = len(conflictos_(nuevo_vecino_2, conficto, index_1, index_2))
        # if E_vecino_1 < E_actual:
        #     tarea = nuevo_vecino_1
        if E_vecino_1 < E_vecino_2 and E_vecino_1 < E_actual:
            tarea = nuevo_vecino_1
            E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
        elif E_vecino_2 < E_vecino_1 and E_vecino_2 < E_actual:
            tarea = nuevo_vecino_2
            E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
        elif E_vecino_1 == E_vecino_2 and E_vecino_1 < E_actual:
            tarea = random.choice([nuevo_vecino_1, nuevo_vecino_2])
            E_actual = len(conflictos_(tarea, conficto, index_1, index_2))
        # calculo Energia actual

        k+=1

    # confictos_tarea__ = conflictos_(tarea, conficto, index_1, index_2)
    # print("Conflictos")
    # for h in confictos_tarea__:
    #     print(h.maquina, h.duracion, h.t_ini)

    return tarea


def calculo_E(estado_ac):
    E = 0
    conflictos = []
    for index_1,job in enumerate(estado_ac):
        for index_2, tarea in enumerate(job):
            E = E + tarea.t_ini + tarea.duracion
            confictos_tarea = conflictos_(tarea,estado_ac,index_1,index_2)
            # confictos_tarea = [tar for numero_job, job in enumerate(estado_ac)
            #            for numero_tarea, tar in enumerate(job)
            #            if (numero_tarea > index_2 and tar.t_ini <= tarea.t_ini + tarea.duracion) or
            #            (numero_tarea < index_2 and tar.t_ini + tar.duracion >= tarea.t_ini) or
            #            (numero_tarea != index_2 and tar.maquina == tarea.maquina and
            #             (tar.t_ini + tar.duracion in range(tarea.t_ini, tarea.t_ini + tarea.duracion)))]
            conflictos = conflictos + confictos_tarea
    conflictos = set(conflictos)
    f = E * 0 + len(conflictos) * 1 #pondero mi camino
    return f


def calculo_T(t):
    alpha = 0.99
    return t*alpha


def recocido_simulado(estado_act, t=200000000):
    print("El estado actual es ")
    for index, job in enumerate(estado_act):
        print("trabajo ", index)
        for tar in job:
            print(tar.maquina, tar.t_ini, tar.duracion, end=' - ')
        print()
    mejor_nodo = copy.deepcopy(estado_act)
    E_mejor_nodo = calculo_E(mejor_nodo)
    E_actual = calculo_E(estado_act)
    while(1):
        T = calculo_T(t)
        if T <= 0.01:
            return mejor_nodo

        #verifico si es solucion
        conflictos = 0
        for index_1,job in enumerate(estado_act):
            for index_2, tarea in enumerate(job):
                confictos_tarea = conflictos_(tarea,estado_act,index_1,index_2)
                conflictos = conflictos + len(confictos_tarea)

        if conflictos == 0:
            return estado_act

        nuevo_estado = copy.deepcopy(estado_act)
        #Escojo una tarea aleatoriamente
        pos_1 = random.randrange(0, len(estado_act))
        print(pos_1)
        pos_2 = random.randrange(0, len(estado_act[pos_1][:]))
        print(len(estado_act[pos_1][:]),pos_2)
        print("El estado actual es ")
        for index, job in enumerate(estado_act):
            print("trabajo ", index)
            for tar in job:
                print(tar.maquina, tar.t_ini, tar.duracion, end=' - ')
            print()
        tarea = copy.deepcopy(estado_act[pos_1][pos_2])
        print("tarea")
        print(tarea.maquina, tarea.duracion, tarea.t_ini)
        nuevo_estado[pos_1][pos_2] = copy.deepcopy(minimo_conflicto(tarea, estado_act, pos_1, pos_2))
        print("estado actual")
        print(estado_act[pos_1][pos_2].maquina, estado_act[pos_1][pos_2].duracion,estado_act[pos_1][pos_2].t_ini)
        print("nuevo_estado")
        print(nuevo_estado[pos_1][pos_2].maquina, nuevo_estado[pos_1][pos_2].duracion,
              nuevo_estado[pos_1][pos_2].t_ini)

        E_nuevo = calculo_E(nuevo_estado)
        # print(E_actual, E_nuevo)
        dE = E_nuevo - E_actual
        if dE < 0:
            # print("cambio de < 0")
            estado_act = copy.deepcopy(nuevo_estado)
        elif dE > 0:
            if math.e ** (-dE / T) > random.random():
                # print("suerte")
                estado_act = copy.deepcopy(nuevo_estado)
        if E_mejor_nodo > E_actual:
            # print("mejor nodo")
            mejor_nodo = copy.deepcopy(estado_act)
            E_mejor_nodo = calculo_E(mejor_nodo)

        E_actual = calculo_E(estado_act)
        # print(t,dE,math.e ** (-dE / T))
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

    for job in trabajos:
        print("trabajo")
        for tar in job:
            print(tar.maquina, tar.t_ini, tar.duracion, end=' - ')
        print()
    conflictos = 0
    conf = []
    for index_1,job in enumerate(trabajos):
        for index_2, tarea in enumerate(job):
            confictos_tarea = conflictos_(tarea,trabajos,index_1,index_2)
            # confictos_tarea = [tar for numero_job, job in enumerate(solucion)
            #                    for numero_tarea, tar in enumerate(job)
            #                    if (numero_tarea > index_2 and tar.t_ini <= tarea.t_ini + tarea.duracion) or
            #                    (numero_tarea < index_2 and tar.t_ini + tar.duracion >= tarea.t_ini) or
            #                    (numero_tarea != index_2 and tar.maquina == tarea.maquina and
            #                     (tar.t_ini + tar.duracion in range(tarea.t_ini, tarea.t_ini + tarea.duracion)))]

            conf = conf + confictos_tarea
            conflictos = conflictos + len(confictos_tarea)

    print("Conflictos")
    conf = set(conf)
    # conf = list(conf)
    for h in conf:
        # for h in job:
        print(h.maquina, h.t_ini, h.duracion)
    # return  0
    solucion = recocido_simulado(trabajos)
    conflictos = 0
    conf = []
    for index_1,job in enumerate(solucion):
        for index_2, tarea in enumerate(job):
            confictos_tarea = conflictos_(tarea,solucion,index_1,index_2)
            # confictos_tarea = [tar for numero_job, job in enumerate(solucion)
            #                    for numero_tarea, tar in enumerate(job)
            #                    if (numero_tarea > index_2 and tar.t_ini <= tarea.t_ini + tarea.duracion) or
            #                    (numero_tarea < index_2 and tar.t_ini + tar.duracion >= tarea.t_ini) or
            #                    (numero_tarea != index_2 and tar.maquina == tarea.maquina and
            #                     (tar.t_ini + tar.duracion in range(tarea.t_ini, tarea.t_ini + tarea.duracion)))]

            conf = conf + confictos_tarea
            conflictos = conflictos + len(confictos_tarea)

    print("Conflictos")
    conf = set(conf)
    # conf = list(conf)
    for h in conf:
        # for h in job:
        print(h.maquina, h.t_ini, h.duracion)
    print("largo")
    print(len(conf))



    print("La solucion es ")
    for index, job in enumerate(solucion):
        print("trabajo ",index)
        for tar in job:
            print(tar.maquina, tar.t_ini, tar.duracion, end=' - ')
        print()





if __name__ == '__main__':
     main()
