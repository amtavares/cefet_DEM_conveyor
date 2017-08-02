# -*- coding: utf-8 -*-

import math
import numpy as np
import time
import random
from particula import Particula

__author__ = 'abraao'


class Inlet:
    def __init__(self):

        # Parâmetros que precisam ser definidos externamente
        self.lotes = []
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.inlet_vetor = None

        self.tempo_total_simulacao = None
        self.altura_material = None
        self.velocidade_correia = None

        self.raio_maximo = None
        self.raio_minimo = None

        self.lista_particulas = {}
        self.quantidade_particulas = None

        self.passo_de_tempo = None

        # Parâmetros definidos internamente
        self.vazao_total_segundo = None  # Em partículas por segundo
        self.velocidade_saida = {'x': None, 'y': None}
        self.quantidade = None
        self.periodo = None

        # self.lista_raios = None

        self.tempo_ultimo_lote = 0

        self.numero_lote_atual = 0

        self.lista_ids = list()

    def inicializa(self):
        ponto1 = np.array([self.x1, self.y1])
        ponto2 = np.array([self.x2, self.y2])
        self.inlet_vetor = ponto2 - ponto1

        raio_medio = (self.raio_maximo + self.raio_minimo) / 2

        # Calculando a vazão de partículas por segundo
        # self.altura_material = 5
        self.vazao_total_segundo = self.altura_material * self.velocidade_correia / (2 * raio_medio)

        # Número total de partículas da simulação
        self.quantidade_particulas = int(self.tempo_total_simulacao * self.vazao_total_segundo)

    def calcula_vazoes(self):
        print('Determinando vazoes do inlet')
        # Numero máximo de particulas simultaneas no inlet
        comprimento = np.linalg.norm(self.inlet_vetor)
        nmax = math.floor(comprimento / (1.01 * 2 * self.raio_maximo))

        # Quantos lotes por segundo serão criados
        tamanho_lote = nmax
        frequencia_lotes = self.vazao_total_segundo / tamanho_lote
        lotes_inteiros = math.floor(frequencia_lotes)
        lotes_fracionados = frequencia_lotes - lotes_inteiros

        # Cria a lista com os tamanhos dos lotes a serem liberados a cada segundo
        for i in range(lotes_inteiros):
            self.lotes.append(tamanho_lote)
        if lotes_fracionados > 0:
            self.lotes.append(int(lotes_fracionados * tamanho_lote))

        # Intervalo entre os lotes
        self.periodo = 1 / len(self.lotes)

        # Velocidade com que as partículas tem de sair para evitar colisão entre lotes
        velocidade = (2 * self.raio_maximo * len(self.lotes)) * 1.05

        # Calculando o vetor perpendicular ao inlet
        perp = np.empty_like(self.inlet_vetor)
        perp[0] = self.inlet_vetor[1]
        perp[1] = -self.inlet_vetor[0]

        perp_norm = perp / np.linalg.norm(perp)

        self.velocidade_saida['x'] = velocidade * perp_norm[0]
        self.velocidade_saida['y'] = velocidade * perp_norm[1]

        self.lista_ids = list(self.lista_particulas.keys())

    def run_inlet(self, tempo):
        dt = tempo - self.tempo_ultimo_lote
        # print('dt: ' + str(dt))
        if dt > 0.25:
            pass

        if dt >= self.periodo:
            # print('liberando  um lote particulas')
            lista_particulas_liberadas = {}

            # Este loop monta um lote de partículas a ser
            quantidade = self.lotes[self.numero_lote_atual]
            for i in range(quantidade):
                # Pega uma partícula da lista
                proxima_particula_id = self.lista_ids[0]
                p = self.lista_particulas[proxima_particula_id]
                p.velocidade['x'] = self.velocidade_saida['x']
                p.velocidade['y'] = self.velocidade_saida['y']
                # p.velocidade['angular'] = 0
                # p.aceleracao['x'] = 0
                # p.aceleracao['y'] = 0
                # p.aceleracao['angular'] = 0
                posx = self.x1 + (self.inlet_vetor[0] / self.lotes[self.numero_lote_atual]) * i
                posy = self.y1 + (self.inlet_vetor[1] / self.lotes[self.numero_lote_atual]) * i
                p.posicao['x'] = posx
                p.posicao['y'] = posy
                # Adiciona na lista de particulas liberadas
                lista_particulas_liberadas[proxima_particula_id] = p
                # Apaga da lista de buffer
                self.lista_ids.remove(proxima_particula_id)
                del self.lista_particulas[proxima_particula_id]

            self.tempo_ultimo_lote = tempo

            if self.numero_lote_atual < len(self.lotes) - 1:
                self.numero_lote_atual += 1
            else:
                self.numero_lote_atual = 0

            return lista_particulas_liberadas

        else:
            return False
