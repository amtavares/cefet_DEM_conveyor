# -*- coding: utf-8 -*-
__author__ = 'abraao'

import pickle
from analises.analise_estatica import Estatistica
from analises.analise_temporal import EstatisticaTemporal
import pandas as pd
import os
import matplotlib.pylab as plt

pd.set_option('expand_frame_repr', False)
plt.style.use('ggplot')

# file_path = '../save/para_benchmark2/para_benchmark2_280'
# file_path = '../save/sem_atrito/sem_atrito_280'
file_path = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_polid/atrp05_atrc05_h10_polid_324'

f = open(file_path, 'rb')
sistema = pickle.load(f)

stat = Estatistica(sistema)

print('Criando as ROIs')

largura_rois = 0.5
altura_rois = 1
ybase_rois = -0.5


y1 = ybase_rois
y2 = y1 + altura_rois


stat.set_roi(-largura_rois/2, y1, largura_rois/2, y2, 'box_durante')
stat.set_roi(-(largura_rois/2+largura_rois),y1, -largura_rois/2, y2, 'box_antes')
stat.set_roi(largura_rois/2, y1, largura_rois/2+largura_rois, y2, 'box_depois')


# stat.set_roi(-1, -0.5, -0.5, 0.5, 'box_antes')
# stat.set_roi(-0.5, -0.5, 0, 0.5, 'box_durante')
# stat.set_roi(0, -0.5, 0.5, 0.5, 'box_depois')

print('Pegando as estatisticas')

dados_antes = pd.DataFrame(stat.estatistica_particulas('box_antes'))
dados_durante = pd.DataFrame(stat.estatistica_particulas('box_durante'))
dados_depois = pd.DataFrame(stat.estatistica_particulas('box_depois'))

print(dados_antes.columns.values.tolist())

# print('Antes: ')
# print('Vx média:  {}'.format(dados_antes['velocidade_x'].mean))
# print('Vx máximo: {}'.format(dados_antes['velocidade_x'].max))
# print('Vx mínimo: {}'.format(dados_antes['velocidade_x'].min))

print('\nAntes: ')
print(dados_antes.describe())
print('\nDepois: ')
print(dados_depois.describe())

tempo = sistema.tempo_simulado
iteracao = sistema.iteracao

fig = plt.figure()
fig.suptitle('$\mu_{particula|particula} = 0.5$  $\mu_{particula|correia} = 0.50$', fontsize=18)

ax1 = fig.add_subplot(311)
dados_antes['velocidade_x'].plot(kind='hist', bins=20, facecolor='blue')
ax1.set_title('Distribuição de Vx antes do fim da correia, em t= {:.2f}s'.format(tempo))
ax1.set_xlabel('Vx [m/s')

ax2 = fig.add_subplot(312)
dados_durante['velocidade_x'].plot(kind='hist', bins=20, facecolor='blue')
ax2.set_title('Distribuição de Vx na região do fim da correia, em t= {:.2f}s'.format(tempo))
ax2.set_xlabel('Vx [m/s')

ax3 = fig.add_subplot(313)
dados_depois['velocidade_x'].plot(kind='hist', bins=20, facecolor='blue')
ax3.set_title('Distribuição de Vx depois do fim da correia, em t= {:.2f}s'.format(tempo))
ax3.set_xlabel('Vx [m/s')
plt.show()


interp_media = stat.estatistica_contatos()
print('Interpenetração média:  {}'.format(interp_media))
print('       Fração do raio:  {}'.format(interp_media/0.025))