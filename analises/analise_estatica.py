# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import math

__author__ = 'abraao'


class Estatistica:
    def __init__(self, sistema):
        self.sistema = sistema
        self.rois = {}  # Key: nome da roi, Value: dictionary com as propriedades calculadas
        pass

    def set_roi(self, x1, y1, x2, y2, nome):
        # nova_roi = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'lista_particulas': self.update_roi(nome)}
        nova_roi = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        self.rois[nome] = nova_roi
        self.update_roi(nome)

    def update_roi(self, nome_roi):
        lista_particulas_roi = list()

        for particula_id, particula in self.sistema.lista_particulas.items():
            if self.particula_na_roi(nome_roi, particula):
                lista_particulas_roi.append(particula_id)

        self.rois[nome_roi]['lista_particulas'] = lista_particulas_roi

    def particula_na_roi(self, nome_roi, particula):
        xmax = max(self.rois[nome_roi]['x1'], self.rois[nome_roi]['x2'])
        xmin = min(self.rois[nome_roi]['x1'], self.rois[nome_roi]['x2'])
        ymax = max(self.rois[nome_roi]['y1'], self.rois[nome_roi]['y2'])
        ymin = min(self.rois[nome_roi]['y1'], self.rois[nome_roi]['y2'])

        pertence = False

        if particula.posicao['x'] > xmin:
            if particula.posicao['x'] < xmax:
                if particula.posicao['y'] > ymin:
                    if particula.posicao['y'] < ymax:
                        pertence = True

        return pertence

    def estatistica_particulas(self, nome_roi=False):
        sistema = self.sistema
        if nome_roi:
            # print('Gerando dados da ROI ' + nome_roi)
            lista_particulas = self.rois[nome_roi]['lista_particulas']
        else:
            # print('Gerando dados do sistema todo')
            lista_particulas = sistema.lista_particulas_livres

        propriedades = {
            'velocidade_x': list(),
            'velocidade_y': list(),
            'velocidade_modulo': list(),
            'massa': list(),
            'posicao_x': list(),
            'posicao_y': list(),
            'aceleracao_x': list(),
            'aceleracao_y': list(),
            'forca_x': list(),
            'forca_y': list(),
            'forca_modulo': list(),
        }

        if len(lista_particulas) > 0:
            for p_id in lista_particulas:
                p = sistema.lista_particulas[p_id]

                propriedades['velocidade_x'].append(p.velocidade['x'])
                propriedades['velocidade_y'].append(p.velocidade['y'])
                propriedades['velocidade_modulo'].append(math.sqrt(p.velocidade['x']**2 + p.velocidade['y']**2))
                propriedades['massa'].append(p.massa)
                propriedades['posicao_x'].append(p.posicao['x'])
                propriedades['posicao_y'].append(p.posicao['y'])
                propriedades['aceleracao_x'].append(p.aceleracao['x'])
                propriedades['aceleracao_y'].append(p.aceleracao['y'])
                propriedades['forca_x'].append(p.forca_total['x'])
                propriedades['forca_y'].append(p.forca_total['y'])
                propriedades['forca_modulo'].append(math.sqrt(p.forca_total['x']**2 + p.forca_total['y']**2))
        else:
            for prop, prop_valores in propriedades.items():
                propriedades[prop].append(np.NaN)

        estatisticas = pd.DataFrame()
        for prop, prop_valores in propriedades.items():
            estatisticas[prop] = pd.Series(prop_valores)

        return estatisticas

    def estatistica_contatos(self):
        sistema = self.sistema

        interpenetracoes = []
        for c_id, c in sistema.lista_contatos.items():
            interpenetracoes.append(c.distancia)

        interpenetracoes = np.array(interpenetracoes)

        return interpenetracoes.mean()

