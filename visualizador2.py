# -*- coding: utf-8 -*-
__author__ = 'abraao'
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import PatchCollection
import math
import numpy as np
from contato import Contato, Contato_objeto



def mostrar_sistema(sistema, figura, vel, manual, valores = [], exibir={}, ):
    if len(exibir) == 0:
        exibir = {'particulas_livres': True,
                  'velocidades': True,
                  'labels_particulas_livres': False,
                  'labels_particulas_fixas': False,
                  'forcas_particulas_livres': False,
                  'contatos':True,
                  'paredes':False,
                  'correia':False,
                  'limites':True,
                  'objetos':True
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
    # fig.clf()
    ax = fig.add_subplot(1, 1, 1)
    if hasattr(sistema, 'iteracao'):
        fig.suptitle('Iteracao: {}  -  {:.2f} segundos'.format(sistema.iteracao, sistema.tempo_simulado))
    else:
        fig.suptitle('Preparando sistema')

    # ax.clear()

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

            if vel == 'x':
                velocidades.append(p.velocidade['x'])
            elif vel == 'y':
                velocidades.append(p.velocidade['y'])
            elif vel == 'modulo':
                velocidades.append(velocidade_modulo)

            # ax.add_patch(circle)

            # Labels
            if exibir['labels_particulas_livres']:
                print('wow')
                # plt.text(x, y, p.id)
                ax.text(x, y, p.id)

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
        # cb = fig.colorbar(col)

        if manual == True:
            # plt.set(cb, valores[0], valores[1])
            norm = mpl.colors.Normalize(vmin=valores[0], vmax=valores[1])
            cb = fig.colorbar(col, norm=norm)
            # cb = fig.colorbar(col, ticks=[valores[0],(valores[0] + valores[1])/2, valores[1]])
            cb.set_clim(valores[0], valores[1])
        else:
            cb = fig.colorbar(col)
            pass


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
    plt.grid()
    # fig.canvas.draw()
    # plt.show()
    # plt.pause(0.001)

    return fig


def mostrar_sistema3(sistema, figura, vel, manual, valores=None, exibir={}, janela=None, titulo=''):
    if len(exibir) == 0:
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

    fig = figura
    ax = fig.add_subplot(1, 1, 1)

    subtitulo = ''
    if vel == 'x':
        subtitulo = 'Particle color by x component of velocity (Vx)'
    elif vel == 'y':
        subtitulo = 'Particle color by y component of velocity (Vy)'
    elif vel == 'modulo':
        subtitulo = 'Particle color by velocity modulus (V)'


    if hasattr(sistema, 'iteracao'):
        fig.suptitle(titulo + 'Time: {1:.2f} seconds, Iteration: {0}\n{2}'
                     .format(sistema.iteracao, sistema.tempo_simulado, subtitulo), fontsize=10)
    else:
        fig.suptitle('Preparando sistema')

    # ax.clear()

    # Partículas livres ------------------------------------------------------------------------------------------------
    if exibir['particulas_livres']:
        lista_objetos = []
        velocidades = []
        for pid in livres:
            p = particulas[pid]
            x = p.posicao['x']
            y = p.posicao['y']
            raio = p.raio
            circle = plt.Circle((x, y), radius=raio, fc='y', linewidth=0)
            lista_objetos.append(circle)
            # Calculo da variável para colorir as partículas
            try:
                velocidade_modulo = math.sqrt(p.velocidade['x'] ** 2 + p.velocidade['y'] ** 2)
            except:
                velocidade_modulo = 0

            if vel == 'x':
                velocidades.append(p.velocidade['x'])
            elif vel == 'y':
                velocidades.append(p.velocidade['y'])
            elif vel == 'modulo':
                velocidades.append(velocidade_modulo)

            # ax.add_patch(circle)

            # Labels
            if exibir['labels_particulas_livres']:
                # plt.text(x, y, p.id)
                ax.text(x, y, p.id)

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

        # construção das variaǘeis para a legenda
        if manual:

            cb_minimo = valores[0]
            cb_maximo = valores[1]
            velocidades = [cb_minimo if v <= cb_minimo else cb_maximo if v >= cb_maximo else v for v in velocidades]

        if len(velocidades) > 0:
            ticks = np.linspace(min(velocidades), max(velocidades), num=10)
        else:
            ticks = [0]

        col.set(array=np.array(velocidades), cmap='jet', edgecolor=None, linewidth=0.5)

        # Adicionando os círculos na figura e criando a legenda
        ax.add_collection(col)
        cbar = fig.colorbar(col, ticks=ticks, orientation='horizontal', fraction=0.07)
        cbar.ax.tick_params(labelsize=10)

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
    if exibir['objetos']:
        for objeto in sistema.lista_objetos.values():
            x1 = objeto.ponto_inicial[0]
            y1 = objeto.ponto_inicial[1]
            x2 = objeto.ponto_final[0]
            y2 = objeto.ponto_final[1]

            ax.plot([x1, x2], [y1, y2], 'k', linewidth=2)

    # Contatos ---------------------------------------------------------------------------------------------------------
    if exibir['contatos']:
        if len(contatos_existentes):
            for cid in contatos_existentes:
                c = contatos[cid]
                x1 = x2 = y1 = y2 = None
                if type(c) is Contato:
                    x1 = c.particula1.posicao['x']
                    y1 = c.particula1.posicao['y']
                    x2 = c.particula2.posicao['x']
                    y2 = c.particula2.posicao['y']
                elif type(c) is Contato_objeto:
                    x1 = c.particula.posicao['x']
                    y1 = c.particula.posicao['y']
                    x2 = c.ponto_contato[0]
                    y2 = c.ponto_contato[1]
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

    # Inlet    ---------------------------------------------------------------------------------------------------------
    if exibir['inlet']:
        x1 = sistema.inlet.x1
        y1 = sistema.inlet.y1
        x2 = sistema.inlet.x2
        y2 = sistema.inlet.y2

        ax.plot([x1, x2], [y1, y2], '#C8CBCC', linewidth=2)

    # ROIs -------------------------------------------------------------------------------------------------------------

    if exibir['rois']:

        largura_rois = 0.5
        altura_rois = 1
        ybase_rois = -0.5
        y1 = ybase_rois
        y2 = y1 + altura_rois

        lxmin = -largura_rois/2
        lxmax = largura_rois/2
        lymin = y1
        lymax = y2
        estilo = '#800000'
        ax.plot([lxmin, lxmin, lxmax, lxmax, lxmin], [lymin, lymax, lymax, lymin, lymin], estilo)
        ax.text(lxmin, lymax, 'During')

        lxmin = -(largura_rois/2 + largura_rois)
        lxmax = -largura_rois /2
        lymin = y1
        lymax = y2
        estilo = '#800000'
        ax.plot([lxmin, lxmin, lxmax, lxmax, lxmin], [lymin, lymax, lymax, lymin, lymin], estilo)
        ax.text(lxmin, lymax, 'Before')

        lxmin = largura_rois / 2
        lxmax = largura_rois / 2 + largura_rois
        lymin = y1
        lymax = y2
        estilo = '#800000'
        ax.plot([lxmin, lxmin, lxmax, lxmax, lxmin], [lymin, lymax, lymax, lymin, lymin], estilo)
        ax.text(lxmin, lymax, 'After')

    # Fim dos plots, ultimos ajustes na  figura ------------------------------------------------------------------------

    ax.axis('scaled')
    if janela:
        ax.set_xlim((janela[0], janela[2]))
        ax.set_ylim((janela[1], janela[3]))
        pass

    ax.grid()
    # ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=10)

    # fig.canvas.draw()
    # plt.show()
    # plt.pause(0.001)

    return fig
