#!/usr/bin/python

import subprocess as sp, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
insertME=''.join(args.mei)
option_tag=''.join(args.option_tag)
path_current=''.join(args.path)

fh = open(path_current+"Results%s/TPM_stats_90_maxUR_10.txt"%(option_tag),"r")
ref = fh.readlines()[1:]
fh.close()
ind_TPM_UR = {}         #ind as key, (TPM,UR) as value
ind_loci = {}           #ind as key, num_loci as value
for row in ref:
        row=row.strip().split("\t")
        ind_TPM_UR[row[0]] = (float(row[2]),int(row[1]))
        ind_loci[row[0]] = 0
#print ind_loci

d_lib_r = {}	#ind as key, mapped_read as value
#to retrive the number of mapped read for the library used

lib_i = []
ln0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
lib_name = sp.Popen(['grep','library'],stdin = ln0.stdout, stdout = sp.PIPE).communicate()[0].strip()
#print lib_name
f_lib = open(path_current+lib_name,"r")
lib_text = f_lib.readlines()
f_lib.close()
for row in lib_text:
        row=row.strip().split("\t")
        lib_i.append(row[1])

is0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
is1 = sp.Popen(['grep','Sample'],stdin = is0.stdout, stdout = sp.PIPE)
ind_sample = sp.Popen(['awk','-F',r"_",r'{print $2}'],stdin = is1.stdout, stdout = sp.PIPE).communicate()[0].strip().split("\n")
i = list(set(lib_i) & set(ind_sample))
#print i, len(i)

for s in i:
	qi = sp.Popen(['ls','%sSample_%s/'%(path_current,s)],stdout = sp.PIPE)
	qii = sp.Popen(['grep','sorted.bam$'],stdin = qi.stdout, stdout = sp.PIPE)
	bam_file = qii.communicate()[0].strip()
#	print bam_file
	q1 = sp.Popen(['samtools','idxstats','%sSample_%s/%s'%(path_current,s,bam_file)],stdout = sp.PIPE)
	q2 = sp.Popen(['awk',r'{sum+=$3;} END {print sum;}'],stdin=q1.stdout,stdout=sp.PIPE)
	mapped_read = float(q2.communicate()[0].strip().split("\n")[0])
#	print "mapped read is %s"%mapped_read
	d_lib_r[s]=mapped_read
#print d_lib_r

d = {}	#locusID as key, {ind:[#raw_read,#uniq_read]} as value
for k in range(0,2,1):
	if k == 0 :
		orient = "minus"
	else:
		orient = "plus"
#	print orient
	fk = open(path_current+"output_bwa-blast%s/%s_all.insert_%s%stemp"%(option_tag,insertME,orient,option_tag),"r")
	data = fk.readlines()
	fk.close()

	for row in data:
		row=row.strip().split(" ")
		if row[5] not in d.keys():
			d[row[5]]={}
			d[row[5]][row[4]] = [int(row[3]),1]
		else:
			if row[4] not in d[row[5]].keys():
				d[row[5]][row[4]] = [int(row[3]),1]
			else:
				d[row[5]][row[4]][0] += int(row[3])
				d[row[5]][row[4]][1] += 1

out = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_All_insertion%sbed"%(option_tag,option_tag),"w")		
out_count = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_All_insertion_ind_count_loci%stxt"%(option_tag,option_tag),"w")
fz = open(path_current+"output_bwa-blast%s/%s_all%sBB.bed"%(option_tag,insertME,option_tag),"r")
template = fz.readlines()
fz.close()

for row in template:
	row=row.strip().split("\t")
	ind_list = []
	TPM_list = []
	UR_list = []
	flag = False
	for ind in d[row[6]].keys():
		if ind in i:
			temp_TPM = (d[row[6]][ind][0]*1000000.0)/d_lib_r[ind]
			if temp_TPM > ind_TPM_UR[ind][0] and d[row[6]][ind][1] > ind_TPM_UR[ind][1]:
				flag = True
				ind_list.append(ind)
				TPM_list.append("%s"%float("%.6g"%temp_TPM))
				UR_list.append(str(d[row[6]][ind][1]))
				ind_loci[ind] += 1

	if flag:
		out.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+row[5]+"\t"+row[6]+"\t"+",".join(ind_list)+"\t"+",".join(TPM_list)+"\t"+",".join(UR_list)+"\n")
out.close()
	
for ind in ind_loci.keys():
	out_count.write(ind+"\t"+str(ind_loci[ind])+"\n")
out_count.close()
