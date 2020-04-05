#!/bin/python

#recibe como parametro un csv y genera las organizaciones en markdown

import csv
import requests
import subprocess
import datetime
import sys

def mostrar_error():
  print ('ERROR - Argumentos incorrectos')
  print ('Modo de uso: cargar_datos.py ARGUMENTO')
  print ('')
  print ('Donde ARGUMENTO es:')
  print ('drive:\t\t Descargar planilla desde drive y crear archivos .csv')
  print ('orgs:\t\t Crear organizaciones a partir de planilla.csv')
  print ('barrios:\t Crear barrios a partir de barrios.csv')
  print ('deptos:\t\t Crear departamentos a partir de departamentos.csv')
  print ('crear_todo:\t orgs + barrios + deptos')
  sys.exit(1)

def descargar_planilla():
  r = requests.get('https://docs.google.com/spreadsheets/d/1o9oKU0ehVBzWlgcUZhxMDCi3FuCZIpq3RXtCozMJY6Q/export?format=csv&gid=1766258191')
  r.encoding = 'utf-8'
  with open('csv/planilla.csv','w') as planilla:
    planilla.write('%s' % r.text)

  with open('csv/planilla.csv','r') as planilla:
    with open('csv/barrios.csv','w') as barrios:
      with open('csv/departamentos.csv','w') as departamentos:
        csv_reader = csv.reader(planilla, delimiter=',')
        num_org = 0
        for row in csv_reader:
          departamentos.write('%s\n' % row[0])
          barrios.write('%s' % row[0])
          barrios.write(',')
          barrios.write('%s\n' % row[1])
          num_org += 1

  subprocess.call(["sort", "-u", "csv/barrios.csv", "-o", "csv/barrios.csv"])
  subprocess.call(["sort", "-u", "csv/departamentos.csv", "-o", "csv/departamentos.csv"])

def crear_orgs():
  with open('csv/planilla.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_org = 0
    for row in csv_reader:
      if num_org != 0:
        f = open('orgs/org%s.markdown' % str(num_org).zfill(3),'w')
        f.write('---\n')
        f.write('layout: organizacion\n')
        f.write('\n')
        f.write('title: \"%s\"\n' % row[2])
        f.write('date: %s\n' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S -0300"))
        f.write('\n')
        f.write('departamento: \"%s\"\n' % row[0])
        f.write('barrio: \"%s\"\n' % row[1])
        f.write('actividades: \"%s\"\n' % row[3])
        f.write('necesidades: \"%s\"\n' % row[4])
        f.write('telefono_contacto: \"%s\"\n' % row[5])
        f.write('direccion: \"%s\"\n' % row[7])
        f.write('\n')
        f.write('otros_contactos: \"%s\"\n' % row[6])
        f.write('horario: \"%s\"\n' % row[8])
        f.write('aclaraciones: \"%s\"\n' % row[9])
        f.write('cuenta_bancaria: \"%s\"\n' % row[10])
        f.write('\n')
        f.write('---\n')
        f.close()
      num_org += 1

def crear_barrios():
  with open('csv/barrios.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_linea = 0
    for row in csv_reader:
      if num_linea != 0:
        f = open('barrios/barrio%s.md' % str(num_linea).zfill(3),'w')
        f.write('---\n')
        f.write('nombre: \"%s\"\n' % row[1])
        f.write('departamento: \"%s\"\n' % row[0])
        f.write('---\n')
        f.write('\n')
        f.write('Barrio %s\n' % row[1])
        f.write('Departamento de %s\n' % row[0])
        f.close()
      num_linea += 1

def crear_deptos ():
  with open('csv/departamentos.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_linea = 0
    for row in csv_reader:
      if num_linea != 0:
        f = open('deptos/depto%s.md' % str(num_linea).zfill(2),'w')
        f.write('---\n')
        f.write('nombre: \"%s\"\n' % row[0])
        f.write('---\n')
        f.write('\n')
        f.write('Departamento de %s\n' % row[0])
        f.close()
      num_linea += 1