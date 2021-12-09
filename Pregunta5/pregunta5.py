# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 08:37:51 2021

@author: ceory
This breast cancer domain was obtained from the University Medical Centre, 
Institute of Oncology, Ljubljana, Yugoslavia. Thanks go to M. Zwitter and M. 
Soklic for providing the data.
"""
import pandas as pd
import numpy as np

#Abrimos el archivo
df = pd.read_csv("breast-cancer.csv")
df.replace(np.nan,"0")

#Preprocesamos los datos
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

df["age_1"] = encoder.fit_transform(df.age.values)
df["menopause_1"] = encoder.fit_transform(df.menopause.values)
df["tumorSize_1"] = encoder.fit_transform(df.tumorSize.values)
df["invNodes_1"] = encoder.fit_transform(df.invNodes.values)
df["nodeCaps_1"] = encoder.fit_transform(df.nodeCaps.values)
df["breast_1"] = encoder.fit_transform(df.breast.values)
df["breastQuad_1"] = encoder.fit_transform(df.breastQuad.values)
df["irradiat_1"] = encoder.fit_transform(df.irradiat.values)

#Empezamos a definir las entradas
X = df[["age_1","menopause_1","tumorSize_1","invNodes_1","nodeCaps_1","degMalig","breast_1","breastQuad_1","irradiat_1"]]
y = df['class']


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.8, test_size=0.2)

#parte 2 del preprocesamiento
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)  

#creación de la red neuronal
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=1000, alpha=0.0001,solver='adam', random_state=21,tol=0.000000001)
mlp.fit(X_train,y_train)
predictions = mlp.predict(X_test)

#Comprobamos que tan bien funciona el modelo
from sklearn.metrics import classification_report
print(classification_report(y_test,predictions))


#iniciamos con la matriz de confunsion
from sklearn.metrics import confusion_matrix

confm = confusion_matrix(y_test,predictions)
print(confm)

#graficamos la matriz de confusión

from string import ascii_uppercase
import seaborn as sns

columnas = ['Clase %s'%(i) for i in list(ascii_uppercase)[0:len(np.unique(predictions))]]
df_conf = pd.DataFrame(confm,index=columnas, columns=columnas)

grafica = sns.heatmap(df_conf, cmap='Pastel1',annot=True)


grafica.set(xlabel = 'Verdaderos', ylabel='Predicciones')
