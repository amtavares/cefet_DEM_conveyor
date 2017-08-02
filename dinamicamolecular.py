# -*- coding: utf-8 -*-
import pickle

__author__ = 'abraao'

import os
from prepare import Prepare
from utilidades import distancia_entre_particulas, str2ids, ids2str
from visualizador import mostrar_sistema
from contato import Contato
import time
from copy import deepcopy

os.environ.setdefault('TERM', 'xterm-color')


# from time import time


class DinamicaMolecular:
    """
    void recherche_Voisins1();
    void inicio();
    void preditor();
    void detectcontacts();
    void calculoforcas();
    void corretor();
    void verifequilibre();
    void profon();
    void affichage();
    void sauvconf();
    int archivagereaction();
    """

    def __init__(self):

        # Configurações
        self.periodo_salvar_estado = 10000
        self.periodo_procura_vizinhos = 10000
        self.periodo_mostrar_output = 1000
        self.configuracao = None
        self.figure = None
        self.axis = None

        self.gravidade = {'x': 0, 'y': -9.81}

        self.limite_iteracoes = -1
        self.limite_tempo_simulado = 10
        self.limite_tempo_real = -1
        self.limites = {'xmin': None, 'xmax': None, 'ymin': None, 'ymax': None}

        self.hora_inicio = None
        self.hora_fim = None

        # Dados gerais do sistema
        self.iteracao = 0
        self.tempo_real = 0
        self.tempo_simulado = 0
        self.lista_particulas = {}  # Dicionario: keys = ids das partículas,values= objetos Particulas
        self.lista_particulas_fixas = []  # list de inteiros com id das partículas
        self.lista_particulas_livres = []  # list de inteiros com id das partículas

        self.lista_contatos = {}
        self.lista_contatos_existentes = set()  # set com os ids dos contatos que existem por iteracao

        self.passo_de_tempo = None
        self.gn_maximo = None

        self.raio_maximo = None
        self.raio_minimo = None
        self.raio_medio = None

        self.salvar = True
        self.numero_arquivo = 0
        self.nome_simulacao = 'simulacao'
        self.salvar_historico = True

    def run(self):

        self.inicializa()
        tanterior = time.time()
        continuar = True
        while continuar:
            # it + +;

            if self.iteracao % self.periodo_procura_vizinhos == 0:
                self.procura_vizinhos()

            # preditor();
            self.preditor()
            # self.mover_paredes()
            # detectcontacts();
            self.detecta_contatos()
            # calculoforcas();
            self.reseta_forcas()
            self.calculo_forcas()
            # corretor();
            self.corretor()

            # Elimina particulas fora dos limites
            self.verificar_limites()

            self.tempo_simulado = self.iteracao * self.passo_de_tempo
            self.tempo_real = time.time() - self.hora_inicio

            continuar = not self.verifica_continuidade()

            # Output
            if self.iteracao % self.periodo_mostrar_output == 0:
                tagora = time.time()
                print(tagora - tanterior)
                tanterior = tagora
                self.mostrar_output()

            # if len(self.lista_contatos_existentes) > 0:
            #     self.periodo_mostrar_output = 100

            if self.iteracao % self.periodo_salvar_estado == 0:
                if self.salvar_historico:
                    self.salvar_historico.salvar(self)

            self.iteracao += 1

    def inicializa(self):
        # Amortecimento
        # printf(" gn ? < %f \n ", 2.0 * sqrt(kn / zmass));
        # scanf("%f", & gn);

        # Determinação do passo de tempo
        # dt = 1 / sqrt(kn * zmass) / 50; / * ! xx / 50 -> arbitraire! * /
        # printf("dt = %f \n", dt);

        localtime = time.asctime(time.localtime(time.time()))
        print("Simulação iniciada em :", localtime)
        self.hora_inicio = time.time()

        # TODO Incorporar a verificação do gn na classe Prepare

        # Coeficiente preditor-corretor
        dt2s2 = self.passo_de_tempo ** 2 / 2
        c1 = dt2s2 / self.passo_de_tempo

        for particula_id in self.lista_particulas_livres:
            p = self.lista_particulas[particula_id]
            p.passo_de_tempo = self.passo_de_tempo
            p.dt2s2 = dt2s2
            p.c1 = c1
            p.gravidade = self.gravidade.copy()
            p.material.gn = self.gn_maximo

        for particula_id in self.lista_particulas_fixas:
            p = self.lista_particulas[particula_id]
            p.posicao_predita = p.posicao.copy()
            p.velocidade_predita = p.velocidade.copy()
            p.aceleracao_predita = p.aceleracao.copy()
            p.material.gn = self.gn_maximo

    def procura_vizinhos(self):

        tamanho_celula_vizinhanca = 1.5 * self.raio_maximo

        # limpar a lista de vizinhos antes de fazer a nova
        for key, val in self.lista_particulas.items():
            self.lista_particulas[key].lista_vizinhos.clear()

        # TODO tentar usar list comprehension: https://gist.github.com/bearfrieze/a746c6f12d8bada03589
        lista_ids = list(self.lista_particulas.keys())

        for i, particula_id_1 in enumerate(lista_ids):
            for particula_id_2 in lista_ids[i + 1:]:

                p1 = self.lista_particulas[particula_id_1]
                p2 = self.lista_particulas[particula_id_2]
                distancia_centros, distancia_contato = distancia_entre_particulas(p1, p2)

                if p1.raio + distancia_contato < tamanho_celula_vizinhanca:
                    # Coloca p2 na lista de vizinhos de p1
                    self.lista_particulas[particula_id_1].lista_vizinhos.append(particula_id_2)
                    # Coloca p1 na lista de vizinhos de p2
                    self.lista_particulas[particula_id_2].lista_vizinhos.append(particula_id_1)

    def preditor(self):
        for particula_id in self.lista_particulas_livres:
            self.lista_particulas[particula_id].preditor()

    def mover_paredes(self):
        for particula_id in self.lista_particulas_fixas:
            self.lista_particulas[particula_id].mover()

    def detecta_contatos(self):

        contatos_ja_verificados = set()  # Lista os contatos já verificados nesta iteração atual
        pass
        # Procura os contatos das partículas livres dentro da lista de vizinhos de cada uma
        # Loop pelas partículas livres
        for particula_id in self.lista_particulas_livres:
            p1 = self.lista_particulas[particula_id]
            # Loop pela lista de visinhos
            for viz_id in p1.lista_vizinhos:

                # Verifica se a vizinha ainda existe na simulação
                if viz_id not in self.lista_particulas:
                    p1.lista_vizinhos.remove(viz_id)
                    continue

                p2 = self.lista_particulas[viz_id]
                contato_id = ids2str(particula_id, viz_id)
                if contato_id in contatos_ja_verificados:
                    continue  # Pula o resto do código dentro do for e vai para a proxima iteração

                contatos_ja_verificados.add(contato_id)
                distancia_centros, distancia_contato = distancia_entre_particulas(p1, p2)

                if distancia_contato < 0:
                    self.lista_contatos_existentes.add(contato_id)
                    # Vemos se ele já existiu alguma vez
                    if contato_id in self.lista_contatos.keys():
                        # Se sim, atualizamos (mesmo código da atualização anterior)
                        # c = self.lista_contatos[contato_id]
                        if p1.id < p2.id:
                            self.lista_contatos[contato_id].particula1 = p1
                            self.lista_contatos[contato_id].particula2 = p2
                        else:
                            self.lista_contatos[contato_id].particula1 = p2
                            self.lista_contatos[contato_id].particula2 = p1
                        self.lista_contatos[contato_id].distancia = distancia_contato
                        self.lista_contatos[contato_id].distancia_centros = distancia_centros
                        self.lista_contatos[contato_id].passo_de_tempo = self.passo_de_tempo
                        self.lista_contatos[contato_id].existencia.append(self.iteracao)
                        self.lista_contatos[contato_id].iteracao_atual = self.iteracao

                    else:
                        # Se não, criamos um novo
                        novo_contato = Contato()
                        novo_contato.id = contato_id
                        if p1.id < p2.id:
                            novo_contato.particula1 = p1
                            novo_contato.particula2 = p2
                        else:
                            novo_contato.particula1 = p2
                            novo_contato.particula2 = p1
                        novo_contato.distancia = distancia_contato
                        novo_contato.distancia_centros = distancia_centros
                        novo_contato.passo_de_tempo = self.passo_de_tempo
                        novo_contato.existencia.append(self.iteracao)
                        novo_contato.iteracao_atual = self.iteracao

                        # Atualiza na lista geral, e na lista de existentes
                        self.lista_contatos[contato_id] = deepcopy(novo_contato)

                else:
                    # Se o contato não existe, deve ser retirado das listas
                    # TODO Talvez guardar todos os contatos que já existiram não seja uma boa idéia, estouro de memoria
                    if contato_id in self.lista_contatos_existentes:
                        self.lista_contatos_existentes.remove(contato_id)

    def reseta_forcas(self):
        [p.reseta_forcas() for p in self.lista_particulas.values()]

    def reseta_forcasa_antiga(self):
        for particula_id, val in self.lista_particulas.items():
            p = self.lista_particulas[particula_id]
            p.forca_normal['x'] = 0
            p.forca_normal['y'] = 0
            p.forca_normal['modulo'] = 0
            p.forca_tangencial['x'] = 0
            p.forca_tangencial['y'] = 0
            p.forca_tangencial['modulo'] = 0
            p.forca_total['x'] = 0
            p.forca_total['y'] = 0
            p.forca_total['modulo'] = 0
            p.torque = 0

            if self.lista_particulas[particula_id].livre:
                forca_gravidade = self.lista_particulas[particula_id].massa * self.gravidade['y']
                self.lista_particulas[particula_id].forca_total['y'] = forca_gravidade

    def calculo_forcas(self):

        # lista_contatos = self.lista_contatos
        # lista_particulas = self.l

        # Calcula as forças nos contatos
        # [contato.calcula_forcas() for c_id, contato in self.lista_contatos.items() if c_id in self.lista_contatos_existentes]
        [self.lista_contatos[cont_id].calcula_forcas() for cont_id in self.lista_contatos_existentes]

        # [self.atribuicao_forcas(contato) for c_id, contato in self.lista_contatos.items() if c_id in self.lista_contatos_existentes]

        for contato_id in self.lista_contatos_existentes:
            # Calcula as forças no contato
            # self.lista_contatos[contato_id].calcula_forcas()

            # Atualiza as forças calculadas nas partículas
            c = self.lista_contatos[contato_id]
            p1_id = c.particula1.id
            p2_id = c.particula2.id
            p1 = self.lista_particulas[p1_id]
            p2 = self.lista_particulas[p2_id]

            p1.forca_normal['x'] += c.forca_normal['x']
            p1.forca_normal['y'] += c.forca_normal['y']
            p1.forca_normal['modulo'] += c.forca_normal['modulo']
            p1.forca_tangencial['x'] += c.forca_tangencial['x']
            p1.forca_tangencial['y'] += c.forca_tangencial['y']
            p1.forca_tangencial['modulo'] += c.forca_tangencial['modulo']
            p1.forca_total['x'] += c.forca_total['x']
            p1.forca_total['y'] += c.forca_total['y']
            p1.forca_total['modulo'] += c.forca_total['modulo']
            # TODO Colocar o torque dentro do calculo no contato
            p1.torque += -c.forca_tangencial['modulo'] * p1.raio

            # Particula 2 -------------------------------------
            p2.forca_normal['x'] += -c.forca_normal['x']
            p2.forca_normal['y'] += -c.forca_normal['y']
            p2.forca_normal['modulo'] += c.forca_normal['modulo']

            p2.forca_total['x'] += -c.forca_total['x']
            p2.forca_total['y'] += -c.forca_total['y']
            p2.forca_total['modulo'] += c.forca_total['modulo']

            p2.forca_tangencial['x'] += -c.forca_tangencial['x']
            p2.forca_tangencial['y'] += -c.forca_tangencial['y']
            p2.forca_tangencial['modulo'] += c.forca_tangencial['modulo']
            # TODO Colocar o torque dentro do calculo no contato
            p2.torque += -c.forca_tangencial['modulo'] * p2.raio
            pass

    def atribuicao_forcas(self,contato):
        # Atualiza as forças calculadas nas partículas
        c = contato

        p1_id = c.particula1.id
        p2_id = c.particula2.id
        p1 = self.lista_particulas[p1_id]
        p2 = self.lista_particulas[p2_id]

        p1.forca_normal['x'] += c.forca_normal['x']
        p1.forca_normal['y'] += c.forca_normal['y']
        p1.forca_normal['modulo'] += c.forca_normal['modulo']
        p1.forca_tangencial['x'] += c.forca_tangencial['x']
        p1.forca_tangencial['y'] += c.forca_tangencial['y']
        p1.forca_tangencial['modulo'] += c.forca_tangencial['modulo']
        p1.forca_total['x'] += c.forca_total['x']
        p1.forca_total['y'] += c.forca_total['y']
        p1.forca_total['modulo'] += c.forca_total['modulo']
        # TODO Colocar o torque dentro do calculo no contato
        p1.torque += -c.forca_tangencial['modulo'] * p1.raio

        # Particula 2 -------------------------------------
        p2.forca_normal['x'] += -c.forca_normal['x']
        p2.forca_normal['y'] += -c.forca_normal['y']
        p2.forca_normal['modulo'] += c.forca_normal['modulo']

        p2.forca_total['x'] += -c.forca_total['x']
        p2.forca_total['y'] += -c.forca_total['y']
        p2.forca_total['modulo'] += c.forca_total['modulo']

        p2.forca_tangencial['x'] += -c.forca_tangencial['x']
        p2.forca_tangencial['y'] += -c.forca_tangencial['y']
        p2.forca_tangencial['modulo'] += c.forca_tangencial['modulo']
        # TODO Colocar o torque dentro do calculo no contato
        p2.torque += -c.forca_tangencial['modulo'] * p2.raio


    def corretor(self):
        for particula_id in self.lista_particulas_livres:
            self.lista_particulas[particula_id].corretor()

    def verifica_continuidade(self):

        # Máximo de iterações
        if self.limite_iteracoes > 0:
            if self.iteracao >= self.limite_iteracoes:
                print('Atingido o limite de {} iterações'.format(self.limite_iteracoes))
                return True
        # Máximo de tempo simulado
        if self.limite_tempo_simulado > 0:
            if self.tempo_simulado >= self.limite_tempo_simulado:
                print('Atingido o limite de {} tempo simulado'.format(self.limite_tempo_simulado))
                return True

        # Máximo de tempo real
        if self.limite_tempo_real > 0:
            if self.tempo_real >= self.limite_tempo_real:
                print('Atingido o limite de {} tempo real decorrido'.format(self.limite_tempo_real))
                return True

        # Existencia de particulas livres
        if len(self.lista_particulas_livres) < 1:
            print('Não há particulas livres na simulação')
            return True
        pass

    def set_estado(self, sistema):
        pass

    def mostrar_output(self):
        # os.system('cls' if os.name == 'nt' else 'clear')
        # os.system('clear')
        # print('\nIteração {} de {}'.format(self.iteracao, self.limite_iteracoes))
        # print('     Tempo simulado: {:f}'.format(self.tempo_simulado))
        # print('     Tempo decorrido: {:f}s'.format(self.tempo_real))

        mostrar_sistema(self, self.figure)

    def set_configuracao(self, sistema=Prepare()):
        # Faz o setup das partículas a aprtir de uma configuração recebida
        self.lista_particulas = sistema.lista_particulas
        self.lista_particulas_fixas = sistema.lista_particulas_fixas
        self.lista_particulas_livres = sistema.lista_particulas_livres

        self.raio_maximo = sistema.raio_maximo
        self.raio_minimo = sistema.raio_minimo

        self.configuracao = sistema.configuracao

        self.passo_de_tempo = self.configuracao.passo_de_tempo
        self.gn_maximo = sistema.gn_maximo

        self.limites = sistema.limites.copy()

    def verificar_limites(self):

        for particula_id in self.lista_particulas_livres:
            deletar = False
            if self.lista_particulas[particula_id].posicao['y'] < self.limites['ymin']:
                deletar = True
            # elif self.lista_particulas[particula_id].posicao['y'] > self.limites['ymax']:
            #     deletar = True
            # elif self.lista_particulas[particula_id].posicao['x'] < self.limites['xmin']:
            #     deletar = True
            # elif self.lista_particulas[particula_id].posicao['x'] > self.limites['xmax']:
            #     deletar = True

            if deletar:
                del self.lista_particulas[particula_id]
                self.lista_particulas_livres.remove(particula_id)
