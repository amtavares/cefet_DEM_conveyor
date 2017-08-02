# -*- coding: utf-8 -*-
#!/usr/bin/env pypy

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
        p1 = Particula()
        p2 = Particula()

        p1 = self.particula1
        p2 = self.particula2
        
        # Atribuindo variáveis para melhorar a leitura do código
        delta_t = self.passo_de_tempo
        v1angular = p1.velocidade_predita['angular']
        v2angular = p2.velocidade_predita['angular']
        raio1 = p1.raio
        raio2 = p2.raio
        kn1 = p1.material.kn
        kn2 = p2.material.kn
        gn1 = p1.material.gn
        gn2 = p2.material.gn
        distancia_centros = self.distancia_centros
        calcula_valor_equivalente = self.calcula_valor_equivalente
        distancia_contato = self.distancia
        
        # Calculando variáveis intermediárias
        if kn1 == kn2:
            kn_equivalente = kn1
        else:
            kn_equivalente = calcula_valor_equivalente(kn1, kn2)

        if gn1 == gn2:
            gn_equivalente = gn1
        else:
            gn_equivalente = calcula_valor_equivalente(gn1, gn2)

        delta_x = p2.posicao_predita['x'] - p1.posicao_predita['x']
        delta_y = p2.posicao_predita['y'] - p1.posicao_predita['y']
        delta_vx = p2.velocidade_predita['x'] - p1.velocidade_predita['x']
        delta_vy = p2.velocidade_predita['y'] - p1.velocidade_predita['y']

        cosseno = delta_x/distancia_centros
        seno = delta_y/distancia_centros

        vel_relativa_normal = cosseno*(delta_vx) + seno*(delta_vy)  # vijn
        vel_relativa_tangencial = (-seno*(delta_vx) + cosseno*(delta_vy)) - v1angular*raio1 - v2angular*raio2   # vijt

        # Calculando as forças normais -------------------------------
        forca_normal_elastica = - kn_equivalente * distancia_contato
        forca_normal_viscosa = - gn_equivalente * vel_relativa_normal
        forca_normal_modulo = forca_normal_elastica + forca_normal_viscosa

        # Calculando as forças tangenciais --------------------------
        # fta = 0
        if self.iteracao_atual-1 in self.existencia:
            fta = self.forca_tangencial_anterior
        else:
            fta = 0

        forca_tangencial_elastica = fta - kn_equivalente * vel_relativa_tangencial * delta_t
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

        # self.forca_normal['x'] = fnx
        # self.forca_normal['y'] = fny
        # self.forca_normal['modulo'] = forca_normal_modulo
        #
        # self.forca_tangencial['x'] = ftx
        # self.forca_tangencial['y'] = fty
        # self.forca_tangencial['modulo'] = forca_tangencial_modulo
        #
        # self.forca_total['x'] = -(fnx + ftx)
        # self.forca_total['y'] = -(fny + fty)

        # self.forca_total['modulo'] = math.sqrt(self.forca_total['x']**2 + self.forca_total['y']**2)
        self.forca_tangencial_anterior = forca_tangencial_modulo

        # Atribui as forças às partículas ============================================
        # p1 = self.particula1
        # p2 = self.particula2
        if 1:
            p1.forca_normal['x'] += fnx
            p1.forca_normal['y'] += fny
            p1.forca_normal['modulo'] += forca_normal_modulo
            p1.forca_tangencial['x'] += ftx
            p1.forca_tangencial['y'] += fty
            p1.forca_tangencial['modulo'] += forca_tangencial_modulo
            p1.forca_total['x'] += -(fnx + ftx)
            p1.forca_total['y'] += -(fny + fty)
            # p1.forca_total['modulo'] += self.forca_total['modulo']
            p1.torque += -forca_tangencial_modulo * p1.raio

            # Particula 2 -------------------------------------
            p2.forca_normal['x'] += -fnx
            p2.forca_normal['y'] += -fny
            p2.forca_normal['modulo'] += forca_normal_modulo
            p2.forca_tangencial['x'] += -ftx
            p2.forca_tangencial['y'] += -fty
            p2.forca_tangencial['modulo'] += forca_tangencial_modulo
            p2.forca_total['x'] += (fnx + ftx)  # -self.forca_total['x']
            p2.forca_total['y'] += (fny + fty)  # -self.forca_total['y']
            # p2.forca_total['modulo'] += self.forca_total['modulo']
            p2.torque += -forca_tangencial_modulo * p2.raio


    
    # def atribui_forcas(self):
    #
    #     # p1_id = c.particula1.id
    #     # p2_id = c.particula2.id
    #     p1 = self.particula1
    #     p2 = self.particula2
    #
    #     p1.forca_normal['x'] += self.forca_normal['x']
    #     p1.forca_normal['y'] += self.forca_normal['y']
    #     p1.forca_normal['modulo'] += self.forca_normal['modulo']
    #     p1.forca_tangencial['x'] += self.forca_tangencial['x']
    #     p1.forca_tangencial['y'] += self.forca_tangencial['y']
    #     p1.forca_tangencial['modulo'] += self.forca_tangencial['modulo']
    #     p1.forca_total['x'] += self.forca_total['x']
    #     p1.forca_total['y'] += self.forca_total['y']
    #     # p1.forca_total['modulo'] += self.forca_total['modulo']
    #     p1.torque += -self.forca_tangencial['modulo'] * p1.raio
    #
    #     # Particula 2 -------------------------------------
    #     p2.forca_normal['x'] += -self.forca_normal['x']
    #     p2.forca_normal['y'] += -self.forca_normal['y']
    #     p2.forca_normal['modulo'] += self.forca_normal['modulo']
    #
    #     p2.forca_total['x'] += -self.forca_total['x']
    #     p2.forca_total['y'] += -self.forca_total['y']
    #     # p2.forca_total['modulo'] += self.forca_total['modulo']
    #
    #     p2.forca_tangencial['x'] += -self.forca_tangencial['x']
    #     p2.forca_tangencial['y'] += -self.forca_tangencial['y']
    #     p2.forca_tangencial['modulo'] += self.forca_tangencial['modulo']
    #     p2.torque += -self.forca_tangencial['modulo'] * p2.raio

    def calcula_valor_equivalente(self, valor1, valor2):

        modelo = 1
        novovalor = None
        # Modelo de molas em série
        if modelo == 1:
            novovalor = (valor1 + valor2) / 2
        elif modelo == 2:
            novovalor = 1 / (1 / valor1 + 1 / valor2)

        return novovalor


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

        p = Particula()
        objeto = ObjetoLinha()

        p = self.particula
        objeto = self.objeto

        delta_t = self.passo_de_tempo
        v1x = p.velocidade_predita['x']
        v1y = p.velocidade_predita['y']
        v1angular = p.velocidade_predita['angular']
        raio1 = p.raio
        kn1 = p.material.kn
        gn1 = p.material.gn

        v2x = objeto.velocidadevetor[0]
        v2y = objeto.velocidadevetor[1]
        kn2 = objeto.material.kn
        gn2 = objeto.material.gn
        calcula_valor_equivalente = self.calcula_valor_equivalente
        ponto_contato = self.ponto_contato
        particula_posicao_predita_x = self.particula.posicao_predita['x']
        particula_posicao_predita_y = self.particula.posicao_predita['y']
        distancia_centros = self.distancia_centros
        distancia_contato = self.distancia

        # Calculando variáveis intermediárias
        if kn1 == kn2:
            kn_equivalente = kn1
        else:
            kn_equivalente = calcula_valor_equivalente(kn1, kn2)
        if gn1 == gn2:
            gn_equivalente = gn1
        else:
            gn_equivalente = calcula_valor_equivalente(gn1, gn2)

        # Determinando o ponto de contato

        # self.ponto_contato, self.distancia = calcula_contato_objeto(self.particula, self.objeto)

        delta_x = ponto_contato[0] - particula_posicao_predita_x
        delta_y = ponto_contato[1] - particula_posicao_predita_y

        cosseno = delta_x / distancia_centros
        seno = delta_y / distancia_centros

        # Daqui pra baixo é igual à classe de contato partícula-partícula

        vel_relativa_normal = cosseno * (v2x - v1x) + seno * (v2y - v1y)  # vijn
        vel_relativa_tangencial = (-seno * (v2x - v1x) + cosseno * (v2y - v1y)) - v1angular * raio1  # vijt

        # Calculando as forças normais -------------------------------
        forca_normal_elastica = - kn_equivalente * distancia_contato
        forca_normal_viscosa = - gn_equivalente * vel_relativa_normal
        forca_normal_modulo = forca_normal_elastica + forca_normal_viscosa

        # Calculando as forças tangenciais --------------------------
        # fta = 0
        if self.iteracao_atual-1 in self.existencia:
            fta = self.forca_tangencial_anterior  # Força tangencial anterior
        else:
            fta = 0

        forca_tangencial_elastica = fta - kn_equivalente * vel_relativa_tangencial * delta_t
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
        #
        # self.forca_normal['x'] = fnx
        # self.forca_normal['y'] = fny
        # self.forca_normal['modulo'] = forca_normal_modulo
        #
        # self.forca_tangencial['x'] = ftx
        # self.forca_tangencial['y'] = fty
        # self.forca_tangencial['modulo'] = forca_tangencial_modulo
        #
        # # self.forca_total['x'] = forca_normal_modulo * cosseno + forca_tangencial_modulo * (-seno)
        # # self.forca_total['y'] = forca_normal_modulo * seno + forca_tangencial_modulo * cosseno
        # self.forca_total['x'] = -(fnx + ftx)
        # self.forca_total['y'] = -(fny + fty)
        #
        # # self.forca_total['modulo'] = math.sqrt(self.forca_total['x'] ** 2 + self.forca_total['y'] ** 2)

        self.forca_tangencial_anterior = forca_tangencial_modulo

        # Atribui forças =================================================================================

        p = self.particula
        p.forca_normal['x'] += fnx
        p.forca_normal['y'] += fny
        p.forca_normal['modulo'] += forca_normal_modulo
        p.forca_tangencial['x'] += ftx
        p.forca_tangencial['y'] += fty
        p.forca_tangencial['modulo'] += forca_tangencial_modulo
        p.forca_total['x'] += -(fnx + ftx)
        p.forca_total['y'] += -(fny + fty)
        # p.forca_total['modulo'] += self.forca_total['modulo']
        p.torque += -forca_tangencial_modulo * p.raio

    # def atribui_forcas(self):
    #     p = self.particula
    #
    #     p.forca_normal['x'] += self.forca_normal['x']
    #     p.forca_normal['y'] += self.forca_normal['y']
    #     p.forca_normal['modulo'] += self.forca_normal['modulo']
    #     p.forca_tangencial['x'] += self.forca_tangencial['x']
    #     p.forca_tangencial['y'] += self.forca_tangencial['y']
    #     p.forca_tangencial['modulo'] += self.forca_tangencial['modulo']
    #     p.forca_total['x'] += self.forca_total['x']
    #     p.forca_total['y'] += self.forca_total['y']
    #     p.forca_total['modulo'] += self.forca_total['modulo']
    #     p.torque += -self.forca_tangencial['modulo'] * p.raio


    def calcula_valor_equivalente(self, valor1, valor2):

        modelo = 1
        novovalor = None
        # Modelo de molas em série
        if modelo == 1:
            novovalor = (valor1 + valor2) / 2
        elif modelo == 2:
            novovalor = 1 / (1 / valor1 + 1 / valor2)

        return novovalor


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
