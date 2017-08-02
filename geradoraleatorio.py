# -*- coding: utf-8 -*-
__author__ = 'abraao'

import random


class GeradorAleatorio:

    def __init__(self):
        self.semente = random.seed

    def rand(self):
        """

        :rtype: float
        """
        return random.random()

    def gaussiana(self):
        return random.gauss(0.5, 0.01)

    def set_semente(self, semente):
        random.seed(semente)
        self.semente = semente
'''
    def rand0(self):
        # TODO Testar esta função contra a do C++
        # Números "mágicos" do gerador aleatório
        A = 843314861
        B = 453816693
        C = 1073741824

        aux = float(0.5)

        s = self.semente

        s = s * A + B

        if s < 0:
            s = (s + M) + M

        self.semente = s

        return s * aux

    def distribuicao_gaussiana(self):
        soma = 0
        for i in range(1, 1000):
            aux = (soma - 500) / 83.25
            aux = (aux + 0.4084) / 0.8585
'''