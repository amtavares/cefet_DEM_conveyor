# -*- coding: utf-8 -*-
__author__ = 'abraao'

import pickle
from analises.analise_estatica import Estatistica
from analises.analise_temporal import EstatisticaTemporal
from analises.particle_traking2 import ParticleTracker
import pandas as pd
from sys import exit, platform
import matplotlib.pyplot as plt


pd.set_option('expand_frame_repr', False)
# plt.style.use('ggplot')


# file_path = '../save/para_benchmark2/para_benchmark2_280'
# file_path = '../save/sem_atrito/sem_atrito_280'

# pasta = '../save/sem_atrito'
# pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_polid'

nome_simulacao = 'atrp05_atrc05_h1_mono'
nome_simulacao = 'atrp05_atrc05_h5_polid'
nome_simulacao = 'atrp05_atrc05_h10_polid'
nome_simulacao = 'atrp05_atrc05_h10_mono'

if platform == 'linux':
    pasta_raiz = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/' + nome_simulacao
elif platform == 'win32':
    pasta_raiz = 'D://SIMULACOES_DMCONVEYOR/' + nome_simulacao
else:
    print('Plataforma desconhecida: ' + str(platform))
    exit()


pasta_analises = pasta_raiz + '/analises - ' + nome_simulacao

arquivo_dados = pasta_analises + '/dados_tracker'


if 0:
    from os import listdir
    from os.path import isfile, join
    lista_arquivos = [f for f in listdir(pasta_raiz) if isfile(join(pasta_raiz, f))]

    quantidade_arquivos = len(lista_arquivos)
    nome_ultimo_arquivo = pasta_raiz + '/' + nome_simulacao + '_' + str(quantidade_arquivos-1)
    print(nome_ultimo_arquivo)
    # nome_ultimo_arquivo = pasta_raiz + '/' + 'atrp05_atrc05_h1_350'
    # print(nome_ultimo_arquivo)

    print('Lendo arquivo ' + nome_ultimo_arquivo)

    sistema_temp = pickle.load(open(nome_ultimo_arquivo, 'rb'))
    maior_id = max(sistema_temp.lista_particulas_livres)

    print('Partícula com maior id: ' + str(maior_id))

    exit()

tracker = ParticleTracker(pasta_raiz)

# lista_particulas_alvo = [1407, 1440, 1602, 1712] # Gerador do grafico polidisperso

lista_particulas_alvo = [1404, 1440, 1590, 1701]
# lista_particulas_alvo = [500, 1000, 1500, 2000]

linestyles = ['o-', 'v-', '+-', 's-']


if 0:
    import os
    dados_particulas = tracker.run(list(range(1400, 1801)))
    if not os.path.exists(pasta_analises):
            os.makedirs(pasta_analises)
    pickle.dump(dados_particulas, open(arquivo_dados, 'wb'))

dados_particulas = pickle.load(open(arquivo_dados, 'rb'))

for p_id in lista_particulas_alvo:
    dados_particulas[p_id].set_index('tempo', drop=True, inplace=True)
    dados_particulas[p_id].sort_index(inplace=True)



# ----------------------------------------------------------------------------------------------------------------------

# ax = fig.add_subplot(133)
# ax.fill_between(dados.index, dados['vx_min_depois'], dados['vx_max_depois'], facecolor='black', alpha=0.1)
# ax.plot(dados.index, dados['vx_media_depois'],'.-', label='Vx Média')
# ax.plot(dados.index, dados['vx_max_depois'],'.-', label='Vx maxima')
# ax.plot(dados.index, dados['vx_min_depois'],'.-', label='Vx mínima')
# ax.set_xlabel('Tempo simulado [s]')
# ax.set_ylabel('Velocidade [m/s]')
# ax.legend(loc='upper left')
# ax.set_title('Vx após o fim da correia\n' + r'$\mu_(particula|particula) = 0.5$' + r'  $\mu_(particula|correia) = 0.50$')

fig = plt.figure()
ax = fig.add_subplot(211)

if 0:
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Velocity [m/s]')
    for p_id in lista_particulas_alvo:

        df = dados_particulas[p_id]
        df['velocidade_x'].plot()

        print(p_id)

if 1:
    ax.set_xlabel('x-coordinate [m]')
    ax.set_ylabel('y-coordinate [m]')

    for i, p_id in enumerate(lista_particulas_alvo):
        df = dados_particulas[p_id]
        ax.plot(df['posicao_x'], df['posicao_y'], linestyles[i], label='particle ID:'+str(p_id))

ax.legend(loc='upper right')
# ax.set_title('Trajetória das partículas, material polidisperso\n' + r'$\mu_(particula|particula) = 0.5$' + r'  $\mu_(particula|correia) = 0.50$')
ax.set_title('A) Particle trajectories')

# AXIS 2 ------------------------------------------------------------

ax2 = fig.add_subplot(212)

if 0:
    ax2.set_xlabel('x-coordinate [m]')
    ax2.set_ylabel('y-coordinate [m]')
    for p_id in lista_particulas_alvo:
        df = dados_particulas[p_id]
        ax2.plot(df['posicao_x'], df['posicao_y'], '.-', label='ID_particula:'+str(p_id))

if 1:
    ax2.set_xlabel('x-coordinate [m]')
    ax2.set_ylabel('Vx [m/s]')
    for i, p_id in enumerate(lista_particulas_alvo):
        df = dados_particulas[p_id]
        ax2.plot(df['posicao_x'], df['velocidade_x'], linestyles[i], label='particle ID:'+str(p_id))

if 0:
    ax2.set_xlabel('x-coordinate [m]')
    ax2.set_ylabel('Contacts ')
    for p_id in lista_particulas_alvo:
        df = dados_particulas[p_id]
        ax2.plot(df['posicao_x'], df['quantidade_contatos'], '.-', label='ID_particula:'+str(p_id))

ax2.legend(loc='lower right')
ax2.set_title('B)  Vx as function of x-coordinate')


# Desenhar o transportador -----------------------------------------
if 1:
    from os import listdir
    from os.path import isfile, join
    lista_arquivos = [f for f in listdir(pasta_raiz) if isfile(join(pasta_raiz, f))]

    quantidade_arquivos = len(lista_arquivos)
    nome_primeiro_arquivo = pasta_raiz + '/' + nome_simulacao + '_' + str(0)
    print(nome_primeiro_arquivo)
    print('Lendo arquivo ' + nome_primeiro_arquivo)
    sistema_temp = pickle.load(open(nome_primeiro_arquivo, 'rb'))

    for objeto in sistema_temp.lista_objetos.values():
            x1 = objeto.ponto_inicial[0]
            y1 = objeto.ponto_inicial[1]
            x2 = objeto.ponto_final[0]
            y2 = objeto.ponto_final[1]

            ax.plot([x1, x2], [y1, y2], 'k', linewidth=2)

ax.grid()
ax2.grid()
plt.show()

