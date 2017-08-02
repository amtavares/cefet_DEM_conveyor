# -*- coding: utf-8 -*-
__author__ = 'abraao'
import numpy as np
import pandas as pd
import math
import pickle
from analises.analise_estatica import Estatistica
import os
import matplotlib.pyplot as plt
from multiprocessing import Pool




def processa_sublista(parametros):

    sublista, i, pasta, pasta_temp = parametros

    print('\nSublista ' + str(i))

    variaveis = {
        'vx_media_antes': list(),
        'vx_min_antes': list(),
        'vx_max_antes': list(),
        'vy_media_antes': list(),
        'vy_min_antes': list(),
        'vy_max_antes': list(),
        'v_media_antes': list(),
        'v_min_antes': list(),
        'v_max_antes': list(),

        'vx_media_depois': list(),
        'vx_min_depois': list(),
        'vx_max_depois': list(),
        'vy_media_depois': list(),
        'vy_min_depois': list(),
        'vy_max_depois': list(),
        'v_media_depois': list(),
        'v_min_depois': list(),
        'v_max_depois': list(),

        'vx_media_durante': list(),
        'vx_min_durante': list(),
        'vx_max_durante': list(),
        'vy_media_durante': list(),
        'vy_min_durante': list(),
        'vy_max_durante': list(),
        'v_media_durante': list(),
        'v_min_durante': list(),
        'v_max_durante': list(),

        'iteracao': list(),
        'tempo': list()
    }

    for arquivo in sublista:
        print('Processando arquivo ' + arquivo)
        f = open(pasta + '/' + arquivo, 'rb')
        sistema = pickle.load(f)
        f.close()

        # --------------------
        largura_rois = 0.5
        altura_rois = 1
        ybase_rois = -0.5
        y1 = ybase_rois
        y2 = y1 + altura_rois
        # --------------------

        stat_temp = Estatistica(sistema)

        stat_temp.set_roi(-largura_rois / 2, y1, largura_rois / 2, y2, 'box_durante')
        stat_temp.set_roi(-(largura_rois / 2 + largura_rois), y1, -largura_rois / 2, y2, 'box_antes')
        stat_temp.set_roi(largura_rois / 2, y1, largura_rois / 2 + largura_rois, y2, 'box_depois')

        dados_antes = pd.DataFrame(stat_temp.estatistica_particulas('box_antes'))
        dados_durante = pd.DataFrame(stat_temp.estatistica_particulas('box_durante'))
        dados_depois = pd.DataFrame(stat_temp.estatistica_particulas('box_depois'))

        # print('Média: ')
        # print(dados_antes['velocidade_x'].mean())
        # print('------')

        variaveis['vx_media_antes'].append(dados_antes['velocidade_x'].mean())
        variaveis['vx_min_antes'].append(dados_antes['velocidade_x'].min())
        variaveis['vx_max_antes'].append(dados_antes['velocidade_x'].max())
        variaveis['vy_media_antes'].append(dados_antes['velocidade_y'].mean())
        variaveis['vy_min_antes'].append(dados_antes['velocidade_y'].min())
        variaveis['vy_max_antes'].append(dados_antes['velocidade_y'].max())
        variaveis['v_media_antes'].append(dados_antes['velocidade_modulo'].mean())
        variaveis['v_min_antes'].append(dados_antes['velocidade_modulo'].min())
        variaveis['v_max_antes'].append(dados_antes['velocidade_modulo'].max())

        variaveis['vx_media_depois'].append(dados_depois['velocidade_x'].mean())
        variaveis['vx_min_depois'].append(dados_depois['velocidade_x'].min())
        variaveis['vx_max_depois'].append(dados_depois['velocidade_x'].max())
        variaveis['vy_media_depois'].append(dados_depois['velocidade_y'].mean())
        variaveis['vy_min_depois'].append(dados_depois['velocidade_y'].min())
        variaveis['vy_max_depois'].append(dados_depois['velocidade_y'].max())
        variaveis['v_media_depois'].append(dados_depois['velocidade_modulo'].mean())
        variaveis['v_min_depois'].append(dados_depois['velocidade_modulo'].min())
        variaveis['v_max_depois'].append(dados_depois['velocidade_modulo'].max())

        variaveis['vx_media_durante'].append(dados_durante['velocidade_x'].mean())
        variaveis['vx_min_durante'].append(dados_durante['velocidade_x'].min())
        variaveis['vx_max_durante'].append(dados_durante['velocidade_x'].max())
        variaveis['vy_media_durante'].append(dados_durante['velocidade_y'].mean())
        variaveis['vy_min_durante'].append(dados_durante['velocidade_y'].min())
        variaveis['vy_max_durante'].append(dados_durante['velocidade_y'].max())
        variaveis['v_media_durante'].append(dados_durante['velocidade_modulo'].mean())
        variaveis['v_min_durante'].append(dados_durante['velocidade_modulo'].min())
        variaveis['v_max_durante'].append(dados_durante['velocidade_modulo'].max())

        variaveis['iteracao'].append(sistema.iteracao)
        variaveis['tempo'].append(sistema.tempo_simulado)

        stat_temp = None
        sistema = None
        dados_antes = None
        dados_durante = None
        dados_depois = None

        plt.close('all')

        for i in plt.get_fignums():
            # plt.figure(i)
            # plt.savefig('figure%d.png' % i)
            print('Figura: ' + str(i))



        # del stat_temp
        # del sistema
        # del dados_antes
        # del dados_durante
        # del dados_depois
        # ---------------------------------------------------------

    # Salva o resultado parcial
    if not os.path.exists(pasta_temp):
        os.makedirs(pasta_temp)

    dados_temp = pd.DataFrame()
    for var, var_valores in variaveis.items():
        dados_temp[var] = pd.Series(var_valores)

    nome_temp = 'dadostemp' + str(i)
    dados_temp.set_index('tempo', drop=True, inplace=True)

    with open(pasta_temp + nome_temp, 'wb') as f:
        pickle.dump(dados_temp, f)

    del variaveis
    del dados_temp


