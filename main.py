# -*- coding: utf-8 -*-
__author__ = 'abraao'

# -*- coding: utf-8 -*-
__author__ = 'abraao'

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dinamicamolecular2 import DinamicaMolecular
from prepare import Prepare
from salvarhistorico import SalvarHistorico
import visualizador as viz
from material import Material

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


# Propriedades da correia
material1 = Material()
material1.kn = 100000
material1.kt = 100000
material1.gn = 100
material1.densidade = 0.1
material1.nome = "Material 1"
material1.cor = 'green'

config = {
    'inclinacao_correia': 0,
    'comprimento_livre_correia': 2,
    'velocidade_correia': 3,
    'raio_particulas_correia': 0.01,
    'material_correia': material1,
    # Propriedades das paredes
    'altura_caixa_entrada': 3,
    'largura_caixa_entrada': 1.5,
    'inclinacao_caixa_entrada': 0,  # Parametro atualmente obsoleto
    'raio_particulas_paredes': 0.01,
    'abertura_caixa_entrada': 0.5,
    'material_paredes': material1,
    # Propriedades das partículas livres
    'raio_max_particulas_livres': 0.05,
    'raio_min_particulas_livres': 0.05,
    'distribuicao_raios_livres': 'normal',  # Parametro atualmente obsoleto
    'quantidade_particulas_livres': 400,
    'material_particulas_livres': material1,
    # Propriedades do sistema
    'limites_xmin': -5,
    'limites_xmax': 3,
    'limites_ymin': -2,
    'limites_ymax': 2,
    }

exibir = {'particulas_livres': True,
          'velocidades': False,
          'labels_particulas_livres': False,
          'labels_particulas_fixas': False,
          'forcas_particulas_livres': False,
          'contatos': True,
          'paredes': True,
          'correia': True,
          'limites': True,
          }

# Criando o transportador
prep = Prepare()
prep.preparar_transportador(config)


# figura = plt.figure()
# viz.mostrar_sistema(prep, plt.figure())

dm = DinamicaMolecular()
dm.set_configuracao(prep)

sh = SalvarHistorico()
sh.nome_projeto = 'simulacao'
sh.pasta_destino = 'save'
dm.salvar_historico = sh

dm.axis = ax1
dm.figure = fig
dm.run()
'''
'''
