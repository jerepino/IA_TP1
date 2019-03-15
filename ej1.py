
class Nodo():
    def __init__(self, posicion,g,h):
        self.posicion = posicion
        self.g=g
        self.h=h
        self.f=g+h


def heuristica(posicion_actual,posicion_fin):
        hh=0
        for i in range(0,len(posicion_actual),1):
                hh=(posicion_fin[i]-posicion_actual[i])**2+hh
        h=hh**0.5

        return h





def main():

    posicion_inicio = (0,0,0,0,0,0)
    posicion_fin = (90,90,90,90,90,90)
    g=0
    h=heuristica(posicion_inicio,posicion_fin)

    nodo_inicio=Nodo(posicion_inicio,g,h)

    lista_abierta=[]
    lista_cerrada=[]

    lista_abierta.append(nodo_inicio)




    nodo_actual=lista_abierta[0]

    #while(len(lista_abierta)>0):

    #for nueva_posicion in [-1,-1,-1,-1,-1,-1]:
    #    nodo_posicion = (nodo_inicio.posicion[0]+nueva_posicion[0],nodo_inicio.posicion[1]+nueva_posicion[1],nodo_inicio.posicion[2]+nueva_posicion[2],nodo_inicio.posicion[3]+nueva_posicion[3],nodo_inicio.posicion[4]+nueva_posicion[4],nodo_inicio.posicion[5]+nueva_posicion[5])

    pos_actual_1 =  [0,0,0,0,0,0]
    pos_actual_2 = [0,0,0,0,0,0]
    pos_ant= posicion_inicio
    for k in range(-1,2,2):
     for i in range(0,6,1):
      for j in range(0,6,1):
       if i==j:
        pos_actual_1 [i]=pos_ant[i]+k
       else:
        pos_actual_1 [j]=pos_ant[j]
      print(pos_actual_1)







if __name__ == '__main__':
        main()
