#!/usr/bin/python
import argparse,os
from collections import defaultdict
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
path_current=os.getcwd()+'/'

input_file=''.join(args.input)
f = open(input_file, 'r')
output=''.join(args.output)

data=defaultdict(list)
initial_row=f.readline()
initial_columns = initial_row.split()
del initial_columns[0]
initial_columns= [int(ic) for ic in initial_columns]

for row in f.readlines():
    columns = row.split()
    for i in initial_columns:
        data[i].append(int(columns[i+1]))

data_list=list(data.values())
ax.boxplot(data_list)
ax.set(xlabel='TPM cutoff', ylabel='Number of loci', axisbelow=True)
ax.set_xticklabels( initial_columns, rotation=45 ) 
canvas.print_figure(output)
