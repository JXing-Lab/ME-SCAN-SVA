#!/usr/bin/env python

import argparse,glob,os,re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
parser=argparse.ArgumentParser()
parser.add_argument('--input_file',nargs='*')
parser.add_argument('--output',nargs='*')

args=parser.parse_args()
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
input_file=''.join(args.input_file)
output=''.join(args.output)


f=open(input_file,'r')

fn=f.readlines()
indv_group=[]

ig=[]

for i in fn:
	c = i.split()
	ig.append(c[0])

for indv in list(set(ig)):
	indv_group.append(indv)
	x=[]
	y=[]
	for row in fn:
		columns = row.split()
		if columns[0]==indv: 
			y.append(columns[2])
			x.append(columns[1])
	ax.plot(x,y,'o',markersize=5)

box = ax.get_position()
ax.set(xlabel='TPM cutoff', ylabel='The number of loci', axisbelow=True)
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(indv_group,loc='upper left',fontsize=10, bbox_to_anchor=(1.02, 1.0),ncol=1, prop={'size':7})
canvas.print_figure(output)
