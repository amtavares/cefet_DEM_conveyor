# -*- coding: utf-8 -*-
import random
import math
import numpy as np
from particula import Particula
from material import Material
# from geradoraleatorio import GeradorAleatorio
# from utilidades import mostrar_sistema
from objetos import ObjetoLinha
from inlet import Inlet

__author__ = 'abraao'


class Prepare:
    def __init__(self):
        # self.semente_gerador_aleatorio

        # Não precisa destas propriedades, é so pegar o len(lista)
        # self.total_particulas = 0
        # self.total_particulas_livres = 0
        # self.total_particulas_fixos = 0

        self.lista_particulas = {}
        self.lista_particulas_fixas = []
        self.lista_particulas_livres = []
        self.lista_objetos = {}
        self.inlet = None

        self.distribuicao_raios = ''

        self.raio_minimo = 0
        self.raio_maximo = 0

        self.limites = {'xmin': None, 'xmax': None, 'ymin': None, 'ymax': None}

        # self.aleat = GeradorAleatorio()

        self.ultimo_id_usado = -1

        self.passo_de_tempo = None
        self.gn_maximo = None

        self.configuracao = None

    def preparar_transportador(self, config):
        '''
        inclinacao_correia
        comprimento_livre_correia
        largura_caixa_entrada
        inclinacao_caixa_entrada
        raio_particulas_correia
        raio_particulas_paredes
        abertura_parede
        :return:  
        '''

        inclinacao_correia = config['inclinacao_correia']
        comprimento_livre_correia = config['comprimento_livre_correia']
        velocidade_correia = config['velocidade_correia']
        raio_particulas_correia = config['raio_particulas_correia']
        material_correia = config['material_correia']
        altura_material_correia = config['altura_material_correia']
        tempo_total_simulacao = config['tempo_total_simulacao']
        # Propriedades d]paredes
        altura_caixa_entrada = config['altura_caixa_entrada']
        largura_caixa_entrada = config['largura_caixa_entrada']
        inclinacao_caixa_entrada = config['inclinacao_caixa_entrada']
        raio_particulas_paredes = config['raio_particulas_paredes']
        abertura_caixa_entrada = config['abertura_caixa_entrada']
        material_paredes = config['material_paredes']
        # Propriedades das partícullivres
        raio_max_particulas_livres = config['raio_max_particulas_livres']
        raio_min_particulas_livres = config['raio_min_particulas_livres']
        distribuicao_raios_livres = config['distribuicao_raios_livres']
        # quantidade_particulas_livres = config['quantidade_particulas_livres']
        material_particulas_livres = config['material_particulas_livres']
        # Propriedades d]o sistema
        # limites_xmin = config['limites_xmin']
        # limites_xmax = config['limites_xmax']
        # limites_ymin = config['limites_ymin']
        # limites_ymax = config['limites_ymax']
        self.limites = {'xmin': config['limites_xmin'], 'xmax': config['limites_xmax'], 'ymin': config['limites_ymin'],
                        'ymax': config['limites_ymax']}

        # Calculando variáveis intermediárias: =========================================================================
        # Correia
        angulo_real_correia = (180 + inclinacao_correia) * math.pi / 180
        comprimento_total_correia = largura_caixa_entrada / math.fabs(
            math.cos(angulo_real_correia)) + comprimento_livre_correia

        x1_correia = comprimento_total_correia * math.cos(angulo_real_correia)
        y1_correia = comprimento_total_correia * math.sin(angulo_real_correia)
        x2_correia = 0
        y2_correia = 0

        # Parede esquerda
        x1_parede_esq = x1_correia
        y1_parede_esq = y1_correia # + raio_particulas_correia + raio_particulas_paredes
        x2_parede_esq = x1_parede_esq
        y2_parede_esq = y1_parede_esq + altura_caixa_entrada

        # Parede direita
        x1_parede_dir = x1_correia + largura_caixa_entrada
        y1_parede_dir = (comprimento_livre_correia * math.sin(
            angulo_real_correia)) + raio_particulas_correia + abertura_caixa_entrada + raio_particulas_paredes
        x2_parede_dir = x1_parede_dir
        y2_parede_dir = y2_parede_esq

        # Tunel
        x1_tunel = x1_parede_dir
        y1_tunel = y1_parede_dir
        x2_tunel = x1_tunel + 0.5
        y2_tunel = y1_tunel

        # Inlet - Partículas livres
        x1_inlet = x1_parede_esq + raio_particulas_paredes + raio_max_particulas_livres * 1.1
        y1_inlet = 1.5
        x2_inlet = x1_parede_dir - raio_max_particulas_livres * 1.1
        y2_inlet = y1_inlet

        # Partículas livres ------------------------------------------------------------------------------
        self.inlet = Inlet()
        self.inlet.x1 = x1_inlet
        self.inlet.y1 = y1_inlet
        self.inlet.x2 = x2_inlet
        self.inlet.y2 = y2_inlet

        self.inlet.velocidade_correia = velocidade_correia
        self.inlet.altura_material = altura_material_correia
        self.inlet.tempo_total_simulacao = tempo_total_simulacao

        self.inlet.raio_minimo = raio_min_particulas_livres
        self.inlet.raio_maximo = raio_max_particulas_livres

        self.inlet.inicializa()

        # Definir os raios das particulas livres
        lista_raios = self.raios(self.inlet.quantidade_particulas, raio_min_particulas_livres,
                                 raio_max_particulas_livres)
        lista_posicoes = self.posicoes(lista_raios, x1_inlet, y1_inlet, x2_inlet, y2_inlet)

        for i in range(0, self.inlet.quantidade_particulas):
            nova_particula = Particula()
            nova_particula.id = self.nova_id()
            nova_particula.raio = lista_raios[i]
            nova_particula.material = material_particulas_livres
            nova_particula.posicao['x'] = lista_posicoes[i]['x']
            nova_particula.posicao['y'] = lista_posicoes[i]['y']
            nova_particula.posicao['angular'] = 0
            nova_particula.livre = True
            nova_particula.update_propriedades_fisicas()

            # Colocar no inlet
            self.inlet.lista_particulas[nova_particula.id] = nova_particula

        self.inlet.calcula_vazoes()

        # Definindo a correia ------------------------------------------------------------------------------------------
        correia = ObjetoLinha()
        correia.ponto_inicial = np.array([x1_correia,y1_correia])
        correia.ponto_final = np.array([x2_correia,y2_correia])
        correia.id = self.nova_id()
        correia.velocidade = velocidade_correia
        correia.material = material_correia
        correia.label = "Correia"
        correia.update()
        self.lista_objetos[correia.id] = correia

        # Parede esquerda
        parede_esquerda = ObjetoLinha()
        parede_esquerda.ponto_inicial = np.array([x1_parede_esq, y1_parede_esq])
        parede_esquerda.ponto_final = np.array([x2_parede_esq, y2_parede_esq])
        parede_esquerda.id = self.nova_id()
        parede_esquerda.velocidade = 0
        parede_esquerda.material = material_paredes
        parede_esquerda.label = "Parede esquerda"

        parede_esquerda.update()
        self.lista_objetos[parede_esquerda.id] = parede_esquerda

        # Parede direita
        parede_direita = ObjetoLinha()
        parede_direita.ponto_inicial = np.array([x1_parede_dir, y1_parede_dir])
        parede_direita.ponto_final =   np.array([x2_parede_dir, y2_parede_dir])
        parede_direita.id = self.nova_id()
        parede_direita.velocidade = 0
        parede_direita.material = material_paredes
        parede_direita.label = "Parede direita"
        parede_direita.update()
        self.lista_objetos[parede_direita.id] = parede_direita

        # Tunel
        tunel = ObjetoLinha()
        tunel.ponto_inicial = np.array([x1_tunel, y1_tunel])
        tunel.ponto_final =   np.array([x2_tunel, y2_tunel])
        tunel.id = self.nova_id()
        tunel.velocidade = 0
        tunel.material = material_paredes
        tunel.label = "Tunel"
        tunel.update()
        self.lista_objetos[tunel.id] = tunel

        # gn, kn, passo de tempo ---------------------------------------------------------------------------------------

        maior_kn = 0
        maior_massa = 0

        for p in self.inlet.lista_particulas.values():
            if p.material.kn > maior_kn:
                maior_kn = p.material.kn
            if p.massa > maior_massa:
                maior_massa = p.massa

        # self.gn_maximo = (2 * math.sqrt(maior_kn / maior_massa)) *10
        # self.passo_de_tempo = (1 / math.sqrt(maior_kn * maior_massa)) / 50
        self.gn_maximo = (2 * math.sqrt(maior_massa * maior_kn))
        self.passo_de_tempo = (1 * math.sqrt(maior_massa / maior_kn)) / 50
        print('Passo de tempo = {} '.format(self.passo_de_tempo))
        print('Gn crítico = {} s'.format(self.gn_maximo))
        print('1000 iteraçoes = {} s'.format(self.passo_de_tempo * 1000))
        print('Para 50 FPS usar: {}'.format((1/50)/self.passo_de_tempo))

        # Inicialização de velocidades e acelerações -------------------------------------------------------------------

        p = Particula()
        for p in self.inlet.lista_particulas.values():
            if p.aceleracao['x'] is None:       p.aceleracao['x'] = 0
            if p.aceleracao['y'] is None:       p.aceleracao['y'] = 0
            if p.aceleracao['angular'] is None: p.aceleracao['angular'] = 0
            if p.velocidade['x'] is None:       p.velocidade['x'] = 0
            if p.velocidade['y'] is None:       p.velocidade['y'] = 0
            if p.velocidade['angular'] is None: p.velocidade['angular'] = 0
            # if p.gravidade['x'] is None: p.gravidade['x'] = 0
            # if p.gravidade['y'] is None: p.gravidade['y'] = 0
            # Todo Não precisa de inicializar as forcas aqui
            # p.forca_total['x'] = 0
            # p.forca_total['y'] = 0
            # p.forca_total['modulo'] = 0
            p.set_passo_de_tempo(self.passo_de_tempo)
            p.material.gn = self.gn_maximo

        for o in self.lista_objetos.values():
            o.material.gn = self.gn_maximo

        # Configuração a ser passada para a Dinamica molecular ---------------------------------------------------------

        from config import Config
        self.configuracao = Config()
        self.configuracao.calculo_gn_contatos = 1
        self.configuracao.calculo_kn_contatos = 1
        self.configuracao.passo_de_tempo = self.passo_de_tempo

        # Exibir resumo ------------------------------------------------------------------------------------------------

        if 1:
            print('____ Resumo do Prepare _____')
            print('     Total de partículas {}'.format(len(self.lista_particulas)))
            print('     Total de particulas livres {}'.format(len(self.lista_particulas_livres)))
            print('     Total de partículas fixas {}'.format(len(self.lista_particulas_fixas)))
            print('     Raio máximo livre {}'.format(self.raio_maximo))
            print('     Raio mínimo live {}'.format(self.raio_minimo))
            print('     Passo de tempo %.2e' % self.passo_de_tempo)
            # print('     Seed {}'.format(random.get))

    def raios(self, numero_particulas_livres, raio_min, raio_max):
        # retorna uma lista de raios de tamanho tamanho_lista e com valores entre raio_min e raio_max

        raios_das_particulas = list(np.linspace(raio_min, raio_max, numero_particulas_livres))
        random.shuffle(raios_das_particulas)

        self.raio_maximo = max(raios_das_particulas)
        self.raio_minimo = min(raios_das_particulas)

        return raios_das_particulas

    def posicoes(self, raios, xmin, ymin, xmax, ymax):

        # Determinar o maior diametro
        diamentromaximo = 2 * max(raios)

        # Determinar um espaçamento entre partículas a partir do maior diâmetro, usando 1%
        espacamento = 0.001
        distancia_entre_centros = diamentromaximo * (1 + espacamento)

        # Cria a lista de posicoes
        n = 1
        linha = 0
        coluna = 0
        lista_posicoes = []
        while n <= len(raios):

            px = xmin + coluna * distancia_entre_centros

            if px > xmax:
                linha += 1
                coluna = 0

            x = xmin + coluna * distancia_entre_centros
            y = ymin + linha * distancia_entre_centros

            lista_posicoes.append({'x': x, 'y': y})

            coluna += 1

            n += 1

        return lista_posicoes

    def gerar_posicoes_parede(self, x_ini, y_ini, x_final, y_final, raio):

        comprimento = math.sqrt((x_final - x_ini) ** 2 + (y_final - y_ini) ** 2)
        quantidade_particulas = math.ceil(comprimento / (2 * raio))

        cosseno = (x_final - x_ini) / comprimento
        seno = (y_final - y_ini) / comprimento

        deltax = 2 * raio * cosseno
        deltay = 2 * raio * seno

        lista_posicoes = []
        for i in range(0, quantidade_particulas):
            x = x_ini + i * deltax
            y = y_ini + i * deltay

            lista_posicoes.append({'x': x, 'y': y})

        return lista_posicoes

    def nova_id(self):
        if self.ultimo_id_usado < 0:
            novoid = 0
        else:
            novoid = self.ultimo_id_usado + 1

        self.ultimo_id_usado = novoid
        return novoid
