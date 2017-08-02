# -*- coding: utf-8 -*-
__author__ = 'abraao'

import numpy as np
import math


def calcula_contato_linha(seg_a, seg_b, circ_pos, circ_rad):

    def closest_point_on_seg(seg_a, seg_b, circ_pos):
        seg_v = seg_b - seg_a
        pt_v = circ_pos - seg_a
        seg_v_comp = np.linalg.norm(seg_v)
        if seg_v_comp <= 0:
            raise ValueError("Invalid segment length")
        seg_v_unit = seg_v / seg_v_comp
        proj = pt_v.dot(seg_v_unit)
        if proj <= 0:
            # print('Ob 3')
            return seg_a.copy()
        if proj >= seg_v_comp:
            # print('Ob 4')
            return seg_b.copy()
        proj_v = seg_v_unit * proj
        closest = proj_v + seg_a

        return closest

    closest = closest_point_on_seg(seg_a, seg_b, circ_pos)
    dist_v = circ_pos - closest
    dist_v_comp = np.linalg.norm(dist_v)

    if dist_v_comp > circ_rad:
        # print('Ob 1')
        # return np.array([0, 0])
        return (False, dist_v_comp)
    if dist_v_comp <= 0:
        # print('Ob 2')
        raise ValueError("Circle's center is exactly on segment")

    # offset = dist_v / dist_v_comp * (circ_rad - dist_v_comp)
    # print('Offset')
    # print(dist_v)
    # return offset

    # -dist_ é a distancia x e y do centro do circulo ao ponto de contato
    # dist_v_comp é o modulo desta distancia
    return -dist_v, dist_v_comp,




if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import random

    lim = 10

    xc = 1
    yc = 1
    # xc = random.randrange(-lim, lim)
    # yc = random.randrange(-lim, lim)
    raio = 5


    x1 = random.randrange(-lim, lim)
    y1 = random.randrange(-lim, lim)
    x2 = random.randrange(-lim, lim)
    y2 = random.randrange(-lim, lim)

    # x1 = -6
    # y1 = 4
    # x2 = -9
    # y2 = 7
    #
    x1 = 4
    y1 = -6
    x2 = 4
    y2 = 6

    sega = np.array([x1,y1])
    segb = np.array([x2,y2])
    circ = np.array([xc,yc])

    ponto, distancia = calcula_contato_linha(sega, segb, circ, raio)
    print(ponto)
    print(distancia)

    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    circle = plt.Circle((xc, yc), radius=raio, fc='y', alpha=0.1)

    plt.plot([x1, x2], [y1, y2], '-s', markeredgewidth=5)
    # plt.plot([xc, cx], [circulo_y, cy], 'r')
    plt.plot([xc,xc+ponto[0]],[yc,yc+ponto[1]],'r-')
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