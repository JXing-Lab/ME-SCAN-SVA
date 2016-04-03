#!/usr/bin/python

import subprocess as sp

beg = sp.Popen(['pwd'],stdout=sp.PIPE)
location = beg.communicate()[0].strip()
#print location

f_b = open(location+"/parameter.txt","r")
sp_info = f_b.readlines()
f_b.close()

ME = sp_info[0].strip().split("=")[1]
insertME = sp_info[2].strip().split("=")[1]

filterType = input("Please enter the filter 1.mild or 2.stringent: ")
iden = ""
folder = ""
if filterType == 1:
	iden = sp_info[3].strip().split("=")[1]
	folder = "/lab01/Projects/MEScan/%s/juiwan/output_from_inheritance_mild/"%ME
elif filterType == 2:
	iden = sp_info[4].strip().split("=")[1]
	folder = "/lab01/Projects/MEScan/%s/juiwan/output_from_inheritance_stringent/"%ME

fh = open(folder+"TPM_stats_90_maxUR_10_%s.txt"%(iden),"r")
ref = fh.readlines()[1:]
fh.close()
ind_TPM_UR = {}		#ind as key, (TPM,UR) as value
ind_loci = {}		#ind as key, {"Polymorphic":#,"Novel_polymorphic":#}
for row in ref:
	row=row.strip().split("\t")
	ind_TPM_UR[row[0]] = (float(row[2]),int(row[1]))
	ind_loci[row[0]] = {"Polymorphic":0,"Novel_polymorphic":0}
#print ind_loci

insert = ["Polymorphic","Novel_polymorphic"]
for fa in insert:
	print fa	
	out_count = open(folder+"latest_data_with_TPM_UR_filters/%s_insertion_ind_count_loci_%s.bed"%(fa,iden),"w")
	
	orient = ""
	for k in range(0,2,1):
		if k == 0:
			orient = "minus"
		else:
			orient = "plus"

		fk = open("/lab01/Projects/MEScan/%s/output_bwa-blast.29.%s.500.repeatcover_off.flexible./%s_insertion_%s.%s.29.%s.500.repeatcover_off.flexible.BB.bed"%(ME,iden,fa,orient,insertME,iden),"r")
		data = fk.readlines()
		fk.close()

		out = open(folder+"latest_data_with_TPM_UR_filters/latest_data_TPM-10UR_filters_%s_insertion_%s_%s.bed"%(fa,orient,iden),"w")

		for row in data:
			row=row.strip().split("\t")
			ind_list = row[7].split(",")
			TPM_list = row[8].split(",")
			UR_list = row[9].split(",")
			temp_ind = []
			temp_TPM = []
			temp_UR = []
			for x in range(0,len(ind_list),1):
				if ind_list[x] in ind_TPM_UR.keys():
					if float(TPM_list[x]) > ind_TPM_UR[ind_list[x]][0] and int(UR_list[x]) > ind_TPM_UR[ind_list[x]][1]:
						temp_ind.append(ind_list[x])
						temp_TPM.append(TPM_list[x])
						temp_UR.append(UR_list[x])
						ind_loci[ind_list[x]][fa] += 1
			if len(temp_ind) > 0:
				out.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+row[5]+"\t"+row[6]+"\t"+",".join(temp_ind)+"\t"+",".join(temp_TPM)+"\t"+",".join(temp_UR)+"\n")
		out.close()

	for ind in ind_loci.keys():
		out_count.write(ind+"\t"+str(ind_loci[ind][fa])+"\n")
	out_count.close()
