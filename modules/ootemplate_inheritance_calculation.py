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
if filterType == 1:
	iden = "48.48"
	output_folder = "/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/output_from_inheritance_mild/"
elif filterType == 2:
	iden = "65.65"
	output_folder = "/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/analysis_SVA_output_Jan16/output_from_inheritance_stringent/"


print "To get the reference TPM cutoff for each ind"
fz = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/Results.29.%s.500.repeatcover_off.flexible./sensitivity_stuff/TPM_stats_90.txt"%iden,"r")
ref = fz.readlines()
fz.close()
ref_TPM = {}	#ind as key, reference_TPM as value
for row in ref:
	row=row.strip().split("\t")
	ref_TPM[row[1]]=row[0]

insert = ["Polymorphic","Novel_polymorphic"]
d_insert = {"Polymorphic":[0 for x in range(21)],"Novel_polymorphic":[0 for x in range(21)]} 	#count of loci vs count of ind
for fa in insert:
	print fa
	out_pos = open(output_folder+"%s_insertion_%s_variableTPM_and_UR_kid_inheritance.txt"%(fa,iden),"w")
	out_pos.write("ped_id\tinsertion_found_in")
	
	filterTPM = [0.5,1,2]
	filterUR = [x for x in range(22)]

	out_denovo = open(output_folder+"%s_%s_inheritance_calculation_error_rate.txt"%(iden,fa),"w")
	out_denovo.write("ped_id\tinsertion_found_in")
	final_denovo_output = {}	#(familyID,child) as key,[%_of_inheritance_error_rate,total_num_insertion_of_child,...] as value
		
	final_output = {}	 #(familyID,relation) as key,[%_of_inheritance_rate,total_num_insertion_of_that_ind,...] as value
	for f_TPM in filterTPM:
		for f_UR in filterUR:
			print f_TPM, f_UR
			out_denovo.write("\t%.1fTPM_>%iUR\ttotal_num_insertion"%(f_TPM,f_UR))
			denovo_output = {}	#(familyID,child) as key, [number_of_uniq_pos,number_of_child_insertion] as value
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
			
#				fh = open("/home/juiwan/analysis_SVA_output_Jan16/generating_list_of_fixed_insertion/%s_insertion_%s.SVA.29.48.48.500.repeatcover_off.flexible.BB.bed"%(fa,type),"r")
				fh = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/output_bwa-blast.29.%s.500.repeatcover_off.flexible./%s_insertion_%s.SVA.29.%s.500.repeatcover_off.flexible.BB.bed"%(iden,fa,type,iden),"r")
				data = fh.readlines()
				fh.close()

				#generating category of filter read for this filter				
				if f_TPM == 0.5 and f_UR == 5 and fa == "Novel_polymorphic":
					out_sp = open(output_folder+"More_than_5UR_0.5TPM_%s_insertion_%s.SVA.29.%s.500.repeatcover_off.flexible.BB.bed"%(fa,type,iden),"w")

				for row in data:
					row = row.strip().split("\t")
					ind_list = row[7].split(",")
					TPM_list = row[8].split(",")
					UR_list = row[9].split(",")
					temp_ind = []
					temp_TPM = []
					temp_UR = []
					for y in range(0,len(ind_list),1):
						if float(TPM_list[y]) >= (f_TPM*float(ref_TPM[ind_list[y]])) and int(UR_list[y]) > f_UR:
							d_aftTPM[ind_list[y]].append(row[0]+":"+row[1])
							if f_TPM == 0.5 and f_UR == 5 and fa == "Novel_polymorphic":
								temp_ind.append(ind_list[y])
								temp_TPM.append(TPM_list[y])
								temp_UR.append(UR_list[y])
					if len(temp_ind)!= 0:
						out_sp.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+",".join(temp_ind)+"\t"+",".join(temp_TPM)+"\t"+",".join(temp_UR)+"\n")

				if f_TPM == 0.5 and f_UR == 5 and fa == "Novel_polymorphic":
					out_sp.close()


				#generating inheritance error rate 
				child_list = []
				for familyID in d_trio_info.keys():
					if familyID == "1459" or familyID == "1463":
						for member in d_trio_info[familyID]:
							if member[1] == "father" or member[1] == "mother":
								child_list.append((member[0],member[1],familyID))
					else:
						for member in d_trio_info[familyID]:
							if member[1] == "child":
								child_list.append((member[0],member[1],familyID))
				for child in child_list:
					uniq_to_child = d_aftTPM[child[0]][:]
					for ind in d_aftTPM.keys():
						if child[0] == ind:
							continue
						else:
							overlap = list(set(d_aftTPM[child[0]])&set(d_aftTPM[ind]))
							uniq_to_child = list(set(uniq_to_child)-set(overlap))
					add_in_dict(denovo_output,child[2],child[1],len(d_aftTPM[child[0]]),len(uniq_to_child))


				#generating plot of histogram for this filter
				if f_TPM == 0.5 and f_UR == 2:
					print "doing count of loci vs individual count"
					d_temp_count = {}
					for each_ind in d_aftTPM.keys():
						for each_pos in d_aftTPM[each_ind]:
							if each_pos not in d_temp_count.keys():
								d_temp_count[each_pos] = 1
							else:
								d_temp_count[each_pos]+=1
					for key in d_temp_count.keys():
						d_insert[fa][d_temp_count[key]-1] += 1

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

			for each in denovo_output.keys():
				if denovo_output[each][1] == 0:
					add_in_final(final_denovo_output,each,["0.0",str(denovo_output[each][1])])
				else:
					add_in_final(final_denovo_output,each,[str("%.1f")%(denovo_output[each][0]*100.0/denovo_output[each][1]),str(denovo_output[each][1])])
	sorted_ID = sorted(final_output.keys())
	#print sorted_ID
	out_pos.write("\n")
	for each in sorted_ID:
		out_pos.write(each[0]+"\t"+each[1]+"\t"+"\t".join(final_output[each])+"\n")
	out_pos.close()

	out_denovo.write("\n")
	sorted_denovo_ID = sorted(final_denovo_output.keys())
	for each in sorted_denovo_ID:
		out_denovo.write(each[0]+"\t"+each[1]+"\t"+"\t".join(final_denovo_output[each])+"\n")
	out_denovo.close()

print "generating loci count plot for all 21 individuals"
N = 21
ind = np.arange(N)  # the x locations for the groups
width = 0.45       # the width of the bars
fig, ax = plt.subplots()
poly = d_insert["Polymorphic"]
rects1 = ax.bar(ind, poly, width, color='r')
rects2 = ax.bar(ind+width, d_insert["Novel_polymorphic"], width, color='y')

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of loci')
ax.set_xlabel('Number of individual')
ax.set_title('Count of loci group by polymorphic and novel polymorphic')
ax.set_xticks(ind + width)
ax.set_xticklabels([x+1 for x in range(21)])

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)
ax.legend((rects1[0], rects2[0]), ('Polymorphic', 'Novel_polymorphic'))
fig.set_size_inches(22.5, 10.5, forward=True)
fig.savefig(output_folder+'%s_count_loci_group_poly_and_novel_poly.png'%iden)
plt.close(fig)
