#!/usr/bin/python
## Decompress .gz file in subdirectory!!
import subprocess,os,time,argparse,fnmatch
parser=argparse.ArgumentParser()
parser.add_argument('--lib',nargs='*')
parser.add_argument('--mei',nargs='*')
parser.add_argument('--r1',nargs='*')
parser.add_argument('--r2',nargs='*')
parser.add_argument('--path',nargs='*')
args=parser.parse_args()

Library=''.join(args.lib)
MEI=''.join(args.mei)
read1=''.join(args.r1)
read2=''.join(args.r2)
file_path=''.join(args.path)

ap="'"
sl='\\'
path_current=os.getcwd()+'/'
path_each_lib=path_current+'Sample_'+Library+'/'


f_path=open(file_path,'r')

for row_path in f_path.readlines():
	columns_path = row_path.split('=')
	if columns_path[0] == "path_mescan":
		path_mescan = columns_path[1]
		path_mescan = path_mescan.rstrip('\n')
	elif columns_path[0] == "path_samtools":
		path_samtools = columns_path[1]
		path_samtools = path_samtools.rstrip('\n')
	elif columns_path[0] == "path_bwa":
		path_bwa = columns_path[1]
		path_bwa = path_bwa.rstrip('\n')
	elif columns_path[0] == "path_blast":
		path_blast = columns_path[1]
		path_blast = path_blast.rstrip('\n')
path_ref_blast=path_mescan+'ref_blast/'

# BWA mapping of read2 running

subprocess.call(''.join([ path_bwa+'bwa mem '+path_ref_blast+'human_g1k_v37.fasta '+read2+'.fastq > '+read2+'_BB.sam' ]),shell=True)
subprocess.call(''.join([ path_samtools+'samtools view -bS '+read2+'_BB.sam > '+read2+'_BB.bam']),shell=True)
subprocess.call(''.join([ path_samtools+'samtools sort '+read2+'_BB.bam '+read2+'_BB_sorted']),shell=True)
print("\n\n")
time.sleep(5)
subprocess.call(''.join([ path_samtools+'samtools index '+read2+'_BB_sorted.bam']),shell=True)
subprocess.call(''.join([ path_samtools+'samtools idxstats '+read2+'_BB_sorted.bam ']),shell=True)
print("\n\n-----"+Library+", BWA mapping is completed-----\n")

# Making fasta file from read1
subprocess.call(''.join([ 'cat '+read1+'.fastq | perl -e '+ap+'$i=0;while(<>){if(/^\@/&&$i==0){s/^\@/\>/;print;}elsif($i==1){print;$i=-3}$i++;}'+ap+\
 						'|awk '+ap+' {if(NR%2==0)print $0; else if(NR%2==1) print $1}'+ap+'> '+read1+'.fasta']),shell=True) 

# Blast running 
## makedb command to bash script.
subprocess.call(''.join([ path_blast+'blastn -task blastn-short -db '+path_current+MEI+'_fragment.fasta -query '+read1+'.fasta -outfmt 6 -out '+read1+'_'+MEI+'_blast.out']),shell=True)

subprocess.call(''.join([ 'sort -k 1b,1 '+read1+'_'+MEI+'_blast.out >'+read1+'_'+MEI+'_blast.filter']),shell=True)