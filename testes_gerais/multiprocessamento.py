# -*- coding: utf-8 -*-
__author__ = 'abraao'

import random
import math
import time
import matplotlib.pylab as plt
from multiprocessing import Pool
from multiprocessing import Process, Queue
import threading

random.seed(42)

# Classe partícula =====================================================================================================

class Particula:
    def __init__(self):
        self.id = None
        self.x = random.random()
        self.y = random.random()
        self.forca = None
        pass

# Classe Contato =====================================================================================================

class Contato:
    def __init__(self):
        self.particula1 = None
        self.particula2 = None
        self.forca_total = None
        pass

    def calcula_forcas(self):
        # print('Tô calculando')
        x1 = self.particula1.x
        y1 = self.particula1.y
        x2 = self.particula2.x
        y2 = self.particula2.y
        forca = 0
        for i in range(15):
            forca += math.sqrt( (x1-x2)**2 + (y1-y2)**2)

        self.forca_total = forca
        self.particula1.forca = - forca

# Classe DM ============================================================================================================

class DincamicaMolecular:
    def __init__(self):
        self.lista_particulas = {}
        self.lista_contatos = {}
        self.lista_contatos_existentes = []

    def inicializar(self):
        n = 25
        for i in range(n):
            nova_particula = Particula()
            nova_particula.id = i

            self.lista_particulas[i] = nova_particula

        for i in range(n):
            for k in range(i+1,n):
                novo_contato = Contato()
                novo_contato.particula1 = self.lista_particulas[i]
                novo_contato.particula2 = self.lista_particulas[k]
                contato_id = str(i) + '_' + str(k)
                self.lista_contatos[contato_id] = novo_contato
                self.lista_contatos_existentes.append(contato_id)

    def atualiza_forcas(self):
        for id in self.lista_contatos_existentes:
            c = self.lista_contatos[id]
            p1_id = c.particula1.id
            p2_id = c.particula2.id

            p1 = self.lista_particulas[p1_id]
            p2 = self.lista_particulas[p2_id]

            p1.forca = - c.forca_total
            p2.forca = - c.forca_total

    def calcula_forcas_aux1(self, id):
        c = self.lista_contatos[id]
        c.calcula_forcas()


    def calcula_forcas_aux2(self, *args):
        # print('piroquinha!')

        for id in args:
            c = self.lista_contatos[id]
            c.calcula_forcas()

    def calcula_forcas(self):

        for id in self.lista_contatos_existentes:
            self.lista_contatos[id].calcula_forcas()


    def calcula_forcas2(self):
        # Demorou 20x mais com 2 proc
        # Demorou 30x mais com 4 proc
        with Pool(4) as pool:
            resultados = pool.map(self.calcula_forcas_aux1,self.lista_contatos_existentes)

    def calcula_forcas3(self):

        n_processos = 3
        lista = self.lista_contatos_existentes
        tamanho = int(len(lista)/n_processos)
        lista_quebrada = [lista[x:x+tamanho] for x in range(0,len(lista), tamanho)]

        sublista = list(lista_quebrada[0])
        processo1 = Process(target=self.calcula_forcas_aux2, args=(sublista))
        processo1.start()
        processo1.join()

        sublista = list(lista_quebrada[1])
        processo2 = Process(target=self.calcula_forcas_aux2, args=(sublista))
        processo2.start()
        processo2.join()

        sublista = list(lista_quebrada[2])
        processo3 = Process(target=self.calcula_forcas_aux2, args=(sublista))
        processo3.start()
        processo3.join()

    def calcula_forcas_aux3(self,q, lista):
        # print('piroquinha')
        while True:
            n = q.get()
            if n == 0:
                return
            else:

                for id in lista:
                    c = self.lista_contatos[id]
                    c.calcula_forcas()

    def calcula_forcas_aux4(self, lista):
        for id in lista:
            c = self.lista_contatos[id]
            c.calcula_forcas()

    def calcula_forcas4(self):
        n_processos = 2
        lista = self.lista_contatos_existentes
        tamanho = int(len(lista) / n_processos)
        lista_quebrada = [lista[x:x + tamanho] for x in range(0, len(lista), tamanho)]

        # sublista = lista_quebrada[0]

        q = Queue()
        ps =[]
        for subs in lista_quebrada:
            p = Process(target=self.calcula_forcas_aux3, args=(q,subs))
            p.start()
            ps.append(p)

        for sublista in lista_quebrada:
            q.put(sublista)
            q.put(0)

        for i in range(len(lista_quebrada)):
            # print('chuleta')
            ps[i].join()

    def calcula_forcas5(self):
        threads = 7
        jobs = []

        lista = self.lista_contatos_existentes
        tamanho = int(len(lista) / threads)
        lista_quebrada = [lista[x:x + tamanho] for x in range(0, len(lista), tamanho)]

        for i in range(0, threads):
            out_list = list()
            sublista = lista_quebrada[i]
            th = threading.Thread(target=self.calcula_forcas_aux4(sublista))
            jobs.append(th)

        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

# ======================================================================================================================
if __name__ == '__main__':
    # import threading

    dm = DincamicaMolecular()
    dm.inicializar()

    print(len(dm.lista_particulas))
    print(len(dm.lista_contatos))
    print(len(dm.lista_contatos_existentes))

    t_inicio = time.time()

    for _ in range(1000):
        dm.calcula_forcas5()
    t_final = time.time()

    tempo_gasto = t_final - t_inicio
    print('Processamento: ' + str(tempo_gasto))

    # dm.atualiza_forcas()


    forcas = []
    for part in dm.lista_particulas.values():
        forcas.append(part.forca)

    print(forcas)
    # plt.plot(forcas)
    # plt.show()