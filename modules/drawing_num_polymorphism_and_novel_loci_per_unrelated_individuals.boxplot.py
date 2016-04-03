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
parser.add_argument('--input_total',nargs='*')
parser.add_argument('--output',nargs='*')

args=parser.parse_args()

input_file=''.join(args.input)
input_total=''.join(args.input_total)
output=''.join(args.output)

fig = Figure()
canvas = FigureCanvas(fig)
ax1 = fig.add_subplot(111) 

f = open(input_file, 'r')
f_total = open(input_total, 'r')
total_novel_number=f_total.readlines()
total_novel_number_columns = total_novel_number[0].split()
del total_novel_number_columns[0]
total_novel_number_columns=[int(tn) for tn in total_novel_number_columns]

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


ax1.boxplot(data_list)
ax1.set(xlabel='TPM cutoff', ylabel='Number of loci',  xticklabels=initial_columns)
ax1.set_xticklabels( initial_columns, rotation=45 ) 
ax2 = ax1.twiny()
ax2.boxplot(data_list)
ax2.set_xticklabels(total_novel_number_columns, fontsize=10, rotation=45)
canvas.print_figure(output)
