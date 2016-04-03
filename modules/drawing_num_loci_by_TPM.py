#!/usr/bin/env python

import argparse,os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
parser=argparse.ArgumentParser()
parser.add_argument('--num',nargs='*')
parser.add_argument('--input',nargs='*')
parser.add_argument('--output',nargs='*')
args=parser.parse_args()

num=''.join(args.num)
input_file=''.join(args.input)
output=''.join(args.output)

ind = np.arange(int(num))
width = 0.01

fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111) 

f = open(input_file, 'r')

i=0
initial_row=f.readline()
initial_columns = initial_row.split()
xtext=initial_columns[1:int(num)+1]
xax= [int(xa) for xa in xtext]
xlabel = [str(xl) for xl in xtext]
legend = []
for row in f.readlines():
    columns = row.split()
    rec = ind+width*i
    rec = [r for r in rec]
    val = columns[1:int(num)+1]
    val = [int(v) for v in val]
    ax.bar(rec, val, width, color=cm.jet(1.*i/(0.5*int(num)*int(num))), edgecolor='none')
    legend.append(columns[0])
    i=i+1
ax.set_xticks(xax)
ax.set_xticklabels(xlabel)
ax.legend(legend)
canvas.print_figure(output)

