"""
Implementa a classe que carrega as configurações do sistema
"""
# -*- coding: utf-8 -*-
__author__ = 'abraao'

class Config:

    def __init__(self):
        # Geral
        self.passo_de_tempo = None
        # Partículas
        # Contatos
        self.calculo_kn_contatos = None
        self.calculo_gn_contatos = None


    def set_calculo_kn_contatos(self, tipo):
        """
        Define o tipo de cálculo realizado para definir o kn de um contato entre duas partículas
        :param tipo: 1,2 ou 3
          1: kn = (k1 + k2) /2
          2: kn = k1 + k2
          3: kn = k1 * k2
        :return: nada
        """
        self.calculo_kn_contatos = tipo

    def set_calculo_gn_contatos(self, tipo):
        """
        Define o tipo de cálculo realizado para definir o gn de um contato entre duas partículas
        :param tipo: 1,2 ou 3
          1: gn = (g1 + g2) /2
          2: gn = g1 + g2
          3: gn = g1 * g2
        :return: nada
        """
        self.calculo_gn_contatos = tipo

