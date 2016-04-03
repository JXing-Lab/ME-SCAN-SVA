#!/usr/bin/env python

import argparse,glob,os,re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
parser=argparse.ArgumentParser()
parser.add_argument('--min',nargs='*')
parser.add_argument('--max',nargs='*')
parser.add_argument('--input_folder',nargs='*')
parser.add_argument('--output',nargs='*')
parser.add_argument('--stag',nargs='*')

args=parser.parse_args()
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
input_folder=''.join(args.input_folder)
stag=''.join(args.stag)

input_file=input_folder+"*.sensi_"+stag
indv_group=[]
f=glob.glob(input_file)
output=''.join(args.output)

for i in f:

    mn=''.join(args.min)
    mx=''.join(args.max)

    fn=os.path.splitext(i)[0]
    indv=re.split('stuff/', fn)
    individual=re.split('_',indv[1])   
    indv_group.append(individual[0])
    ftpm=fn+".tpm_"+stag
    fsensi=fn+".sensi_"+stag
    each_tpm=open(ftpm,'r')
    each_sensi=open(fsensi,'r')
    x=each_tpm.readlines()
    y=each_sensi.readlines()
    ax.plot(x,y)
    ax.set_xlim(int(mn),int(mx))
box = ax.get_position()
ax.set(xlabel='TPM cutoff', ylabel='Sensitivity', axisbelow=True)
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(indv_group,loc='upper left',fontsize=10, bbox_to_anchor=(1.02, 1.0),ncol=1, prop={'size':7})
canvas.print_figure(output)
