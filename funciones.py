#!/bin/python

#recibe como parametro un csv y genera las organizaciones en markdown

import csv
import requests
import subprocess
import datetime
import sys
import json
import os

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
        num_fila = 0
        for row in csv_reader:
          if num_fila != 0:
            departamentos.write('%s\n' % row[1])
            barrios.write('%s' % row[1])
            barrios.write(',')
            barrios.write('%s\n' % row[2])
          num_fila += 1

  subprocess.call(["sort", "-u", "csv/barrios.csv", "-o", "csv/barrios.csv"])
#  with open('csv/barrios.csv','r') as barrios:
#    csv_reader = csv.reader(barrios, delimiter=',')
#    num_fila = 0
#    for row in csv_reader:
#      if num_fila != 0:
#        print (len (row))
#      num_fila += 1

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
        f.write('title: \"%s\"\n' % row[3].replace('\"', '\\"'))
        f.write('date: %s\n' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S -0300"))
        f.write('\n')
        f.write('departamento: \"%s\"\n' % row[1].replace('\"', '\\"'))
        f.write('barrio: \"%s\"\n' % row[1].replace('\"', '\\"'))
        f.write('actividades: \"%s\"\n' % row[2].replace('\"', '\\"'))
        f.write('necesidades: \"%s\"\n' % row[4].replace('\"', '\\"'))
        f.write('telefono_contacto: \"%s\"\n' % row[6].replace('\"', '\\"'))
        f.write('direccion: \"%s\"\n' % row[7].replace('\"', '\\"'))
        f.write('\n')
        f.write('otros_contactos: \"%s\"\n' % row[8].replace('\"', '\\"'))
        f.write('horario: \"%s\"\n' % row[11].replace('\"', '\\"'))
        f.write('aclaraciones: \"%s\"\n' % row[12].replace('\"', '\\"'))
        f.write('cuenta_bancaria: \"%s\"\n' % row[19].replace('\"', '\\"'))
        f.write('\n')
        f.write('---\n')
        f.close()
      num_org += 1

def crear_barrios():
  with open('csv/barrios.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_barrio = 1
    for row in csv_reader:
      f = open('barrios/barrio%s.md' % str(num_barrio).zfill(3),'w')
      f.write('---\n')
      f.write('nombre: \"%s\"\n' % row[1])
      f.write('departamento: \"%s\"\n' % row[0])
      f.write('---\n')
      f.write('\n')
      f.write('Barrio %s\n' % row[1])
      f.write('Departamento de %s\n' % row[0])
      f.close()
      num_barrio += 1

def crear_deptos ():
  with open('csv/departamentos.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_depto = 1
    for row in csv_reader:
      f = open('deptos/depto%s.md' % str(num_depto).zfill(2),'w')
      f.write('---\n')
      f.write('nombre: \"%s\"\n' % row[0])
      f.write('---\n')
      f.write('\n')
      f.write('Departamento de %s\n' % row[0])
      f.close()
      num_depto += 1

# crea un csv y un json para exportar los datos y ser compartidos
def crear_export ():
  with open('csv/planilla.csv') as csv_file:
    #aqui se deben colocar los nombres de las keys que se quieren compartir.
    #ahora coinciden con los nombres de la planilla menos las ultimas columnas que son internas
    campos = ['Departamento', 'Barrio/Localidad', 'Organización', 'Actividad/es', 'Necesidades', 'Número de contacto', 'Otro contacto', 'Dirección', 'Horario', 'Aclaraciones Adicionales', 'Cuenta Banco', 'Coordenada Latitud', 'Coordenada Longitud']
    csv_reader = csv.DictReader(csv_file, campos)

    #archivo de salida csv
    csv_out_name = 'export/datos.csv'
    os.makedirs(os.path.dirname(csv_out_name), exist_ok=True)
    csv_out = open(csv_out_name, 'w')

    writer = csv.DictWriter(csv_out, campos, extrasaction='ignore') #se ignoran los campos que no estan en 'campos'
    writer.writeheader();
    num_linea = 0
    #se crea el csv solo con los campos a compartir
    for row in csv_reader:
      if num_linea != 0:
        writer.writerow(row)
      num_linea += 1
    csv_out.close()

  #se crea el json a partir del nuevo csv
  with open('export/datos.csv') as csv_file:
    #aqui se deben colocar los nombres de las keys que se quieren compartir.
    #ahora coinciden con los nombres de la planilla menos las ultimas columnas que son internas
    campos = ['Fecha de actualización', 'Departamento', 'Barrio/Localidad', 'Organización', 'Actividad/es', 'Necesidades', 'Número de contacto', 'Otro contacto', 'Dirección', 'Horario', 'Aclaraciones Adicionales', 'Cuenta Banco', 'Coordenada Latitud', 'Coordenada Longitud']
    csv_reader = csv.DictReader(csv_file, campos)

    #archivo de salida json
    json_out_name = 'export/datos.json'
    os.makedirs(os.path.dirname(json_out_name), exist_ok=True)
    jsonfile = open(json_out_name, 'w')

    jsonfile.write('[\n ')
    num_linea = 0
    for row in csv_reader:
      if num_linea != 0:
        if num_linea != 1:
          jsonfile.write(',\n')
        json.dump(row, jsonfile, ensure_ascii=False, indent=4)
      num_linea += 1
    jsonfile.write(']')
    jsonfile.close()
