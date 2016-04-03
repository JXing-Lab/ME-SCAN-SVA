#!/usr/bin/python
import argparse,os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
parser=argparse.ArgumentParser()
parser.add_argument('--input',nargs='*')
parser.add_argument('--output',nargs='*')

args=parser.parse_args()


fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)

input_file=''.join(args.input)
f = open(input_file, 'r')
output=''.join(args.output)

x=[]
y=[]
k=1
v=0
for row in f.readlines():
	v+=int(row)
	y.append(v)
	x.append(k)
	k+=1

ax.plot(x,y, alpha=0.5)
ax.set(xlabel='Number of genetically unrelated individual', ylabel='Number of loci', axisbelow=True)

canvas.print_figure(output)
