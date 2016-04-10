#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import subprocess as sp

beg = sp.Popen(['pwd'],stdout=sp.PIPE)
location = beg.communicate()[0].strip()
#print location

f_b = open(location+"/parameter.txt","r")
sp_info = f_b.readlines()
f_b.close()

ME = sp_info[0].strip().split("=")[1]

filterType = input("Please enter the filter want: 1.mild or 2.stringent: ")
folder = ""
iden = ""
if filterType == 1:
	folder = "/lab01/Projects/MEScan/%s/juiwan/output_from_inheritance_mild/sensitivity/"%(ME)
	iden = sp_info[3].strip().split("=")[1]
elif filterType == 2:
	folder = "/lab01/Projects/MEScan/%s/juiwan/output_from_inheritance_stringent/sensitivity/"%(ME)
	iden = sp_info[4].strip().split("=")[1]

p1 = sp.Popen(['ls','%s'%folder],stdout=sp.PIPE)
input_files = p1.communicate()[0].strip().split("\n")
#print input_files

max_UR = 10
out = open(folder.split("sensitivity")[0]+"TPM_stats_90_maxUR_%i_%s.txt"%(max_UR,iden),"w")
out.write("individual_ID\tUR\tTPM\t%_sensitivity\n")

TPM_UR = {}
small = 100.0
for x in range(0,len(input_files),1):
	target_UR = 0
	flag_UR = False
	flag_TPM = False
	print input_files[x]
	ind = input_files[x].split("_")[0]
	fh = open(folder+input_files[x],"r")
	data = fh.readlines()
	fh.close()

	UR_list = data[0].strip().split("\t")
	del UR_list[0]
	del data[0]
	TPM_UR[ind] = np.random.rand(len(data),len(UR_list))
	for row in range(0,len(data),1):
		data[row]=data[row].strip().split("\t")
		del data[row][0]
		for col in range(0,len(data[row]),1):
			TPM_UR[ind][row,col]=data[row][col]
			if float(data[row][col]) < small:
				small = float(data[row][col])
			if ind != "overall" and ind != "average":
				if not flag_UR and col < max_UR+1 and float(data[row][col]) < 90:
					flag_UR = True
					if col != max_UR and row > 0:
						target_UR = max_UR-1
					else:
						target_UR = col-1
		if ind != "overall" and ind != "average" and not flag_TPM and flag_UR and float(data[row][target_UR]) < 90:
			flag_TPM = True
			out.write(ind+"\t%i\t%i\t%s\n"%(target_UR+1,row,data[row-1][target_UR]))
out.close()

print small

sorted_ID = sorted(TPM_UR.keys())
avg_ov = sorted_ID[-2:]
del sorted_ID[-2:]
print avg_ov
print sorted_ID

two_heatmap = [sorted_ID,avg_ov]
for loop in range(0,len(two_heatmap),1):
	count = 0
	fig = plt.figure()
	for each in two_heatmap[loop]:
		count += 1
		if loop == 0:
			ax1 = fig.add_subplot(7,3,count)
			size = ['%.2f',1.00]
		else:
			ax1 = fig.add_subplot(4,2,count)
			size = ['%.0f',1.02]
		heatmap = plt.pcolor(TPM_UR[each],vmin=int(small),vmax=100)
		for y in range(TPM_UR[each].shape[0]):
		    for x in range(TPM_UR[each].shape[1]):
		        plt.text(x + 0.5, y + 0.5, size[0] % TPM_UR[each][y,x],
		                 horizontalalignment='center',
		                 verticalalignment='center',
		                 )
		plt.colorbar(heatmap)
		plt.xlim(0,TPM_UR[each].shape[1])
		plt.ylim(0,TPM_UR[each].shape[0])
		ax1.set_title('%s'%each,fontsize=45,y=size[1])
		ax1.set_ylabel('TPM',fontsize = 30)
		ax1.set_xlabel('UR',fontsize = 30)
	
	if loop == 0:
		name = "individual"
		fig.set_size_inches(75, 75)
	else:
		name = "average_overall"
		fig.set_size_inches(25, 30)
	fig.savefig(folder.split("sensitivity")[0]+'heatmap_sensitivity_%s_analysis_%s.pdf'%(name,iden))
	plt.close(fig)
	
