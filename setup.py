# -*- coding: utf-8 -*-
__author__ = 'abraao'

from distutils.core import setup
from Cython.Build import cythonize


setup(ext_modules =cythonize('utilidades.py')  )
setup(ext_modules =cythonize('particula.py')  )
setup(ext_modules =cythonize('contato.py')  )
setup(ext_modules =cythonize('dinamicamolecular3_1.py')  )
