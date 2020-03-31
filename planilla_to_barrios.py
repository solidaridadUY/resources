#!/bin/python

#recibe como parametro un csv y genera las organizaciones en markdown

import sys
import csv
import datetime

with open('barrios.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_linea = 0
    for row in csv_reader:
        if num_linea != 0:
            f = open('barrio%s.md' % num_linea,'w')
            f.write('---\n')
            f.write('nombre: \"%s\"\n' % row[1])
            f.write('departamento: \"%s\"\n' % row[0])
            f.write('\n')
            f.write('Barrio %s\n' % row[1])
            f.write('Departamento de %s\n' % row[0])
            f.close()
        num_linea += 1
