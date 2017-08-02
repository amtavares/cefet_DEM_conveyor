# -*- coding: utf-8 -*-
__author__ = 'abraao'

from particula import Particula
from objetos import ObjetoLinha
import math
import numpy as np


class Contato:

    def __init__(self, config=None):
        self.id = None              # string da id do contato, deve ser gerada pela função utilidades.ids2str

        self.particula1 = Particula()
        self.particula2 = Particula()

        self.passo_de_tempo = None

        self.kn_equivalente = None
        self.gn_equivalente = None
        self.mi_equivalente = 0.5

        self.distancia = None
        self.distancia_centros = None
        self.angulo_contato = None  # Em radianos, orientado como o circulo trignometrico

        self.forca_normal = {'x': None, 'y': None, 'modulo': None}
        self.forca_tangencial = {'x': None, 'y': None, 'modulo': None}
        self.forca_tangencial_anterior = None
        self.forca_total = {'x': None, 'y': None, 'modulo': None}
        self.torque = None

        self.deslizante = None

        self.existencia = []  # lista de iterações nas quais este contato existe
        self.iteracao_atual = None

        # Em qual iteração foi feito o ultimo update deste contato
        # Serve para não computar 2 vezes
        self.ultimo_update = None  # TODO Acho que não precisa disso mais

        if config:
            pass

    def calcula_forcas(self):

        # Atribuindo variáveis para melhorar a leitura do código

        # v1x = self.particula1.velocidade_predita['x']
        # v1y = self.particula1.velocidade_predita['y']
        # v2x = self.particula2.velocidade_predita['x']
        # v2y = self.particula2.velocidade_predita['y']
        delta_t = self.passo_de_tempo
        v1angular = self.particula1.velocidade_predita['angular']
        v2angular = self.particula2.velocidade_predita['angular']
        raio1 = self.particula1.raio
        raio2 = self.particula2.raio
        kn1 = self.particula1.material.kn
        kn2 = self.particula2.material.kn
        gn1 = self.particula1.material.gn
        gn2 = self.particula2.material.gn

        # Calculando variáveis intermediárias

        self.kn_equivalente = self.calcula_kn_equivalente(kn1, kn2)
        self.gn_equivalente = self.calcula_gn_equivalente(gn1, gn2)

        delta_x = self.particula2.posicao_predita['x'] - self.particula1.posicao_predita['x']
        delta_y = self.particula2.posicao_predita['y'] - self.particula1.posicao_predita['y']
        delta_vx = self.particula2.velocidade_predita['x'] - self.particula1.velocidade_predita['x']
        delta_vy = self.particula2.velocidade_predita['y'] - self.particula1.velocidade_predita['y']

        cosseno = delta_x/self.distancia_centros
        seno = delta_y/self.distancia_centros

        vel_relativa_normal = cosseno*(delta_vx) + seno*(delta_vy)  # vijn
        vel_relativa_tangencial = (-seno*(delta_vx) + cosseno*(delta_vy)) - v1angular*raio1 - v2angular*raio2   # vijt

        # Calculando as forças normais -------------------------------
        forca_normal_elastica = - self.kn_equivalente * self.distancia
        forca_normal_viscosa = - self.gn_equivalente * vel_relativa_normal
        forca_normal_modulo = forca_normal_elastica + forca_normal_viscosa

        # Calculando as forças tangenciais --------------------------
        # fta = 0
        if self.iteracao_atual-1 in self.existencia:
            fta = self.forca_tangencial_anterior['modulo']  # Força tangencial anterior
        else:
            fta = 0

        forca_tangencial_elastica = fta - self.kn_equivalente * vel_relativa_tangencial * delta_t
        forca_atrito = self.mi_equivalente * forca_normal_modulo

        # Testa se a força tangencial é maior que a de atrito dinamico
        if abs(forca_tangencial_elastica) > forca_atrito:
            self.deslizante = True
            if forca_tangencial_elastica > 0:
                forca_tangencial_elastica = forca_atrito
            else:
                forca_tangencial_elastica = -forca_atrito
        else:
            self.deslizante = False

        forca_tangencial_modulo = forca_tangencial_elastica

        # Atualiza --------------------------------------------------
        # Transformando as forças para o sistema global
        fnx = forca_normal_modulo * cosseno
        fny = forca_normal_modulo * seno

        ftx = forca_tangencial_modulo * -seno
        fty = forca_tangencial_modulo * cosseno

        self.forca_normal['x'] = fnx
        self.forca_normal['y'] = fny
        self.forca_normal['modulo'] = forca_normal_modulo

        self.forca_tangencial['x'] = ftx
        self.forca_tangencial['y'] = fty
        self.forca_tangencial['modulo'] = forca_tangencial_modulo

        # self.forca_total['x'] = forca_normal_modulo * cosseno + forca_tangencial_modulo * (-seno)
        # self.forca_total['y'] = forca_normal_modulo * seno + forca_tangencial_modulo * cosseno
        self.forca_total['x'] = -(fnx + ftx)
        self.forca_total['y'] = -(fny + fty)

        # self.forca_total['modulo'] = math.sqrt(self.forca_total['x']**2 + self.forca_total['y']**2)

        self.forca_tangencial_anterior = self.forca_tangencial.copy()

    def calcula_kn_equivalente(self, kn1, kn2):
        if kn1 == kn2:
            return kn1

        modelo = 1
        kn = None
        # Modelo de molas em série
        if modelo == 1:
            kn = (kn1 + kn2)/2
        elif modelo == 2:
            kn = 1/(1/kn1 + 1/kn2)

        return kn

    def calcula_gn_equivalente(self, gn1, gn2):
        if gn1 == gn2:
            return gn1

        modelo = 1
        gn = None
        # Modelo de molas em série
        if modelo == 1:
            gn = (gn1 + gn2) / 2
        elif modelo == 2:
            gn = 1 / (1 / gn1 + 1 / gn2)

        return gn


