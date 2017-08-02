# -*- coding: utf-8 -*-
__author__ = 'abraao'

# from visualizador2 import mostrar_sistema3 as mostrar_sistema
# from PyQt4.uic import loadUiType
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt4agg import (
# FigureCanvasQTAgg as FigureCanvas,
# NavigationToolbar2QT as NavigationToolBar)
# import time

import pickle
import tkinter as tk
from tkinter import filedialog

# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askopenfilename()

file_path = 'save/para_benchmark2/para_benchmark2_18'

f = open(file_path, 'rb')
dm = pickle.load(f)

dm.salvar_historico = False
dm.periodo_mostrar_output = 100
dm.run()

