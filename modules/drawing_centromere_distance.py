#!/usr/bin/env python
import argparse,os
import matplotlib.pyplot as plt

parser=argparse.ArgumentParser()
parser.add_argument('--input',nargs='*')
parser.add_argument('--output',nargs='*')
args=parser.parse_args()

input_file=''.join(args.input)
f=open(input_file, 'r')
output=''.join(args.output)
chr1=[];chr2=[];chr3=[];chr4=[];chr5=[];chr6=[];chr7=[];chr8=[];chr9=[];chr10=[];chr11=[];chr12=[];chr13=[];chr14=[];chr15=[];chr16=[];chr17=[];chr18=[];chr19=[];chr20=[];chr21=[];chr22=[];chrX=[];chrY=[];
for row in f.readlines():
    columns=row.split()
    if columns[0] == "chr1": 
        chr1.append(columns[1])
    elif columns[0] == "chr2": 
        chr2.append(columns[1])
    elif columns[0] == "chr3": 
        chr3.append(columns[1])
    elif columns[0] == "chr4": 
        chr4.append(columns[1])
    elif columns[0] == "chr5": 
        chr5.append(columns[1])
    elif columns[0] == "chr6": 
        chr6.append(columns[1])
    elif columns[0] == "chr7": 
        chr7.append(columns[1])
    elif columns[0] == "chr8": 
        chr8.append(columns[1])
    elif columns[0] == "chr9": 
        chr9.append(columns[1])
    elif columns[0] == "chr10": 
        chr10.append(columns[1])
    elif columns[0] == "chr11": 
        chr11.append(columns[1])
    elif columns[0] == "chr12": 
        chr12.append(columns[1])
    elif columns[0] == "chr13": 
        chr13.append(columns[1])
    elif columns[0] == "chr14": 
        chr14.append(columns[1])
    elif columns[0] == "chr15": 
        chr15.append(columns[1])
    elif columns[0] == "chr16": 
        chr16.append(columns[1])
    elif columns[0] == "chr17": 
        chr17.append(columns[1])
    elif columns[0] == "chr18": 
        chr18.append(columns[1])
    elif columns[0] == "chr19": 
        chr19.append(columns[1])
    elif columns[0] == "chr20": 
        chr20.append(columns[1])
    elif columns[0] == "chr21": 
        chr21.append(columns[1])
    elif columns[0] == "chr22": 
        chr22.append(columns[1])
    elif columns[0] == "chrX": 
        chrX.append(columns[1])
    elif columns[0] == "chrY": 
        chrY.append(columns[1])

chr1= [int(v) for v in chr1];chr2= [int(v) for v in chr2];
chr3= [int(v) for v in chr3];chr4= [int(v) for v in chr4];
chr5= [int(v) for v in chr5];chr6= [int(v) for v in chr6];
chr7= [int(v) for v in chr7];chr8= [int(v) for v in chr8];
chr9= [int(v) for v in chr9];chr10= [int(v) for v in chr10];
chr11= [int(v) for v in chr11];chr12= [int(v) for v in chr12];
chr13= [int(v) for v in chr13];chr14= [int(v) for v in chr14];
chr15= [int(v) for v in chr15];chr16= [int(v) for v in chr16];
chr17= [int(v) for v in chr17];chr18= [int(v) for v in chr18];
chr19= [int(v) for v in chr19];chr20= [int(v) for v in chr20];
chr21= [int(v) for v in chr21];chr22= [int(v) for v in chr22];
chrX= [int(v) for v in chrX];chrY= [int(v) for v in chrY]
list_chr=[]
list_color=[]
list_legend=[]
dic_chr={'v_chr1':chr1,'v_chr2':chr2,'v_chr3':chr3,'v_chr4':chr4,'v_chr5':chr5,'v_chr6':chr6,'v_chr7':chr7,'v_chr8':chr8,'v_chr9':chr9,'v_chr10':chr10,'v_chr11':chr11,'v_chr12':chr12,'v_chr13':chr13,'v_chr14':chr14,'v_chr15':chr15,'v_chr16':chr16,'v_chr17':chr17,'v_chr18':chr18,'v_chr19':chr19,'v_chr20':chr20,'v_chr21':chr21,'v_chr22':chr22,'v_chrX':chrX,'v_chrY':chrY}
dic_color={'v_chr1':'#5C5858','v_chr2':'#657383','v_chr3':'#0020C2','v_chr4':'#95B9C7','v_chr5':'#82CAFF','v_chr6':'#CCFFFF','v_chr7':'#48CCCD','v_chr8':'#848b79','v_chr9':'#4AA02C','v_chr10':'#B2C248','v_chr11':'#B5EAAA','v_chr12':'#F5F5DC','v_chr13':'#FBB117','v_chr14':'#B5A642','v_chr15':'#493D26','v_chr16':'#F87431','v_chr17':'#FF2400','v_chr18':'#954535','v_chr19':'#C48189','v_chr20':'#F778A1','v_chr21':'#CA226B','v_chr22':'#6A287E','v_chrX':'#C45AEC','v_chrY':'#E3E4FA',}
dic_legend={'v_chr1':'chr1','v_chr2':'chr2','v_chr3':'chr3','v_chr4':'chr4','v_chr5':'chr5','v_chr6':'chr6','v_chr7':'chr7','v_chr8':'chr8','v_chr9':'chr9','v_chr10':'chr10','v_chr11':'chr11','v_chr12':'chr12','v_chr13':'chr13','v_chr14':'chr14','v_chr15':'chr15','v_chr16':'chr16','v_chr17':'chr17','v_chr18':'chr18','v_chr19':'chr19','v_chr20':'chr20','v_chr21':'chr21','v_chr22':'chr22','v_chrX':'chrX','v_chrY':'chrY'}

for variable in ['v_chr1','v_chr2','v_chr3','v_chr4','v_chr5','v_chr6','v_chr7','v_chr8','v_chr9','v_chr10','v_chr11','v_chr12','v_chr13','v_chr14','v_chr15','v_chr16','v_chr17','v_chr18','v_chr19','v_chr20','v_chr21','v_chr22','v_chrX','v_chrY']:

    if dic_chr[variable]!=[]:
        list_chr.append(dic_chr[variable])
        list_color.append(dic_color[variable])
        list_legend.append(dic_legend[variable])

fig = plt.figure()

ax = fig.add_subplot(1,1,1) 
ax.hist((list_chr),bins=5,color=(list_color))
ax.legend(list_legend)

ax.set_xlabel("Distance away from centromere")
ax.set_ylabel("Number of loci")
fig.savefig(output)
