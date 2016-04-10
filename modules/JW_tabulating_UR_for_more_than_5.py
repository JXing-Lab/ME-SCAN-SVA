#!/usr/bin/python

for k in range(0,2,1):
	if k ==0:
		orient = "minus"
	else:
		orient = "plus"
	fh = open("/home/juiwan/analysis_SVA_output_Jan16/output_from_inheritance_stringent/More_than_5UR_0.5TPM_Novel_polymorphic_insertion_%s.SVA.29.65.65.500.repeatcover_off.flexible.BB.bed"%orient,"r")
	data = fh.readlines()
	fh.close()

	ur_list = []
	for row in data:
		row=row.strip().split()
		UR = row[5].split(",")
		for x in UR:
			ur_list.append(int(x))
	ur_list.sort()
	large = ur_list[-1]
	print large,orient

	category = [0 for x in range(large)]
	for each in ur_list:
		category[each-1]+=1

	out = open("/home/juiwan/analysis_SVA_output_Jan16/output_from_inheritance_stringent/category_More_than_5UR_0.5TPM_Novel_polymorphic_insertion_%s.txt"%orient,"w")
	out.write("number_of_UR\tcount\n")
	for x in range(0,len(category),1):
		if category[x] != 0:
			out.write(str(x+1)+"\t"+str(category[x])+"\n")
	out.close()

