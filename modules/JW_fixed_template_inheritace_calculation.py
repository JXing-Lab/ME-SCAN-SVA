#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

def add_in_dict(output,each,relation,length,num):
	if (each,relation) not in output.keys():
		output[(each,relation)] = [num,length]
	else:
		output[(each,relation)][0] += num	#num is count of inheritance from each parent
		output[(each,relation)][1] += length	#length is the total number of insertion in that individual

def inheritance(parent_list,child_list,rel,each,output):
	for x in range(0,len(parent_list),1):
		inherit_from_parent = list(set(parent_list[x])&set(child_list))
		relation=""
		if x == 0:
			relation = rel+"father"
		else:
			relation = rel+"mother"
#		print each,relation,len(inherit_from_parent),len(child_list),len(parent_list[x])
		add_in_dict(output,each,relation,len(parent_list[x]),len(inherit_from_parent))
	none = list(set(child_list)-set(parent_list[0])-set(parent_list[1]))
#	print each,rel+"none",len(none),len(child_list)
	add_in_dict(output,each,rel+"none",len(child_list),len(none))

def add_in_final (dict,key,value):
	if key not in dict.keys():
		dict[key] = value
	else:
		dict[key].extend(value)

print "To get familyID and the relationship of each ind"
fk = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/library_81_107_info_trio.txt","r")
info = fk.readlines()
fk.close()
d_trio_info = {}	# family id as key, [(ind,relationship)] as value
for row in info:
	row=row.strip().split("\t")
	if row[3] not in d_trio_info.keys():
		d_trio_info[row[3]]=[(row[1],row[4])]
	else:
		d_trio_info[row[3]].append((row[1],row[4]))
#print d_trio_info

filterType = 0
filterType = input("Please enter 1.mild or 2.stringent: ")
iden = ""
output_folder=""
input_folder=""
if filterType == 1:
	iden = "48.48"
	output_folder = "/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/output_from_inheritance_mild/"
	input_folder = "/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/generating_list_of_fixed_insertion/mild/"
elif filterType == 2:
	iden = "65.65"
	output_folder = "/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/output_from_inheritance_stringent/"
	input_folder = "/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/generating_list_of_fixed_insertion/stringent/"

print "To get the reference TPM cutoff for each ind"
fz = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/Results.29.%s.500.repeatcover_off.flexible./sensitivity_stuff/TPM_stats_90.txt"%iden,"r")
ref = fz.readlines()
fz.close()
ref_TPM = {}	#ind as key, reference_TPM as value
for row in ref:
	row=row.strip().split("\t")
	ref_TPM[row[1]]=row[0]

insert = ["Fixed"]
#filterTPM = [0.5,1,2]
#filterUR = [0,1,2]
for fa in insert:
	print fa
	out_pos = open(output_folder+"%s_insertion_%s_variableTPM_and_UR_kid_inheritance.txt"%(fa,iden),"w")
	out_pos.write("ped_id\tinsertion_found_in")
	
	filterTPM = [x for x in range(20)]
	filterUR = [x for x in range(22)]

	final_output = {}	 #(familyID,relation) as key,[%_of_inheritance_rate,total_num_insertion_of_that_ind,...] as value
	for f_TPM in filterTPM:
		for f_UR in filterUR:
			print f_TPM, f_UR
			out_pos.write("\t%.1fTPM_>%iUR\ttotal_num_insertion"%(f_TPM,f_UR))
			output = {}	#(familyID,relation) as key, [number_of_inheritance,total_num_insertion_of_that_ind] as value
			for k in range(0,2,1):
				if k==0:
					type = "minus"
				else:
					type = "plus"
#				print type
				
				d_aftTPM = {}		# ind as key, [insertion pos] as value
				for row in info:
					row=row.strip().split("\t")
					d_aftTPM[row[1]] = []
			
				fh = open(input_folder+"%s_insertion_%s.SVA.29.%s.500.repeatcover_off.flexible.BB.bed"%(fa,type,iden),"r")
				data = fh.readlines()
				fh.close()

				for row in data:
					row = row.strip().split("\t")
					ind_list = row[7].split(",")
					TPM_list = row[8].split(",")
					UR_list = row[9].split(",")
					for y in range(0,len(ind_list),1):
						if float(TPM_list[y]) >= (f_TPM*float(ref_TPM[ind_list[y]])) and int(UR_list[y]) > f_UR:
							d_aftTPM[ind_list[y]].append(row[0]+":"+row[1])

				for each in d_trio_info.keys():
					for ind in d_trio_info[each]:
						if each == "1459":
							if ind[1] == "father":
								 child1_pos = d_aftTPM[ind[0]]
							elif ind[1] == "paternal grandfather":
								dad1_pos = d_aftTPM[ind[0]]
							elif ind[1] == "paternal grandmother":
								mom1_pos = d_aftTPM[ind[0]]
							elif ind[1] == "mother":
								 child2_pos = d_aftTPM[ind[0]]
							elif ind[1] == "maternal grandfather":
								dad2_pos = d_aftTPM[ind[0]]
							elif ind[1] == "maternal grandmother":
								mom2_pos = d_aftTPM[ind[0]]
						elif each == "1463":
							if ind[1] == "mother":
								child_pos = d_aftTPM[ind[0]]
							elif ind[1] == "maternal grandfather":
								dad_pos = d_aftTPM[ind[0]]
							elif ind[1] == "maternal grandmother":
								mom_pos = d_aftTPM[ind[0]]
						else:
							if ind[1] == "child":
								child_pos = d_aftTPM[ind[0]]
							elif ind[1] == "father":
								dad_pos = d_aftTPM[ind[0]]
							elif ind[1] == "mother":
								mom_pos = d_aftTPM[ind[0]]
				
					if each == "1459":
						inheritance([dad1_pos,mom1_pos],child1_pos,"paternal_",each,output)
						inheritance([dad2_pos,mom2_pos],child2_pos,"maternal_",each,output)
					else:		
						inheritance([dad_pos,mom_pos],child_pos,"",each,output)

			for each in output.keys():
				if output[each][1] == 0:
					add_in_final(final_output,each,["0.0",str(output[each][1])])	
				else:
					add_in_final(final_output,each,[str("%.1f")%(output[each][0]*100.0/output[each][1]),str(output[each][1])])

	sorted_ID = sorted(final_output.keys())
	#print sorted_ID
	out_pos.write("\n")
	for each in sorted_ID:
		out_pos.write(each[0]+"\t"+each[1]+"\t"+"\t".join(final_output[each])+"\n")
	out_pos.close()


