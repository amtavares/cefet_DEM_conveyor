# -*- coding: utf-8 -*-
__author__ = 'abraao'

import math


lista = ['aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk','ll','mm','nn','oo','pp']

n = 3
c = int(len(lista)/n)

print(c)

sublistas = []
for s in range(0, len(lista),c):
    sublistas.append(lista[s:s+c])

print(sublistas)

print('==================================')

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
            'quantidade_contatos': list()
        }

class Propriedades:

    def __init__(self):
        self.valores = {
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
                'quantidade_contatos': list()
        }
    
prop = Propriedades()
prop.massa = 38



dicio = dict()
dicio['banana'] = Propriedades()
dicio['choco'] = Propriedades()

dicio['banana'].valores['massa'].append(45)
dicio['choco'].valores['massa'].append(37)

for superkey in dicio.keys():
    print('\n' + superkey)
    print('------------')
    for key in dicio[superkey].valores.keys():
        print(key + ' : ' + str(dicio[superkey].valores[key]))