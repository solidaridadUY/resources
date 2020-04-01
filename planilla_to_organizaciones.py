#!/bin/python

#recibe como parametro un csv y genera las organizaciones en markdown

import sys
import csv
import datetime
import requests

r = requests.get('https://docs.google.com/spreadsheets/d/1o9oKU0ehVBzWlgcUZhxMDCi3FuCZIpq3RXtCozMJY6Q/export?format=csv&gid=1766258191')
r.encoding = 'utf-8'
c = open('organizaciones.csv','w')
c.write('%s' % r.text)

with open('organizaciones.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_org = 0
    for row in csv_reader:
        if num_org != 0:
            f = open('org%s.markdown' % str(num_org).zfill(3),'w')
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
