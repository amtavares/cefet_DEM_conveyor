# -*- coding: utf-8 -*-
__author__ = 'abraao'
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import PatchCollection
import math
import numpy as np
from contato import Contato, Contato_objeto

raio = 3
xs = [4, 8, 15, 16, 23, 42]
ys = [4, 8, 15, 16, 23, 42]
velocidades = [0.1, 2.23, 3.78, 4.15, 5.0, 6.7]
lista_objetos = []

fig = plt.figure()
ax = fig.add_subplot(111)

for coordenada in zip(xs, ys):
    x, y = coordenada
    circulo = plt.Circle(coordenada, radius=raio, edgecolor='none', linestyle='dashed', lw=250)
    lista_objetos.append(circulo)

minimo = 0
maximo = 20
velocidades = [minimo if v <=minimo else maximo if v >= maximo else v for v in velocidades]
print(velocidades)

col = PatchCollection(lista_objetos)
col.set(array=np.array(velocidades), cmap='jet', edgecolor='none')
ax.add_collection(col)

ticks = np.linspace(min(velocidades), max(velocidades), num=10)

# cb = fig.colorbar(col, ticks=ticks)



print(fig.axes[0])
# print(fig.axes[1])

ax.axis('scaled')
plt.grid()
plt.show()
