# -*- coding: utf-8 -*-
__author__ = 'Abraão'

import numpy as np
import pandas as pd
import math
import pickle
import os
import matplotlib.pyplot as plt
from multiprocessing import Pool


class Propriedades:
    valores = None

    def __init__(self):
        self.valores = {
                'velocidade_x': list(),
                'velocidade_y': list(),
                'velocidade_angular': list(),
                'velocidade_modulo': list(),
                'massa': list(),
                'posicao_x': list(),
                'posicao_y': list(),
                'aceleracao_x': list(),
                'aceleracao_y': list(),
                'forca_x': list(),
                'forca_y': list(),
                'forca_modulo': list(),
                'torque': list(),
                'quantidade_contatos': list(),
                'tempo': list()
        }


def processa_arquivos(lista_arquivos, pasta, pasta_temp, lista_particulas_alvo):

    dados_particulas = dict()
    for p_id in lista_particulas_alvo:
        dados_particulas[p_id] = Propriedades()

    for arquivo in lista_arquivos:
        print("\nProcessando arquivo " + arquivo)
        f = open(pasta + '/' + arquivo, 'rb')
        sistema = pickle.load(f)
        f.close()

        lolzinho = list()

        # print(sistema.lista_particulas_livres)

        # Pega os dados cada uma partícula em um tempo
        for p_id in lista_particulas_alvo:
            prop = dados_particulas[p_id]

            if p_id in sistema.lista_particulas_livres:
                # lolzinho.append('X')
                # print('assoooooooooooooooooooooooooooooo')
                p = sistema.lista_particulas[p_id]

                prop.valores['velocidade_x'].append(p.velocidade['x'])
                prop.valores['velocidade_y'].append(p.velocidade['y'])
                prop.valores['velocidade_angular'].append(p.velocidade['angular'])
                prop.valores['velocidade_modulo'].append(math.sqrt(p.velocidade['x']**2 + p.velocidade['y']**2))
                prop.valores['massa'].append(p.massa)
                prop.valores['posicao_x'].append(p.posicao['x'])
                prop.valores['posicao_y'].append(p.posicao['y'])
                prop.valores['aceleracao_x'].append(p.aceleracao['x'])
                prop.valores['aceleracao_y'].append(p.aceleracao['y'])
                prop.valores['forca_x'].append(p.forca_total['x'])
                prop.valores['forca_y'].append(p.forca_total['y'])
                prop.valores['forca_modulo'].append(math.sqrt(p.forca_total['x']**2 + p.forca_total['y']**2))
                prop.valores['torque'].append(p.torque)

                quantidade_contatos = len(p.lista_contatos) + len(p.lista_contatos_objetos)
                prop.valores['quantidade_contatos'].append(quantidade_contatos)

            else:
                # lolzinho.append('-')

                prop.valores['velocidade_y'].append(np.NaN)
                prop.valores['velocidade_x'].append(np.NaN)
                prop.valores['velocidade_angular'].append(np.NaN)
                prop.valores['massa'].append(np.NaN)
                prop.valores['velocidade_modulo'].append(np.NaN)
                prop.valores['posicao_x'].append(np.NaN)
                prop.valores['posicao_y'].append(np.NaN)
                prop.valores['aceleracao_x'].append(np.NaN)
                prop.valores['aceleracao_y'].append(np.NaN)
                prop.valores['forca_x'].append(np.NaN)
                prop.valores['forca_y'].append(np.NaN)
                prop.valores['forca_modulo'].append(np.NaN)
                prop.valores['quantidade_contatos'].append(np.NaN)
                prop.valores['torque'].append(np.NaN)

            prop.valores['tempo'].append(sistema.tempo_simulado)

        plt.close('all')

        # print(lolzinho)
        # print(dados_particulas[4].valores['tempo'])

    dados = dict()
    for p_id in lista_particulas_alvo:
        df = pd.DataFrame.from_dict(dados_particulas[p_id].valores)
        dados[p_id] = df

    return dados


class ParticleTracker:
    def __init__(self, pasta):
        self.pasta = pasta
        self.pasta_temp = None
        # self.dados_particulas = dict()

    def run(self, lista_particulas_alvo):
        from os import listdir
        from os.path import isfile, join

        self.pasta_temp = self.pasta + '/temp/tracking/'
        lista_arquivos = [f for f in listdir(self.pasta) if isfile(join(self.pasta, f))]

        dados_particulas = processa_arquivos(lista_arquivos, self.pasta, self.pasta_temp, lista_particulas_alvo)

        print('Finalizando processamento de arquivos...')

        return dados_particulas