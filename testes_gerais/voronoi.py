# -*- coding: utf-8 -*-
__author__ = 'abraao'

from visualizador2 import mostrar_sistema3 as mostrar_sistema
from sys import platform, exit
import pickle
from os.path import isfile, join
import matplotlib.pyplot as plt
import os
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np


nome_simulacao = 'atrp05_atrc05_h1_mono'
nome_simulacao = 'atrp05_atrc05_h10_mono'
nome_simulacao = 'atrp05_atrc05_h5_polid'
nome_simulacao = 'atrp05_atrc05_h10_polid'

if platform == 'linux':
    pasta_raiz = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/' + nome_simulacao
elif platform == 'win32':
    pasta_raiz = 'D://SIMULACOES_DMCONVEYOR/' + nome_simulacao
else:
    print('Plataforma desconhecida: ' + str(platform))
    exit()

# ----------------------------------------------------------------------------------------------------------------------

numero_arquivo = 300

arquivo = pasta_raiz +'/' + nome_simulacao + '_' + str(numero_arquivo)

print('Carregando arquivo')
print(arquivo)

sistema = pickle.load(open(arquivo, 'rb'))
plt.close('all')
print('Carregado')

print('Numero de partículas livres: ' + str(len(sistema.lista_particulas_livres)))

pontoslistadepois = []
i = 0
for pid in sistema.lista_particulas_livres:
    p = sistema.lista_particulas[pid]
    x = p.posicao['x']
    y = p.posicao['y']

    # print(i)

    # np.append(pontos, [x, y], axis=0)
    if x >= -9999 and i < 1000:
        i += 0
        pontoslistadepois.append([x, y])

pontosdepois = np.asarray(pontoslistadepois)
print(i)
print(pontosdepois.ndim)

# print(pontoslista)


vor = Voronoi(pontosdepois)

voronoi_plot_2d(vor)
plt.show()

