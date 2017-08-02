# -*- coding: utf-8 -*-
__author__ = 'abraao'

import pickle
from visualizador2 import mostrar_sistema3 as mostrar_sistema
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
FigureCanvasQTAgg as FigureCanvas,
NavigationToolbar2QT as NavigationToolBar)
import time

Ui_MainWindow, QMainWindow = loadUiType('GUI/visualizadormainwindow2.ui')

class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.fig_dict = {}

        self.mplfigs.itemClicked.connect(self.changefig)
        self.botaoArquivo.clicked.connect(self.abrearquivo)
        self.botaoAplicar.clicked.connect(self.limpalista)


        fig = Figure()
        self.addmpl(fig)

    def abrearquivo(self):
        # fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home/abraao/Dropbox/PythonProjects/DM Conveyor/save')
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/media/abraao/Downloads/SIMULACOES_DMCONVEYOR')
        # fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'D:\SIMULACOES_DMCONVEYOR\save')

        f = open(fname, 'rb')

        with f:
            self.sistema = pickle.load(f)
            nomearquivo = fname.split('/')[-1]
            string = ('File: '+ nomearquivo + '\n'
                      + 'Iteration: '+str(self.sistema.iteracao)+ '\n'
                      + 'Time: {:2f} seg'.format(self.sistema.tempo_simulado))
            self.textoInfo1.setPlainText(string)

            self.criarfiguras()

    def changefig(self, item):
            # print('ID:' + str(item.id))
            text = item.text()
            self.rmmpl()
            self.addmpl(self.fig_dict[text])

    def limpalista(self):
        self.mplfigs.clear()
        self.criarfiguras()

    def addfig(self, name, fig):
        self.fig_dict[name] = fig
        self.mplfigs.addItem(name)

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolBar(self.canvas,self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def criarfiguras(self):

        self.mplfigs.clear()

        valores = [float(self.minimo.text()), float(self.maximo.text())]

        if self.radioButton_manual.isChecked():
            manual = True
        else:
            manual = False

        # janela = [x1,y1,x2,y2]
        janela = [-4, -1, 2, 2]

        print(manual)
        print(valores)

        comeco = time.time()
        fig1 = Figure()
        fig1 = mostrar_sistema(self.sistema,fig1,'x',manual, valores, janela=janela)
        print(time.time()-comeco)

        comeco = time.time()
        fig2 = Figure()
        fig2 = mostrar_sistema(self.sistema, fig2, 'y', manual, valores, janela=janela)
        print(time.time() - comeco)

        comeco = time.time()
        fig3 = Figure()
        fig3 = mostrar_sistema(self.sistema, fig3, 'modulo', manual, valores, janela=janela)
        print(time.time() - comeco)

        self.addfig('Velocity modulus', fig3)
        self.addfig('X component', fig1)
        self.addfig('Y component', fig2)

        # self.mplfigs.setCurrentItem(2)

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np

    # Carregar o arquivo

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.setWindowTitle('DM Conveyor - CEFET MG')

    main.minimo.setText('3')
    main.maximo.setText('4')

    main.show()
    sys.exit(app.exec_())
