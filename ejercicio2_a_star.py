import math
import matplotlib as plt


class Nodo():


    def __init__(self,x,y,g):
        self.x = x
        self.y = y

        self.g=g


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def heuristica(self, xFin,yFin):
        x_h=0
        y_h=0

        #Distancia euclediana
        x_h= xFin - self.x
        y_h= yFin - self.y
        h = math.sqrt(x_h*x_h + y_h*y_h)

        #Distancia de Manhatan
        #x_h = h + abs(xFin - self.x)
        #y_h = h + abs(yFin - self.y)
        #h= x_h + y_h


        return(h)

    def funcion_evaluacion(self,xFin,yFin):
        self.f = self.g + self.heuristica(xFin,yFin)

def a_estrella (inicio,meta,mapa,M,N):

    lista_abierta=[]

    primer_nodo=Nodo(inicio[1],inicio[0],0)

    lista_abierta.append(primer_nodo)

    primer_nodo.funcion_evaluacion(meta[1],meta[0])

    meta_nodo=Nodo(meta[1],meta[0],0)

    lista_cerrada=[]


    while (len(lista_abierta)>0):

        ident_actual=0
        nodo_actual = lista_abierta[0]

        for ident, item in enumerate(lista_abierta):
            if item.f < nodo_actual.f:
                nodo_actual = item
                ident_actual = ident

        lista_abierta.pop(ident_actual)
        lista_cerrada.append(nodo_actual)




        #Muestro valores de lista_cerrada
        #for x in range(len(lista_cerrada)):
        # print lista_cerrada[x]

        print (nodo_actual.x, nodo_actual.y)

        if nodo_actual.x == meta_nodo.x and nodo_actual.y == meta_nodo.y:
            return nodo_actual.x , nodo_actual.y


        #Genero vecinos (8 vecinos)
        vecinos=[]
        valores_f=[]

        for i in [(-1,0),(1,0),(0,1),(0,-1),(-1,1),(-1,-1),(1,1),(1,-1)]:
            coord_vecinos = (nodo_actual.x +i[0] , nodo_actual.y+i[1])


            if (coord_vecinos[0]>=0 and coord_vecinos[0]<M and coord_vecinos[1]>=0 and coord_vecinos[1]<N):
                if (mapa[coord_vecinos[1]][coord_vecinos[0]]!=1):

                    nuevo_nodo=Nodo(coord_vecinos[0],coord_vecinos[1],nodo_actual.g+1)

                    nuevo_nodo.funcion_evaluacion(meta[1],meta[0])

                    vecinos.append(nuevo_nodo)

                    valores_f.append(nuevo_nodo.f)

        #Muestro valores de f
        #for x in range(len(valores_f)):
        #    print valores_f[x]

        #Verifico si estan en la lista cerrada

        for vecino in vecinos:
            for j in lista_cerrada:
                if vecino == j:
                    continue
            #Verifico que no este en la lista abierta

            for nodoAbierto in lista_abierta:
                if vecino == nodoAbierto and vecino.g > nodoAbierto.g:
                    continue

            lista_abierta.append(vecino)





def main():

    mapa = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    M=len(mapa[0])
    N=len(mapa)

    #print M
    #print N

    inicio=[9,12]

    #OJO QUE LAS COORDENADAS ESTAN INVERT
    #EJEMPLO: meta=[2,1]  2->y 1->x


    meta=[0,0]
    camino=a_estrella(inicio,meta,mapa,M,N)
    print ("Encontraste la meta")
    print (camino)




if __name__ == '__main__':
    main()
