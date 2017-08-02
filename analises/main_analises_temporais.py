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

if __name__ == '__main__':

    # file_path = '../save/para_benchmark2/para_benchmark2_280'
    # file_path = '../save/sem_atrito/sem_atrito_280'

    # pasta = '../save/sem_atrito'
    pasta = 'D://SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_polid'
    pasta = 'D://SIMULACOES_DMCONVEYOR/atrp05_atrc05_h5_polid'
    pasta = 'D://SIMULACOES_DMCONVEYOR/atrp05_atrc05_h1_mono'
    pasta = 'D://SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono'
    pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono'
    pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_polid'
    pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono_inc-5'
    pasta = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR/atrp05_atrc05_h10_mono_inc5'

    stat = EstatisticaTemporal(pasta)

    # print('Criando as ROIs')
    # stat.set_roi(-0.5, -0.5, 0, 0.5, 'box_antes')
    # stat.set_roi(0, -0.5, 0.5, 0.5, 'box_depois')

    arquivo_dados = pasta + '/analises/dados'

    if 1:
        dados = stat.run()

        pasta_dados = pasta+'/analises'
        if not os.path.exists(pasta+'/analises'):
            os.makedirs(pasta+'/analises')

        pickle.dump(dados, open(pasta + '/analises/dados', 'wb'))

    dados = pickle.load(open(arquivo_dados, 'rb'))

    print(dados.columns.values.tolist())

    dados.sort_values(['iteracao'], inplace=True)
    # dados.sort_values(['v_max_depois'])
    # dados.sort_index(level = 'tempo')

    # print(dados.head())
    # print(dados.describe())
    # print(dados[['vx_media_depois', 'iteracao']])

    # dados.plot.scatter(x='iteracao', y='vx_media_depois')

    if 0:
        dados.fillna(0, inplace=True)

    # Plot ---------------------------------------------------------------------------------------------------
    #
    # fig, ax = plt.subplots(1)
    # ax.fill_between(dados.index, dados['vx_min_depois'], dados['vx_max_depois'], facecolor='black', alpha=0.1)
    # ax.plot(dados.index, dados['vx_media_depois'],'.-', label='mean Vx')
    # ax.plot(dados.index, dados['vx_max_depois'],'.-', label='max Vx')
    # ax.plot(dados.index, dados['vx_min_depois'],'.-', label='min Vx')
    # ax.set_xlabel('Simulation time [s]')
    # ax.set_ylabel('Velocity [m/s]')
    # ax.legend(loc='upper left')
    # ax.set_title('Vx after  belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')
    #
    #
    # fig2, ax = plt.subplots(1)
    # ax.fill_between(dados.index, dados['vx_min_durante'], dados['vx_max_durante'], facecolor='black', alpha=0.1)
    # ax.plot(dados.index, dados['vx_media_durante'],'.-', label='mean Vx')
    # ax.plot(dados.index, dados['vx_max_durante'],'.-', label='max Vx')
    # ax.plot(dados.index, dados['vx_min_durante'],'.-', label='min Vx')
    # ax.set_xlabel('Simulation time [s]')
    # ax.set_ylabel('Velocity [m/s]')
    # ax.legend(loc='upper left')
    # ax.set_title('Vx during belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')
    #
    #
    # fig3, ax = plt.subplots(1)
    # ax.fill_between(dados.index, dados['vx_min_antes'], dados['vx_max_antes'], facecolor='black', alpha=0.1)
    # ax.plot(dados.index, dados['vx_media_antes'],'.-', label='mean Vx')
    # ax.plot(dados.index, dados['vx_max_antes'],'.-', label='max Vx')
    # ax.plot(dados.index, dados['vx_min_antes'],'.-', label='min Vx')
    # ax.set_xlabel('Simulation time [s]')
    # ax.set_ylabel('Velocity [m/s]')
    # ax.legend(loc='upper left')
    # ax.set_title('Vx before  belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')

    fig = plt.figure()

    ax = fig.add_subplot(313)
    ax.fill_between(dados.index, dados['vx_min_depois'], dados['vx_max_depois'], facecolor='black', alpha=0.1)
    ax.plot(dados.index, dados['vx_media_depois'],'.-', label='mean Vx')
    ax.plot(dados.index, dados['vx_max_depois'],'.-', label='max Vx')
    ax.plot(dados.index, dados['vx_min_depois'],'.-', label='min Vx')
    ax.set_xlabel('Simulation time [s]')
    ax.set_ylabel('Velocity [m/s]')
    ax.legend(loc='upper left')
    # ax.set_title('Vx after  belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')
    ax.set_title('Vx after  belt\'s end\n')

    ax2 = fig.add_subplot(312, sharex=ax, sharey=ax)
    ax2.fill_between(dados.index, dados['vx_min_durante'], dados['vx_max_durante'], facecolor='black', alpha=0.1)
    ax2.plot(dados.index, dados['vx_media_durante'],'.-', label='mean Vx')
    ax2.plot(dados.index, dados['vx_max_durante'],'.-', label='max Vx')
    ax2.plot(dados.index, dados['vx_min_durante'],'.-', label='min Vx')
    ax2.set_xlabel('Simulation time [s]')
    ax2.set_ylabel('Velocity [m/s]')
    ax2.legend(loc='upper left')
    ax2.set_title('Vx during belt\'s end\n')

    ax3 = fig.add_subplot(311, sharex=ax, sharey=ax)
    ax3.fill_between(dados.index, dados['vx_min_antes'], dados['vx_max_antes'], facecolor='black', alpha=0.1)
    ax3.plot(dados.index, dados['vx_media_antes'],'.-', label='mean Vx')
    ax3.plot(dados.index, dados['vx_max_antes'],'.-', label='max Vx')
    ax3.plot(dados.index, dados['vx_min_antes'],'.-', label='min Vx')
    ax3.set_xlabel('Simulation time [s]')
    ax3.set_ylabel('Velocity [m/s]')
    ax3.legend(loc='upper left')
    ax3.set_title('Vx before  belt\'s end\n')
    
    # -------------
    
    if 0:

        fig = plt.figure()
    
        ax = fig.add_subplot(133)
        ax.fill_between(dados.index, dados['v_min_depois'], dados['v_max_depois'], facecolor='black', alpha=0.1)
        ax.plot(dados.index, dados['v_media_depois'],'.-', label='mean V')
        ax.plot(dados.index, dados['v_max_depois'],'.-', label='max V')
        ax.plot(dados.index, dados['v_min_depois'],'.-', label='min V')
        ax.set_xlabel('Simulation time [s]')
        ax.set_ylabel('Velocity [m/s]')
        ax.legend(loc='upper left')
        ax.set_title('V after belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')
    
        ax2 = fig.add_subplot(132, sharex=ax, sharey=ax)
        ax2.fill_between(dados.index, dados['v_min_durante'], dados['v_max_durante'], facecolor='black', alpha=0.1)
        ax2.plot(dados.index, dados['v_media_durante'],'.-', label='mean V')
        ax2.plot(dados.index, dados['v_max_durante'],'.-', label='max V')
        ax2.plot(dados.index, dados['v_min_durante'],'.-', label='min V')
        ax2.set_xlabel('Simulation time [s]')
        ax2.set_ylabel('Velocity [m/s]')
        ax2.legend(loc='upper left')
        ax2.set_title('V during belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')
    
        ax3 = fig.add_subplot(131, sharex=ax, sharey=ax)
        ax3.fill_between(dados.index, dados['v_min_antes'], dados['v_max_antes'], facecolor='black', alpha=0.1)
        ax3.plot(dados.index, dados['v_media_antes'],'.-', label='mean V')
        ax3.plot(dados.index, dados['v_max_antes'],'.-', label='max V')
        ax3.plot(dados.index, dados['v_min_antes'],'.-', label='min V')
        ax3.set_xlabel('Simulation time [s]')
        ax3.set_ylabel('Velocity [m/s]')
        ax3.legend(loc='upper left')
        ax3.set_title('V before  belt\'s end\n' + r'$\mu_(particle|particle) = 0.5$' + r'  $\mu_(particle|belt) = 0.50$')
    
    

    # plt.tight_layout(pad=0.5)
    ax.grid()
    ax2.grid()
    ax3.grid()
    plt.show()
