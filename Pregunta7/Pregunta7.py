# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 07:50:53 2021

@author: ceory
"""

import pandas as pd
import  numpy as np


df = pd.read_csv('breast-cancer.csv')

#Preprocesamos los datos
df.replace(np.nan,"0")
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

df["class_1"] = encoder.fit_transform(df.clas.values)
df["age_1"] = encoder.fit_transform(df.age.values)
df["menopause_1"] = encoder.fit_transform(df.menopause.values)
df["tumorSize_1"] = encoder.fit_transform(df.tumorSize.values)
df["invNodes_1"] = encoder.fit_transform(df.invNodes.values)
df["nodeCaps_1"] = encoder.fit_transform(df.nodeCaps.values)
df["breast_1"] = encoder.fit_transform(df.breast.values)
df["breastQuad_1"] = encoder.fit_transform(df.breastQuad.values)
df["irradiat_1"] = encoder.fit_transform(df.irradiat.values)

#Empezamos a definir las entradas
X = np.array(list(zip(df["age_1"].values,df["menopause_1"].values,df["tumorSize_1"].values,df["invNodes_1"].values,df["nodeCaps_1"].values,df["degMalig"].values,df["breast_1"].values,df["breastQuad_1"].values,df["irradiat_1"].values)))

#Agrupamos
from sklearn.cluster import KMeans
kMeans = KMeans(n_clusters = 2)
kMeans = kMeans.fit(X)
labels=kMeans.predict(X)
centroids=kMeans.cluster_centers_

#graficamos
import matplotlib.pyplot as plt

colors=["m.","r."]

for i in range(len(X)):
    print(f"Coordenada: {X[i]} Label: {labels[i]}")
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)
    
plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=150, linewidths=5, zorder=10)
plt.show()

#evaluamos el modelo
from sklearn import metrics
labels_true = df["class_1"].values
print(" ")
print("El modelo presenta una eficacia del: ",metrics.rand_score(labels_true, labels))

#Comprobamos que tan bien funciona el modelo
from sklearn.metrics import classification_report
print(" ")
print(classification_report(labels_true,labels))


#iniciamos con la matriz de confunsion
from sklearn.metrics import confusion_matrix
confm = confusion_matrix(labels_true,labels)
print(confm)

#graficamos la matriz de confusión

from string import ascii_uppercase
import seaborn as sns

columnas = ['Clase %s'%(i) for i in list(ascii_uppercase)[0:len(np.unique(labels))]]
df_conf = pd.DataFrame(confm,index=columnas, columns=columnas)

grafica = sns.heatmap(df_conf, cmap='Pastel1',annot=True)


grafica.set(xlabel = 'Verdaderos', ylabel='Predicciones')