class Contato_objeto:
    def __init__(self):
        self.id = None  # string da id do contato, deve ser gerada pela função utilidades.ids2str

        self.particula = Particula()
        self.objeto = ObjetoLinha() 
        # self.particula2 = Particula()

        self.passo_de_tempo = None

        self.kn_equivalente = None
        self.gn_equivalente = None
        self.mi_equivalente = 0.5

        self.distancia = None
        self.distancia_centros = None
        self.angulo_contato = None  # Em radianos, orientado como o circulo trignometrico
        self.ponto_contato = None

        self.forca_normal = {'x': None, 'y': None, 'modulo': None}
        self.forca_tangencial = {'x': None, 'y': None, 'modulo': None}
        self.forca_tangencial_anterior = None
        self.forca_total = {'x': None, 'y': None, 'modulo': None}
        self.torque = None

        self.deslizante = None

        self.existencia = []  # lista de iterações nas quais este contato existe
        self.iteracao_atual = None

        # Em qual iteração foi feito o ultimo update deste contato
        # Serve para não computar 2 vezes
        self.ultimo_update = None  # TODO Acho que não precisa disso mais


    def calcula_forcas(self):
        # print('calc forças {}'.format(self.id))
        # Atribuindo variáveis para melhorar a leitura do código

        delta_t = self.passo_de_tempo
        v1x = self.particula.velocidade_predita['x']
        v1y = self.particula.velocidade_predita['y']
        v1angular = self.particula.velocidade_predita['angular']
        raio1 = self.particula.raio
        kn1 = self.particula.material.kn
        gn1 = self.particula.material.gn

        v2x = self.objeto.velocidadevetor[0]
        v2y = self.objeto.velocidadevetor[1]
        kn2 = self.objeto.material.kn
        gn2 = self.objeto.material.gn
        # v2angular = 0
        # raio2 = 0

        # Calculando variáveis intermediárias

        self.kn_equivalente = self.calcula_kn_equivalente(kn1, kn2)
        self.gn_equivalente = self.calcula_gn_equivalente(gn1, gn2)

        # Determinando o ponto de contato

        # self.ponto_contato, self.distancia = calcula_contato_objeto(self.particula, self.objeto)

        delta_x = self.ponto_contato[0] - self.particula.posicao_predita['x']
        delta_y = self.ponto_contato[1] - self.particula.posicao_predita['y']


        cosseno = delta_x / self.distancia_centros
        seno = delta_y / self.distancia_centros

        # Daqui pra baixo é igual à classe de contato partícula-partícula

        vel_relativa_normal = cosseno * (v2x - v1x) + seno * (v2y - v1y)  # vijn
        vel_relativa_tangencial = (-seno * (v2x - v1x) + cosseno * (v2y - v1y)) - v1angular * raio1  # vijt

        # Calculando as forças normais -------------------------------
        forca_normal_elastica = - self.kn_equivalente * self.distancia
        forca_normal_viscosa = - self.gn_equivalente * vel_relativa_normal
        forca_normal_modulo = forca_normal_elastica + forca_normal_viscosa

        # Calculando as forças tangenciais --------------------------
        # fta = 0
        if self.iteracao_atual - 1 in self.existencia:
            fta = self.forca_tangencial_anterior['modulo']  # Força tangencial anterior
        else:
            fta = 0

        forca_tangencial_elastica = fta - self.kn_equivalente * vel_relativa_tangencial * delta_t
        forca_atrito = self.mi_equivalente * forca_normal_modulo

        # Testa se a força tangencial é maior que a de atrito dinamico
        if abs(forca_tangencial_elastica) > forca_atrito:
            self.deslizante = True
            if forca_tangencial_elastica > 0:
                forca_tangencial_elastica = forca_atrito
            else:
                forca_tangencial_elastica = -forca_atrito
        else:
            self.deslizante = False

        forca_tangencial_modulo = forca_tangencial_elastica

        # Atualiza --------------------------------------------------
        # Transformando as forças para o sistema global
        fnx = forca_normal_modulo * cosseno
        fny = forca_normal_modulo * seno

        ftx = forca_tangencial_modulo * -seno
        fty = forca_tangencial_modulo * cosseno

        self.forca_normal['x'] = fnx
        self.forca_normal['y'] = fny
        self.forca_normal['modulo'] = forca_normal_modulo

        self.forca_tangencial['x'] = ftx
        self.forca_tangencial['y'] = fty
        self.forca_tangencial['modulo'] = forca_tangencial_modulo

        # self.forca_total['x'] = forca_normal_modulo * cosseno + forca_tangencial_modulo * (-seno)
        # self.forca_total['y'] = forca_normal_modulo * seno + forca_tangencial_modulo * cosseno
        self.forca_total['x'] = -(fnx + ftx)
        self.forca_total['y'] = -(fny + fty)

        self.forca_total['modulo'] = math.sqrt(self.forca_total['x'] ** 2 + self.forca_total['y'] ** 2)

        self.forca_tangencial_anterior = self.forca_tangencial.copy()

    def calcula_kn_equivalente(self, kn1, kn2):
        if kn1 == kn2:
            return kn1

        modelo = 1
        kn = None
        # Modelo de molas em série
        if modelo == 1:
            kn = (kn1 + kn2) / 2
        elif modelo == 2:
            kn = 1 / (1 / kn1 + 1 / kn2)

        return kn

    def calcula_gn_equivalente(self, gn1, gn2):
        if gn1 == gn2:
            return gn1

        modelo = 1
        gn = None
        # Modelo de molas em série
        if modelo == 1:
            gn = (gn1 + gn2) / 2
        elif modelo == 2:
            gn = 1 / (1 / gn1 + 1 / gn2)

        return gn


