#!/bin/python

import sys
from funciones import *

if (len(sys.argv) != 2):
  mostrar_error()
else:
  argumento = sys.argv[1]

if (argumento == 'drive'):
  descargar_planilla()
elif (argumento == 'orgs'):
  crear_orgs()
elif (argumento == 'barrios'):
  crear_barrios()
elif (argumento == 'deptos'):
  crear_deptos()
elif (argumento == 'crear_todo'):
  crear_orgs()
  crear_barrios()
  crear_deptos()
else:
  mostrar_error()
