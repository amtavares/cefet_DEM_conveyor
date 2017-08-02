# -*- coding: utf-8 -*-
__author__ = 'abraao'

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dinamicamolecular import DinamicaMolecular
from prepare import Prepare
from salvarhistorico import SalvarHistorico
import utilidades as u

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

prep = Prepare()
prep.preparar()
# u.mostrar_sistema(prep)
dm = DinamicaMolecular()
dm.set_configuracao(prep)

sh = SalvarHistorico()
sh.nome_projeto = 'simulacao'
sh.pasta_destino = 'save'
dm.salvar_historico = sh

dm.axis = ax1
dm.figure = fig
dm.run()



