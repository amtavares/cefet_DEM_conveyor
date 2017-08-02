# -*- coding: utf-8 -*-
__author__ = 'abraao'
import numpy as np

class ObjetoLinha:

    def __init__(self):
        self.id = None
        self.ponto_inicial = None
        self.ponto_final = None
        self.vetor = None
        self.vetorunitario = None
        self.comprimento = None
        self.velocidade = None
        self.velocidadevetor = None
        self.tipo = None
        self.label = None

        self.material = None

        self.lista_vizinhos = set()
        self.lista_contatos = set()

    def update(self):
        self.vetor = self.ponto_final - self.ponto_inicial
        self.comprimento = np.linalg.norm(self.vetor)
        self.vetorunitario = self.vetor / self.comprimento
        self.velocidadevetor = self.velocidade * self.vetorunitario


class ObjetoCirculo:

    def __init__(self):
        self.centro = None