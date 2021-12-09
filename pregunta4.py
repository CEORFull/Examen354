# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 16:46:28 2021

@author: ceory
"""

import numpy as np

        

X = np.array([[1,1,1],
              [1,-1,1],
              [-1,1,1],
              [-1,-1,1]])

y = np.array([[1],[-1],[-1],[-1]])

w = 2 * np.random.random((1,3)) - 1
print(w)

factor_aprendizaje = 0.4

entrenado = False

while entrenado == False:
    i = 0
    #empieza la sumatoria
    for a in X:
        sum = a[0]*w[0][0] + a[1]*w[0][1] + a[2]*w[0][2]
        print(sum)
        #función de activación
        if sum < 0:
            res = -1
        else:
            res = 1
            
        error = y[i] - res
        print(error)
        
        if error == 0:
            i = i+1
            if(i == 3):
                entrenado = True
                break
        else:
            #cambia los pesos
            for u in range(3):
                w[0][u] = w[0][u] + (factor_aprendizaje * error * a[u])
            
            print(w)
            break
        
print("Entrenamiento terminado, los pesos obtenidos son: ")
print(w)
entrada1 = int(input("Ingrese la primera entrada: "))
entrada2 = int(input("Ingrese la segunda entrada: "))

suma = entrada1*w[0][0] + entrada2*w[0][1] + X[0][2]*w[0][2]
if suma < 0:
    print ("El resultado es 0")
else:
    print ("El resultado es 1")

print("fin")
                

            
