import random

vector = [0,1, 2 , 3, 4, 5,6,7,8,9]
ve = [10,11,12,13,14,15,16,17,18,19]
print(vector[1:5])
print(vector[1:])
print(vector[:5])
del vector[1:5]
print(vector)
vector = vector + [10,11]
print(vector)
aux = ve[2:4]
print(aux)


if 1 and 1:
    print("ok")
if 1 and not 2:
    print("not ")

p = 5
n = [ p in range(0,10)]
print(random.randint(0, 2))