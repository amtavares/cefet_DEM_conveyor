# -*- coding: utf-8 -*-
__author__ = 'abraao'
import random
import math
from particula import Particula
from material import Material
from geradoraleatorio import GeradorAleatorio
from utilidades import mostrar_sistema

class Correia:

    def __init__(self):
        self.velocidade = {'x':None,'y':None,'angular':None}
        self.lista_particulas = []
        self.limites

    def update_correia(self):
        # Condições periodicas de contorno

        pass
