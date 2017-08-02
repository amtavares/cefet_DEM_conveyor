# -*- coding: utf-8 -*-
__author__ = 'abraao'

import numpy as np
import math


def segmento_circulo(x1, y1, x2, y2, xc, yc, raio):

    raiz = math.sqrt

    dx = x2-x1
    dy = y2-y1
    distancia_perpendicular = abs(dx * xc + (-dy) * yc + (-dx) * y1 + dy * x1) / raiz(dx ** 2 + dy ** 2)

    if distancia_perpendicular < raio:

        distancia_p1 = raiz((x1 - xc) ** 2 + (y1 - yc) ** 2)
        distancia_p2 = raiz((x2 - xc) ** 2 + (y2 - yc) ** 2)

        p1dentro = distancia_p1 < raio
        p2dentro = distancia_p2 < raio

        # Caso 1: Um ponto dentro e outro fora
        # Caso 2: Dois pontos fora, sem contato
        # Caso 3: Dois pontos fora, com contato
        # Caso 4: Dois pontos dentro

        # Caso 1: Um ponto dentro e outro fora
        if p1dentro != p2dentro:
            print("Caso 1")
            if distancia_p1 < distancia_p2:
                # Calcula a interpenetracao e o vetor do contato
                distancia_contato = distancia_p1 - raio
                return distancia_contato
            else:
                distancia_contato = distancia_p2 - raio
                return distancia_contato

        # Casos 2 e 3
        if not (p1dentro and p2dentro):
            # Detectar se existe o contato
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            c = np.array([xc, yc])
            segmento_vetor = p2 - p1
            segmento_comprimento = np.linalg.norm(segmento_vetor)

            if distancia_p1 < distancia_p2:
                vetor_p_c = c - p1
            else:
                vetor_p_c = c - p2

            proj = np.dot(vetor_p_c, segmento_vetor)

            if abs(proj) > segmento_comprimento:
                print("Caso 2")
                # Caso 2: Dois pontos fora, sem contato
                return False
            else:
                print("Caso 3")
                # Caso 3: Dois pontos fora, com contato
                distancia_contato = distancia_perpendicular - raio
                return distancia_contato
            pass

        # Caso 4: Dois pontos dentro
        if p1dentro and p2dentro:
            print("Caso 4")
            # Não será implementado pois dado as dimensões típicas do sistema simulado, ele não ocorrerá
            pass

    else:
        # Não há contato
        return False

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import random

    xc = 0
    yc = 0
    raio = 5

    lim = 10

    x1 = random.randrange(-lim, lim)
    y1 = random.randrange(-lim, lim)
    x2 = random.randrange(-lim, lim)
    y2 = random.randrange(-lim, lim)

    x1 = -6
    y1 = 4
    x2 = -9
    y2 = 7

    x1 = -6
    y1 = 4
    x2 = 4
    y2 = 4

    print(segmento_circulo(x1, y1, x2, y2, xc, yc, raio))

    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    circle = plt.Circle((xc, yc), radius=raio, fc='y', alpha=0.1)

    plt.plot([x1, x2], [y1, y2], '-s', markeredgewidth=5)
    # plt.plot([xc, cx], [circulo_y, cy], 'r')

    axis.add_patch(circle)
    axis.axis('square')
    axis.axis()
    plt.grid()
    plt.show()







'''
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

    if (p1dentro and p2dentro) or

else:
    # return False
    pass







# ----------------------------------------------------------------------------------------------------------------------

'''