# -*- coding: utf-8 -*-
__author__ = 'Abraão'

from visualizador2 import mostrar_sistema3 as mostrar_sistema
from sys import platform, exit
import pickle
from os.path import isfile, join
import matplotlib.pyplot as plt
import os

def gera_frame(args):

    arquivo, pastaframes, nomesimulacao = args

    print('Processando arquivo ' + arquivo)
    # print(pasta_frames)

    frame_number = str(arquivo).split('_')[-1]
    sistema_temp = pickle.load(open(arquivo, 'rb'))
    plt.close('all')

    exibir = {'particulas_livres': True,
              'velocidades': 0,
              'labels_particulas_livres': 0,
              'labels_particulas_fixas': False,
              'forcas_particulas_livres': False,
              'contatos': 0,
              'paredes': False,
              'correia': False,
              'limites': True,
              'objetos': True,
              'inlet': True,
              'rois': True}

    fig = plt.figure(figsize=(19, 10))
    # figura = mostrar_sistema(sistema_temp, fig, 'x', manual=False, exibir=exibir)

    titulo = 'Simulação - {} \n'.format(nomesimulacao)
    figura = mostrar_sistema(sistema_temp, fig, 'x', manual=True, valores=[3, 10], exibir=exibir,
                             janela=[-4, -1.5, 2, 2], titulo=titulo)
    figura.tight_layout()

    # print(pasta_frames)
    frame_filename = pastaframes + '/frame_' + str(frame_number).zfill(5) + '.jpg'
    figura.savefig(frame_filename)
    plt.close(figura)
    # plt.show()

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

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

    pasta_analises = pasta_raiz + '/analises - ' + nome_simulacao

    pasta_frames = pasta_analises + '/frames'

    if not os.path.exists(pasta_frames):
        os.makedirs(pasta_frames)

    lista_arquivos = [join(pasta_raiz, f) for f in os.listdir(pasta_raiz) if isfile(join(pasta_raiz, f))]

    i = 10

    # print(lista_arquivos[i])

    from multiprocessing import Pool
    parametros = list(zip(lista_arquivos, [pasta_frames]*len(lista_arquivos), [nome_simulacao]*len(lista_arquivos)))
    # parametros = list(zip(lista_arquivos[0:10], [pasta_frames]*10))

    teste = 0

    if teste:
        gera_frame((lista_arquivos[10], pasta_frames, nome_simulacao))

    if 0:
        pool = Pool(6)
        pool.map(gera_frame, parametros)
        pool.close()
        pool.join()

    if 1:

        FFMPEG_BIN = "ffmpeg"
        fps = '25'
        import subprocess as sp
        command = [FFMPEG_BIN,
                   '-qscale', '5',
                   '-r', fps,
                   '-i', pasta_frames+'/frame_%04d.jpg',
                   '-b:a', '1800',
                   pasta_frames+'/aa_shazan.mp4']

        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
