#!/usr/bin/python

def add_in_dict(output,each,relation,num,length):
	if (each,relation) not in output.keys():
		output[(each,relation)] = [num,length]
	else:
		output[(each,relation)][0] += num
		output[(each,relation)][1] += length

def inheritance(parent_list,child_list,rel,each,output):
	for x in range(0,len(parent_list),1):
		inherit_from_parent = list(set(parent_list[x])&set(child_list))
		relation=""
		if x == 0:
			relation = rel+"father"
		else:
			relation = rel+"mother"
		print each,relation,len(inherit_from_parent),len(child_list)
		add_in_dict(output,each,relation,len(inherit_from_parent),len(child_list))
	none = list(set(child_list)-set(parent_list[0])-set(parent_list[1]))
	print each,rel+"none",len(none),len(child_list)
	add_in_dict(output,each,rel+"none",len(none),len(child_list))

fk = open("/home/juiwan/analysis_SVA_output_Jan16/library_81_107_info_trio.txt","r")
info = fk.readlines()
fk.close()

d_trio_info = {}	# family id as key, (ind,relationship) as value
for row in info:
	row=row.strip().split("\t")
	if row[3] not in d_trio_info.keys():
		d_trio_info[row[3]]=[(row[1],row[4])]
	else:
		d_trio_info[row[3]].append((row[1],row[4]))
print d_trio_info

output = {}	#(familyID,relation) as key, [number_of_inheritance,length_of_child_pos] as value
out_pos = open("/home/juiwan/analysis_SVA_output_Jan16/novel_polymorphic_insertion_kid_inheritance.txt","w")
out_pos.write("ped_id\tinsertion_found_in\t%_of_inheritance\n")
for k in range(0,2,1):
	if k==0:
		type = "minus"
	else:
		type = "plus"
	print type
	
	d_aftTPM = {}		# ind as key, insertion pos as value
	for row in info:
		row=row.strip().split("\t")
		d_aftTPM[row[1]] = []

	fh = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/output_bwa-blast.29.48.48.500.repeatcover_off.flexible./Novel_polymorphic_insertion_%s.SVA.29.48.48.500.repeatcover_off.flexible.TPM4.2.BB.bed"%type,"r")
	data = fh.readlines()
	fh.close()
	
	for row in data:
		row = row.strip().split("\t")
		ind_list = row[7].split(",")
		TPM_list = row[8].split(",")
		UR_list = row[9].split(",")
		for y in ind_list:
			d_aftTPM[y].append(row[0]+":"+row[1])

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
				elif ind[1] == "maternal father":
					dad_pos = d_aftTPM[ind[0]]
				elif ind[1] == "maternal mother":
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

sorted_ID = sorted(output.keys())
#print sorted_ID
for each in sorted_ID:
	if output[each][1] == 0:
		out_pos.write(each[0]+"\t"+each[1]+"\t0.0\n")
	else:
		out_pos.write(each[0]+"\t"+each[1]+"\t%.1f\n"%(output[each][0]*100.0/output[each][1]))
out_pos.close()
