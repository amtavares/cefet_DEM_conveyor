# -*- coding: utf-8 -*-
__author__ = 'abraao'

import pickle
from analises.analise_estatica import Estatistica
from analises.analise_temporal import EstatisticaTemporal
import pandas as pd
import os
import matplotlib.pylab as plt

pd.set_option('expand_frame_repr', False)
# plt.style.use('ggplot')
import math

if __name__ == '__main__':

    # pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono_inc-5'
    # pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono'
    # pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono_inc5'

    pastas = list()
    pastas.append('/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono_inc-5')
    pastas.append('/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono')
    pastas.append('/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono_inc5')

    angulos = [-5, 0, 5]

    fig, ax = plt.subplots(1)

    for i, pasta in enumerate(pastas):

        stat = EstatisticaTemporal(pasta)

        arquivo_dados = pasta + '/analises/dados'

        dados = pickle.load(open(arquivo_dados, 'rb'))
        dados.sort_values(['iteracao'], inplace=True)

        vxmed = dados[dados.index >= 3.0]['vx_media_depois']
        vxmax = dados[dados.index >= 3.0]['vx_max_depois']
        vxmin = dados[dados.index >= 3.0]['vx_min_depois']

        vxmed_media = vxmed.mean()
        vxmed_erro = (vxmed.max() - vxmed.min()) / math.sqrt(3)
        vxmax_media = vxmax.mean()
        vxmax_erro = (vxmax.max() - vxmax.min()) / math.sqrt(3)
        vxmin_media = vxmin.mean()
        vxmin_erro = (vxmin.max() - vxmin.min()) / math.sqrt(3)

        angulo = angulos[i]

        # Plot
        # Linha vertical
        # ax.plot([angulo, angulo], [vxmin, vxmax], 'k')
        
        espessura = 2
        cps = 5

        # Minimo
        ax.errorbar(angulo, vxmin_media, yerr=vxmin_erro, elinewidth=espessura, capthick=espessura, capsize=cps, ecolor='r')
        ax.plot(angulo, vxmin_media, 'sr', label='min', markersize=10)

        # Media
        ax.errorbar(angulo, vxmed_media, yerr=vxmed_erro, elinewidth=espessura, capthick=espessura, capsize=cps, ecolor='b')
        ax.plot(angulo, vxmed_media, 'ob', label='mean', markersize=10)

        # Maximo
        ax.errorbar(angulo, vxmax_media, yerr=vxmax_erro, elinewidth=espessura, capthick=espessura, capsize=cps, ecolor='g')
        ax.plot(angulo, vxmax_media, 'sg', label='max', markersize=10)

        ax.set_xlabel('Belt slope [degrees]')
        ax.set_ylabel('Velocity [m/s]')
        # ax.legend(loc='upper left')
        ax.set_title('Vx after belt')


    # plt.legend([minimo, maximo, media], ['min', 'max', 'mean'])
    plt.xticks(angulos, angulos)
    plt.grid()
    plt.show()





