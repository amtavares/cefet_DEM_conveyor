# -*- coding: utf-8 -*-
__author__ = 'abraao'

import pickle
import os

class SalvarHistorico:

    def __init__(self):
        self.numero_arquivo = 0
        # self.pasta_destino = 'save'
        self.pasta_destino = 'D:/SIMULACOES_DMCONVEYOR'
        self.nome_projeto = 'simulacao'

    def salvar(self, sistema):
        pasta = self.pasta_destino + '/' +self.nome_projeto

        if not os.path.exists(pasta):
            os.makedirs(pasta)

        nome_arquivo = pasta + '/' + self.nome_projeto + '_' + str(self.numero_arquivo)
        pickle.dump(sistema, open(nome_arquivo, 'wb'))
        self.numero_arquivo += 1