# Função independente das classes ======================================================================================
def calcula_contato_objeto(particula, objeto):

    tipo_objeto = 1

    if tipo_objeto == 1:

        pini = objeto.ponto_inicial
        pfinal = objeto.ponto_final
        circ_centro = np.array([particula.posicao['x'], particula.posicao['y']])
        circ_raio = particula.raio

        def closest_point_on_seg(seg_a, seg_b, circ_pos):
            seg_v = seg_b - seg_a
            pt_v = circ_pos - seg_a
            seg_v_comp = np.linalg.norm(seg_v)
            if seg_v_comp <= 0:
                raise ValueError("Invalid segment length")
            seg_v_unit = seg_v / seg_v_comp
            proj = pt_v.dot(seg_v_unit)
            if proj <= 0:
                # print('Ob 3')
                return seg_a.copy()
            if proj >= seg_v_comp:
                # print('Ob 4')
                return seg_b.copy()
            proj_v = seg_v_unit * proj
            closest = proj_v + seg_a

            return closest

        closest = closest_point_on_seg(pini, pfinal, circ_centro)
        dist_v = circ_centro - closest
        dist_v_comp = np.linalg.norm(dist_v)

        if dist_v_comp > circ_raio:
            # print('Ob 1')
            # return np.array([0, 0])
            return False, dist_v_comp
        if dist_v_comp <= 0:
            # print('Ob 2')
            raise ValueError("Circle's center is exactly on segment")

        # offset = dist_v / dist_v_comp * (circ_rad - dist_v_comp)
        # print('Offset')
        # print(dist_v)
        # return offset

        # -dist_ é a distancia x e y do centro do circulo ao ponto de contato
        # dist_v_comp é o modulo desta distancia

        # Colocando o ponto de contato na superfície do círculo
        dist_v_unit = -dist_v / dist_v_comp
        ponto_local = dist_v_unit*circ_raio

        # ponto_local é a distancia x e y do centro do circulo à projecao do ponto de contato na borda do circulo
        # dist_v_comp é a distancia do centro ao ponto de contato real (contando a interpenetracao
        return ponto_local, dist_v_comp,
