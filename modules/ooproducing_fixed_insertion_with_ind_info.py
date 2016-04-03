#!/usr/bin/python

import subprocess as sp

beg = sp.Popen(['pwd'],stdout=sp.PIPE)
location = beg.communicate()[0].strip()
#print location

f_b = open(location+"/parameter.txt","r")
sp_info = f_b.readlines()
f_b.close()

ME = sp_info[0].strip().split("=")[1]
lib_file = sp_info[1].strip().split("=")[1]
insertME = sp_info[2].strip().split("=")[1]
filterType = input("Please enter filter: 1.mild or 2.stringent: ")
iden = ""
output_folder = ""
if filterType == 1:
	iden = sp_info[3].strip().split("=")[1]
	output_folder = "/lab01/Projects/MEScan/%s/juiwan/generating_list_of_fixed_insertion/mild/"%ME
elif filterType == 2:
	iden = sp_info[4].strip().split("=")[1]
	output_folder = "/lab01/Projects/MEScan/%s/juiwan/generating_list_of_fixed_insertion/stringent/"%ME

fh = open(output_folder+"fixed_insertion_candidates.bed","r")
candidates = fh.readlines()
fh.close()

d_m = {}	#locusID as key, {ind:[#raw_read,#uniq_read]} as value
d_p = {}
for row in candidates:
	row=row.strip().split("\t")
	if row[5] == "+":
		d_p[row[3]]={}
	else:
		d_m[row[3]]={}

d_lib_r = {}	#ind as key, mapped_read as value
#to retrive the number of mapped read for the library used
i = []
f_lib = open("/lab01/Projects/MEScan/%s/juiwan/%s"%(ME,lib_file),"r")
lib_text = f_lib.readlines()
f_lib.close()
for row in lib_text:
	row=row.strip().split("\t")
	i.append(row[1])
print i, len(i)
for s in i:
	qi = sp.Popen(['ls','/lab01/Projects/MEScan/%s/Sample_%s/'%(ME,s)],stdout = sp.PIPE)
	qii = sp.Popen(['grep','sorted.bam$'],stdin = qi.stdout, stdout = sp.PIPE)
	bam_file = qii.communicate()[0].strip()
#	print bam_file
	q1 = sp.Popen(['samtools','idxstats','/lab01/Projects/MEScan/%s/Sample_%s/%s'%(ME,s,bam_file)],stdout = sp.PIPE)
	q2 = sp.Popen(['awk',r'{sum+=$3;} END {print sum;}'],stdin=q1.stdout,stdout=sp.PIPE)
	mapped_read = float(q2.communicate()[0].strip().split("\n")[0])
#	print "mapped read is %s"%mapped_read
	d_lib_r[s]=mapped_read
print d_lib_r

for k in range(0,2,1):
	if k == 0 :
		orient = "minus"
		d = d_m
	else:
		orient = "plus"
		d = d_p
	print orient
	fk = open("/lab01/Projects/MEScan/%s/output_bwa-blast.29.%s.500.repeatcover_off.flexible./%s_all.insert_%s.29.%s.500.repeatcover_off.flexible.temp"%(ME,iden,insertME,orient,iden),"r")
	data = fk.readlines()
	fk.close()

	for row in data:
		row=row.strip().split(" ")
		if row[5] in d.keys():
			if row[4] not in d[row[5]].keys():
				d[row[5]][row[4]] = [int(row[3]),1]
			else:
				d[row[5]][row[4]][0] += int(row[3])
				d[row[5]][row[4]][1] += 1

	out = open(output_folder+"Fixed_insertion_%s.%s.29.%s.500.repeatcover_off.flexible.BB.bed"%(orient,insertME,iden),"w")		
	
	fz = open("/lab01/Projects/MEScan/%s/output_bwa-blast.29.%s.500.repeatcover_off.flexible./%s_all.29.%s.500.repeatcover_off.flexible.BB.bed"%(ME,iden,insertME,iden),"r")
	template = fz.readlines()
	fz.close()

	for row in template:
		row=row.strip().split("\t")
		if row[6] in d.keys():
			ind_list = []
			TPM_list = []
			UR_list = []
			flag = False
			for ind in d[row[6]].keys():
				if ind in i:
					flag = True
					ind_list.append(ind)
					temp_TPM = (d[row[6]][ind][0]*1000000.0)/d_lib_r[ind]
					TPM_list.append("%s"%float("%.6g"%temp_TPM))
					UR_list.append(str(d[row[6]][ind][1]))
			if flag:
				out.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+",".join(ind_list)+"\t"+row[6]+"\t"+",".join(ind_list)+"\t"+",".join(TPM_list)+"\t"+",".join(UR_list)+"\n")
out.close()
				
