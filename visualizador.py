# -*- coding: utf-8 -*-
__author__ = 'abraao'
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import math
import numpy as np


def mostrar_sistema(sistema, figura, exibir={}):
    if len(exibir) == 0:
        exibir = {'particulas_livres': True,
                  'velocidades': False,
                  'labels_particulas_livres': False,
                  'labels_particulas_fixas': False,
                  'forcas_particulas_livres': False,
                  'contatos':True,
                  'paredes':True,
                  'correia':True,
                  'limites':True,
                  }

    if not hasattr(sistema, 'lista_contatos'):
        exibir['contatos'] = False

    particulas = sistema.lista_particulas
    livres = sistema.lista_particulas_livres
    fixas = sistema.lista_particulas_fixas
    if hasattr(sistema, 'lista_contatos'):
        contatos = sistema.lista_contatos
        contatos_existentes = sistema.lista_contatos_existentes
    else:
        contatos = []
        contatos_existentes = []

    # plt.figure()
    # plt.axes()
    # ax = sistema.axis

    fig = figura
    fig.clf()
    ax = fig.add_subplot(1, 1, 1)
    if hasattr(sistema, 'iteracao'):
        fig.suptitle('Iteracao: {}  -  {:.2f} segundos'.format(sistema.iteracao, sistema.tempo_simulado))
    else:
        fig.suptitle('Preparando sistema')

    ax.clear()

    # Partículas livres ------------------------------------------------------------------------------------------------
    if exibir['particulas_livres']:
        lista_objetos = []
        velocidades = []
        for pid in livres:
            p = particulas[pid]
            x = p.posicao['x']
            y = p.posicao['y']
            raio = p.raio
            circle = plt.Circle((x, y), radius=raio, fc='y')
            lista_objetos.append(circle)
            # Calculo da variável para colorir as partículas
            try:
                velocidade_modulo = math.sqrt(p.velocidade['x'] ** 2 + p.velocidade['y'] ** 2)
            except:
                velocidade_modulo = 0

            # velocidades.append(p.velocidade['x'])
            # velocidades.append(p.velocidade['y'])
            velocidades.append(velocidade_modulo)
            # ax.add_patch(circle)

        # Labels
        if exibir['labels_particulas_livres']:
            plt.text(x, y, p.id)

        # Setas:
        comprimento = 0.3
        # Forças
        if exibir['forcas_particulas_livres']:
            try:
                modulo = math.sqrt(p.forca_total['x'] ** 2 + p.forca_total['y'] ** 2)
                dx = comprimento * p.forca_total['x'] / modulo
                dy = comprimento * p.forca_total['y'] / modulo
                ax.arrow(x, y, dx, dy, color='m', head_width=0.01, head_length=0.01)
            except:
                pass

        # Velocidades
        if exibir['velocidades']:
            modulo = math.sqrt(p.velocidade['x'] ** 2 + p.velocidade['y'] ** 2)
            dx = comprimento * p.velocidade['x']
            dy = comprimento * p.velocidade['y']
            ax.arrow(x, y, dx, dy, color='c', head_width=0.01 * modulo, head_length=0.01 * modulo)

        col = PatchCollection(lista_objetos)
        col.set(array=np.array(velocidades), cmap='jet')
        ax.add_collection(col)
        cb = fig.colorbar(col)
        # plt.clim(0,5)
        # plt.set(cb, vmin=0, vmax=5)

    # Partículas fixas  ------------------------------------------------------------------------------------------------
        for pid in fixas:
            p = particulas[pid]
            # grupo = p.grupo
            if exibir['paredes'] and p.grupo == 'parede':
                x = p.posicao['x']
                y = p.posicao['y']
                raio = p.raio
                circle = plt.Circle((x, y), radius=raio, fc='#B8B8B8')
                ax.add_patch(circle)

            if exibir['correia'] and p.grupo == 'correia':
                x = p.posicao['x']
                y = p.posicao['y']
                raio = p.raio
                circle = plt.Circle((x, y), radius=raio, fc='#B8B8B8')
                ax.add_patch(circle)

            # Labels
            if exibir['labels_particulas_fixas']:
                plt.text(x, y, p.id)

    # Contatos ---------------------------------------------------------------------------------------------------------
    if exibir['contatos']:
        if len(contatos_existentes):
            for cid in contatos_existentes:
                c = contatos[cid]
                x1 = c.particula1.posicao['x']
                y1 = c.particula1.posicao['y']
                x2 = c.particula2.posicao['x']
                y2 = c.particula2.posicao['y']
                if c.deslizante:
                    estilo = 'g--'
                else:
                    estilo = 'g'
                ax.plot([x1, x2], [y1, y2], estilo)

    # Limites  ---------------------------------------------------------------------------------------------------------
    if exibir['limites']:

        lxmin = sistema.limites['xmin']
        lxmax = sistema.limites['xmax']
        lymin = sistema.limites['ymin']
        lymax = sistema.limites['ymax']
        estilo = '-y'
        ax.plot([lxmin, lxmin, lxmax, lxmax, lxmin], [lymin, lymax, lymax, lymin, lymin], estilo)


    ax.axis('scaled')
    fig.canvas.draw()
    plt.grid()
    # plt.show()
    plt.pause(0.001)
