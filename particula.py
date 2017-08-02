# -*- coding: utf-8 -*-
__author__ = 'abraao'

from material import *
import math

class Particula():

    def __init__(self):

        # Propriedades Básicas
        self.id = -1
        self.raio = None
        self.cor = ''
        self.material = Material()
        self.livre = True
        self.grupo = None
        # Propriedades físicas
        self.area = None
        self.massa = None

        # Forças e contatos
        # self.forcas = {'x':None,'y':None,'tangencial':None}
        self.gravidade = {'x':0,'y':-9.81}
        self.forca_normal = {'x': None, 'y': None, 'modulo': None}
        self.forca_tangencial = {'x': None, 'y': None, 'modulo': None}
        self.forca_total = {'x': None, 'y': None, 'modulo': None}
        self.torque = None

        self.lista_contatos = set()
        self.lista_vizinhos = set() # guardar apenas as IDs das partículas
        self.lista_vizinhos_objetos = set()
        self.lista_contatos_objetos = set()

        self.aceleracao = {'x':None,'y':None,'angular':None}
        self.velocidade = {'x':None,'y':None,'angular':None}
        self.posicao =    {'x':None, 'y':None,'angular':None}

        self.aceleracao_predita = {'x': None, 'y': None, 'angular': None}
        self.velocidade_predita = {'x': None, 'y': None, 'angular': None}
        self.posicao_predita =    {'x': None, 'y': None, 'angular': None}

        # Propriedades da simulacao
        self.passo_de_tempo = None
        self.dt2s2 = None
        self.c1 = None

    def set_passo_de_tempo(self, passo):
        # Atualmente não é usada
        self.passo_de_tempo = passo
        self.dt2s2 = self.passo_de_tempo ** 2 / 2
        self.c1 = self.dt2s2 / self.passo_de_tempo

    def update_propriedades_fisicas(self):
        self.area = math.pi * self.raio**2
        self.massa = self.material.densidade * self.area * 1 # Discos de 10cm de espessura
        self.cor = self.material.cor

        # self.passo_de_tempo = passo
        # self.dt2s2 = self.passo_de_tempo ** 2 / 2
        # self.c1 = dt2s2 / self.passo_de_tempo

    def preditor(self):
        dt = self.passo_de_tempo
        dt2s2 = self.dt2s2

        # Acelerações -----------------------------------------------------------------------
        # Calcula
        aceleracao_x_predita       = self.aceleracao['x']
        aceleracao_y_predita       = self.aceleracao['y']
        aceleracao_angular_predita = self.aceleracao['angular']
        # Atualiza
        self.aceleracao_predita['x']       = aceleracao_x_predita
        self.aceleracao_predita['y']       = aceleracao_y_predita
        self.aceleracao_predita['angular'] = aceleracao_angular_predita

        # Velocidades -----------------------------------------------------------------------
        # Calcula
        vx_predita = self.velocidade['x'] + self.aceleracao['x'] * dt
        vy_predita = self.velocidade['y'] + self.aceleracao['y'] * dt
        vangular_predita = self.velocidade['angular'] + self.aceleracao['angular'] * dt
        # Atualiza
        self.velocidade_predita['x'] = vx_predita
        self.velocidade_predita['y'] = vy_predita
        self.velocidade_predita['angular'] = vangular_predita

        # Posições -----------------------------------------------------------------------
        # Calcula
        delta_x = self.velocidade['x'] * dt + self.aceleracao['x'] * dt2s2
        delta_y = self.velocidade['y'] * dt + self.aceleracao['y'] * dt2s2
        delta_angular = self.velocidade['angular'] * dt + self.aceleracao['angular'] * dt2s2
        posicao_x_predita = self.posicao['x'] + delta_x
        posicao_y_predita = self.posicao['y'] + delta_y
        posicao_angular_predita = self.posicao['angular'] + delta_angular

        # Atualiza
        self.posicao_predita['x'] = posicao_x_predita
        self.posicao_predita['y'] = posicao_y_predita
        self.posicao_predita['angular'] = posicao_angular_predita
        pass

    def corretor(self):

        # self.aceleracao['x'] = self.forca_normal['x']/self.massa
        # self.aceleracao['y'] = self.forca_normal['y']/self.massa

        self.aceleracao['x'] = self.forca_total['x'] / self.massa
        self.aceleracao['y'] = self.forca_total['y'] / self.massa
        self.aceleracao['angular'] = self.torque / self.massa

        self.velocidade['x'] = self.velocidade_predita['x'] + self.c1*(self.aceleracao['x'] - self.aceleracao_predita['x'])
        self.velocidade['y'] = self.velocidade_predita['y'] + self.c1*(self.aceleracao['y'] - self.aceleracao_predita['y'])
        self.velocidade['angular'] = self.velocidade_predita['angular'] + self.c1*(self.aceleracao['angular'] - self.aceleracao_predita['angular'])

        self.posicao['x'] = self.posicao_predita['x']
        self.posicao['y'] = self.posicao_predita['y']
        pass

    def mover(self):
        dt = self.passo_de_tempo

        self.posicao['x'] += self.velocidade['x'] * dt
        self.posicao['y'] += self.velocidade['y'] * dt
        self.posicao['angular'] += self.velocidade['angular'] * dt

        self.posicao_predita['x'] = self.posicao['x']
        self.posicao_predita['y'] = self.posicao['y']
        self.posicao_predita['angular'] = self.posicao['angular']

    def reseta_forcas(self):
        self.forca_normal['x'] = 0
        self.forca_normal['y'] = 0
        self.forca_normal['modulo'] = 0
        self.forca_tangencial['x'] = 0
        self.forca_tangencial['y'] = 0
        self.forca_tangencial['modulo'] = 0
        self.forca_total['x'] = 0
        self.forca_total['y'] = 0
        self.forca_total['modulo'] = 0
        self.torque = 0

        if self.livre:
            forca_gravidade = self.massa * self.gravidade['y']
            self.forca_total['y'] = forca_gravidade