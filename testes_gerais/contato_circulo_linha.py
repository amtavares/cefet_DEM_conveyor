# -*- coding: utf-8 -*-
__author__ = 'abraao'

import matplotlib.pyplot as plt
import numpy as np
import math
import random

# ----------------------------------------------------------------------------------------------------------------------
def intersecao_linhas(x1,y1,x2,y2,x3,y3,x4,y4):
    pass


# ----------------------------------------------------------------------------------------------------------------------
raiz = math.sqrt
abs = math.fabs

circulo_x = 0
circulo_y = 0
circulo_raio = 5

lim = 10

p1x = random.randrange(-lim,lim)
p1y = random.randrange(-lim,lim)

p2x = random.randrange(-lim,lim)
p2y = random.randrange(-lim,lim)

dx = p2x - p1x
dy = p2y - p1y
comprimento_linha = raiz(dx**2 + dy**2)


retorno = True
# ----------------------------------------------------------------------------------------------------------------------





# Teste 1: Distância do centro do círculo à linha infinita

distancia_linha = abs( (dx)*circulo_x + (-dy)*circulo_y + (-dx)*p1y + (dy)*p1x )/raiz(dx**2+dy**2)

# Outro método de calculo -------------------------
# A1 = p2y - p1y
# B1 = p1x - p2x
# C1 = A1*p1x + B1*p1y
# C2 = -B1*circulo_x + A1*circulo_y
# det = A1*A1 + B1*B1
# cx = 0
# cy = 0
#
# if det != 0:
#     cx = (A1*C1 - B1*C2)/det
#     cy = (A1*C2 + B1*C1)/det
# else:
#     cx = circulo_x
#     cy = circulo_y
#
# distancia2 = raiz( (cx - circulo_x)**2 + (cy - circulo_y)**2 )
#
# print(distancia1)
# print(distancia2)

if distancia_linha < circulo_raio:

    p1dentro = False
    p2dentro = False

    distancia_p1 = raiz((p1x - circulo_x)**2 + (p1y - circulo_y)**2)
    distancia_p2 = raiz((p2x - circulo_x)**2 + (p2y - circulo_y)**2)

    if distancia_p1 < circulo_raio:
        p1dentro = True
    if distancia_p2 < circulo_raio:
        p2dentro = True

    # if (p1dentro and p2dentro) or

else:
    # return False
    pass







# ----------------------------------------------------------------------------------------------------------------------

fig = plt.figure()
axis = fig.add_subplot(1,1,1)

circle = plt.Circle((circulo_x,circulo_y), radius=circulo_raio, fc='y', alpha=0.1)

plt.plot([p1x, p2x], [p1y, p2y], '-s', markeredgewidth=5)
plt.plot([circulo_x, cx], [circulo_y, cy], 'r')


axis.add_patch(circle)
axis.axis('square')
axis.axis()
plt.grid()
plt.show()