class EstatisticaTemporal:
    def __init__(self, pasta):
        self.pasta = pasta
        self.pasta_temp = None
        # self.sistema = None
        self.rois = {}  # Key: nome da roi, Value: dictionary com as propriedades calculadas

    def run(self):
        from os import listdir
        from os.path import isfile, join
        mypath = self.pasta

        self.pasta_temp = self.pasta + '/temp/'
        lista_arquivos = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        # lista_arquivos.sort()

        dados = pd.DataFrame()

        # --------------------
        # largura_rois = 0.5
        # altura_rois = 1
        # ybase_rois = -0.5
        # y1 = ybase_rois
        # y2 = y1 + altura_rois
        # --------------------

        n = 10
        c = int(len(lista_arquivos) / n)
        todos_parametros = []
        i = 0
        for s in range(0, len(lista_arquivos), c):
            sublista = lista_arquivos[s:s + c]
            todos_parametros.append((sublista, i, self.pasta, self.pasta_temp))
            i += 1

        # for param in todos_parametros:
        #     processa_sublista(param)

        # if 1:
        pool = Pool(5)
        pool.map(processa_sublista, todos_parametros)
        pool.close()
        pool.join()

        #
        # for sublista in sublistas:
        #     print('\nSublista ' + str(i))
        #
        #     if not os.path.exists(self.pasta_temp + 'dadostemp' + str(i)):
        #         processa_sublista(sublista, i, self.pasta, self.pasta_temp)
        #     else:
        #         print('Arquivo dadostemp' + str(i) + ' já existe')
        #
        #     i += 1

        print('Finalizando processamento de arquivos...')
        dados = pd.DataFrame()
        # Reagrupando os dados
        for i in range(0, n):
            nome_temp = 'dadostemp' + str(i)

            # dados_temp = None
            f = open(self.pasta_temp + nome_temp, 'rb')
            dados_temp = pickle.load(f)
            f.close()

            dados = dados.append(dados_temp)

        return dados

    def set_roi(self, x1, y1, x2, y2, nome):
        # nova_roi = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'lista_particulas': self.update_roi(nome)}
        nova_roi = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        self.rois[nome] = nova_roi
