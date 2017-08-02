# -*- coding: utf-8 -*-
__author__ = 'abraao'


nome_projeto = 'shanghai'

# pasta_destino = 'D:/SIMULACOES_DMCONVEYOR'
pasta_destino = '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR'

# Copia este arquivo para a nova pasta

dest = pasta_destino + '/' + nome_projeto

from shutil import copyfile

# copyfile()
import inspect, os
nomedestearquivo = str(__file__).split('/')[-1]
endereco_atual = __file__
endereco_destino = pasta_destino + '/' + nome_projeto + '/' + nomedestearquivo
if not os.path.exists(dest):
    os.makedirs(dest)

copyfile(endereco_atual, endereco_destino)
