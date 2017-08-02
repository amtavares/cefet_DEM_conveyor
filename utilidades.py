# -*- coding: utf-8 -*-
__author__ = 'abraao'
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import math
import numpy as np

# class Gerador():
#     def __init__(self, s):
#         self.semente = s
#
#     def rand0(self):
#         #TODO Testar esta função contra a do C++
#         # Números "mágicos" do gerador aleatório
#         A = 843314861
#         B = 453816693
#         C = 1073741824
#
#         aux = 0.5
#         s = self.semente
#
#         s = s * A
#         if s < 0:
#             s = (s + M) + M
#
#         self.semente = s
#
#         chupeta = s * aux
#
#         return chupeta
#
# def distribuicao_gaussiana(self):
#     soma = 0
#     for i in range(1, 1000):
#         aux = (soma - 500)/83.25
#         aux = (aux + 0.4084)/0.8585
#
def distancia_entre_particulas(p1, p2):

    x1 = p1.posicao['x']
    y1 = p1.posicao['y']
    x2 = p2.posicao['x']
    y2 = p2.posicao['y']

    raio1 = p1.raio
    raio2 = p2.raio

    distancia_centros = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
    distancia_contato = distancia_centros - (raio1 + raio2)

    return distancia_centros, distancia_contato



def ids2str(id1, id2):
    return str(id1) + '_' + str(id2) if id1 < id2 else str(id2) + '_' + str(id1)

def str2ids(s):
    # ids = s.split('_')
    ids = [int(string) for string in s.split('_')]
    return ids

# def mostrar_sistema(sistema):
#
#     # print(' Mostrando sistema')
#     particulas = sistema.lista_particulas
#     livres = sistema.lista_particulas_livres
#     fixas = sistema.lista_particulas_fixas
#     contatos = sistema.lista_contatos
#     contatos_existentes = sistema.lista_contatos_existentes
#
#
#     # plt.figure()
#     # plt.axes()
#     # ax = sistema.axis
#     fig = sistema.figure
#     fig.clf()
#     ax = fig.add_subplot(1, 1, 1)
#     fig.suptitle('Iteracao: {}  -  {:.2f} segundos'.format(sistema.iteracao, sistema.tempo_simulado))
#     ax.clear()
#
#     # Partículas livres ------------------------------------------------------------------------------------------------
#     if (1):
#         lista = []
#         velocidades = []
#         for pid in livres:
#             p = particulas[pid]
#             x = p.posicao['x']
#             y = p.posicao['y']
#             raio = p.raio
#             circle = plt.Circle((x, y), radius=raio, fc='y')
#             lista.append(circle)
#             velocidade_modulo = math.sqrt(p.velocidade['x']**2 + p.velocidade['y']**2)
#             velocidades.append(p.velocidade['x'])
#             # ax.add_patch(circle)
#
#
#             # Labels
#             if 0:
#                 plt.text(x,y,p.id)
#
#             # Setas:
#             comprimento = 0.3
#             # Aceleração
#             if 0:
#                 modulo = math.sqrt(p.aceleracao['x']**2 + p.aceleracao['y']**2)
#                 # print('P.id:{} Aceleração: {} - {} - {:f}'.format(p.id, p.aceleracao['x'],p.aceleracao['y'],modulo))
#                 dx = comprimento * p.aceleracao['x'] / modulo
#                 dy = comprimento * p.aceleracao['y'] / modulo
#                 ax.arrow(x,y,dx,dy,color='r', head_width=0.05, head_length=0.1)
#
#             # Forças
#             if 0:
#                 modulo = math.sqrt(p.forca_total['x'] ** 2 + p.forca_total['y'] ** 2)
#                 # print('P.id:{} Forças: {} - {} - {:f}'.format(p.id, p.forca_total['x'], p.forca_total['y'], modulo))
#                 dx =  comprimento * p.forca_total['x'] / modulo
#                 dy =  comprimento * p.forca_total['y'] / modulo
#                 ax.arrow(x, y, dx, dy, color='m', head_width=0.01, head_length=0.01)
#
#             # Velocidades
#             if 1:
#                 modulo = math.sqrt(p.velocidade['x'] ** 2 + p.velocidade['y'] ** 2)
#                 # print('P.id:{} Velocidade: {} - {} - {:f}'.format(p.id, p.forca_total['x'], p.forca_total['y'], modulo))
#                 dx = comprimento * p.velocidade['x']
#                 dy = comprimento * p.velocidade['y']
#                 ax.arrow(x, y, dx, dy, color='c', head_width=0.01*modulo, head_length=0.01*modulo)
#
#
#         col = PatchCollection(lista)
#         col.set(array=np.array(velocidades), cmap='jet')
#         # ax.add_collection(col)
#         cb = fig.colorbar(col)
#         # plt.clim(0,5)
#         # plt.set(cb, vmin=0, vmax=5)
#
#
#
#     # Partículas fixas  ------------------------------------------------------------------------------------------------
#     if 1:
#         for pid in fixas:
#             p = particulas[pid]
#             x = p.posicao['x']
#             y = p.posicao['y']
#             raio = p.raio
#             circle = plt.Circle((x, y), radius=raio, fc='#B8B8B8')
#             ax.add_patch(circle)
#
#             # Labels
#             if 0:
#                 plt.text(x, y, p.id)
#
#     # Contatos ---------------------------------------------------------------------------------------------------------
#     if 1:
#         if len(contatos_existentes):
#             for cid in contatos_existentes:
#                 c = contatos[cid]
#                 x1 = c.particula1.posicao['x']
#                 y1 = c.particula1.posicao['y']
#                 x2 = c.particula2.posicao['x']
#                 y2 = c.particula2.posicao['y']
#                 if c.deslizante:
#                     estilo = 'g--'
#                 else:
#                     estilo = 'g'
#                 ax.plot([x1,x2],[y1,y2],estilo)
#                 pass
#
#
#
#     ax.axis('scaled')
#     fig.canvas.draw()
#     plt.pause(0.0001)
#     # if sistema.iteracao > 10:
#     #     input()
#
#
#
#
#
