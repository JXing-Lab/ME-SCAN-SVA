#!/usr/bin/python

fk = open("/home/juiwan/analysis_SVA_output/library_81_107_info_trio.txt","r")
info = fk.readlines()
fk.close()

d_trio_info = {}	# family id as key, (ind,relationship) as value
d_befTPM = {}             # ind as key, insertion pos as value
d_aftTPM = {}
for row in info:
	row=row.strip().split("\t")
	d_befTPM[row[1]] = []
	d_aftTPM[row[1]] = []
	if row[3] not in d_trio_info.keys():
		d_trio_info[row[3]]=[(row[1],row[4])]
	else:
		d_trio_info[row[3]].append((row[1],row[4]))
#print d_trio_info

fh = open("/home/juiwan/analysis_SVA_output/strigent_and_TPMcutoff_SVA.txt","r")
data = fh.readlines()[1:]
fh.close()

for row in data:
	row = row.strip().split("\t")
	ind_befTPM = row[6].strip("\"\"").split(",")
	for x in ind_befTPM:
		d_befTPM[x].append(row[0]+":"+row[1])
	ind_aftTPM = row[8].strip("\"\"").split(",")
	for y in ind_aftTPM:
		d_aftTPM[y].append(row[0]+":"+row[1])

out = open("/home/juiwan/analysis_SVA_output/out_inheritance.txt","w")
out.write("ped_id\tind_id\trelationship\tnum_of_insertion_beforeTPM\tnum_of_insertion_afterTPM\n")
for each in d_trio_info.keys():
	for ind in d_trio_info[each]:
		out.write(each+"\t"+ind[0]+"\t"+ind[1]+"\t"+str(len(d_befTPM[ind[0]]))+"\t"+str(len(d_aftTPM[ind[0]]))+"\n")
out.close()

type = ""
for k in range(0,2,1):
	if k == 0:
		type = "befTPM"
		temp_d = d_befTPM
	else:
		type = "aftTPM"
		temp_d = d_aftTPM
	out_pos = open("/home/juiwan/analysis_SVA_output/kid_inheritance_%s.txt"%(type),"w")
	out_pos.write("ped_id\tinsertion_found_in\tlist_of_position\n")
	for each in d_trio_info.keys():
		for ind in d_trio_info[each]:
			if each == "1459":
				if ind[1] == "father":
					 child1_pos = temp_d[ind[0]]
				elif ind[1] == "paternal grandfather":
					dad1_pos = temp_d[ind[0]]
				elif ind[1] == "paternal grandmother":
					mom1_pos = temp_d[ind[0]]
				elif ind[1] == "mother":
					 child2_pos = temp_d[ind[0]]
				elif ind[1] == "maternal grandfather":
					dad2_pos = temp_d[ind[0]]
				elif ind[1] == "maternal grandmother":
					mom2_pos = temp_d[ind[0]]
			elif each == "1463":
				if ind[1] == "mother":
					child_pos = temp_d[ind[0]]
				elif ind[1] == "maternal father":
					dad_pos = temp_d[ind[0]]
				elif ind[1] == "maternal mother":
					mom_pos = temp_d[ind[0]]
			else:
				if ind[1] == "child":
					child_pos = temp_d[ind[0]]
				elif ind[1] == "father":
					dad_pos = temp_d[ind[0]]
				elif ind[1] == "mother":
					mom_pos = temp_d[ind[0]]
		if each == "1459":
			inherit1 = [dad1_pos,mom1_pos]
			for x in range(0,len(inherit1),1):
				inherit_from_parent = list(set(inherit1[x])&set(child1_pos))
				relation = ""
				if x == 0:
					relation = "paternal_father"
				else:
					relation = "paternal_mother"
				out_pos.write(each+"\t"+relation+"\t"+",".join(inherit_from_parent)+"\n")
			none1 = list(set(child1_pos)-set(dad1_pos)-set(mom1_pos))
			out_pos.write(each+"\tnone\t"+",".join(none1)+"\n")
			
			inherit2 = [dad2_pos,mom2_pos]
			for x in range(0,len(inherit2),1):
				inherit_from_parent = list(set(inherit2[x])&set(child2_pos))
				relation = ""
				if x == 0:
					relation = "maternal_father"
				else:
					relation = "maternal_mother"
				out_pos.write(each+"\t"+relation+"\t"+",".join(inherit_from_parent)+"\n")
			none2 = list(set(child2_pos)-set(dad2_pos)-set(mom2_pos))
			out_pos.write(each+"\tnone\t"+",".join(none2)+"\n")
		else:		
			inherit = [dad_pos,mom_pos]
			for x in range(0,len(inherit),1):
				inherit_from_parent = list(set(inherit[x])&set(child_pos))
				relation = ""
				if x == 0:
					relation = "father"
				else:
					relation = "mother"
				out_pos.write(each+"\t"+relation+"\t"+",".join(inherit_from_parent)+"\n")
			none = list(set(child_pos)-set(dad_pos)-set(mom_pos))
			out_pos.write(each+"\tnone\t"+",".join(none)+"\n")
	out_pos.close()
