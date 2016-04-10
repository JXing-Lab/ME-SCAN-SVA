#!/usr/bin/python

import subprocess as sp

ls = sp.Popen(['ls', '-l', '/lab01/Projects/MEScan/Analysis_SVA_Mar022015'],stdout=sp.PIPE)
p2 = sp.Popen(['awk',r'{print $9}'],stdin=ls.stdout,stdout=sp.PIPE)
p3 = sp.Popen('grep Sample'.split(),stdin=p2.stdout,stdout=sp.PIPE)
p4 = sp.Popen(['awk','-F',r"_",r'$1=="Sample"{print $2}'],stdin=p3.stdout,stdout=sp.PIPE)
i = p4.communicate()[0].strip().split("\n")
print i, len(i)

def add_in_dict(d,key,li):
	if key not in d.keys():
		d[key] = [li]
	else:
		d[key].append(li)

window = 1000
type = ""
for k in range(0,2,1):
	if k==0:
		type = "minus"
	else:
		type = "plus"
	file_out_name = "All_inds_flexible_%ibp_%s_insert_loci.txt"%(window,type)
	out = open("/home/juiwan/analysis_SVA_output_Jan16/windowSize_candidate/%s"%file_out_name,"w")
	dict = {}		#chr as key, [[futher_from_ins,closer_from_ins,num_read,s]] as value
	dict_rep = {}		#locus as key, [[chr,futher_from_ins,closer_from_ins,num_read,s]] as value

	for s in i:
		print s
		fh = open ("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/Sample_"+s+"/"+s+"_R2.mapping_%s.29.48.48.500.repeatcover_off.flexible.temp"%type,"r")
		read = fh.readlines()
		fh.close()
		for row in read:
			row=row.strip().split("\t")
			add_in_dict(dict,row[0],[row[1],row[2],row[3],s])
	
	sorted_chr = []
	chr_list = []
	flagX = False
	flagY = False
	flagMT = False
	for x in dict.keys():
		if x!="chrMT" and x!="chrX" and x!="chrY":
			chr_list.append(x)
		elif x == "chrX":
			flagX = True
		elif x == "chrY":
			flagY = True
		elif x == "chrMT":
			flagMT = True
	sorted_chr=sorted(chr_list,key=lambda x:int(x[3:]))
	if flagMT:
		sorted_chr.insert(0,"chrMT")
	if flagX:
		sorted_chr.append("chrX")
	if flagY:
		sorted_chr.append("chrY")
	print sorted_chr
	
	
	print "start clustering"
	print "compare %s mapping"%type
	count = 0
	for chr in sorted_chr:
		count += 1
		locus = type+str(count)
		sorted_list = sorted(dict[chr],key=lambda x:int(x[1]))
		ref = sorted_list[0]
		add_in_dict(dict_rep,locus,[chr,ref[0],ref[1],ref[2],ref[3]])
		for curr in range(1,len(sorted_list),1):
			if int(sorted_list[curr][1]) >= int(ref[1]) and int(sorted_list[curr][1]) <= int(ref[1])+window: #(500bp library sequenced - 132bp (adapter sequence+6bp index)) * 2
				pass
			else:
				count += 1
				locus = type+str(count)
			ref = sorted_list[curr]
			add_in_dict(dict_rep,locus,[chr,ref[0],ref[1],ref[2],ref[3]])
	
	for each in dict_rep.keys():
		for pos in dict_rep[each]:
			out.write(pos[0]+" "+str(pos[1])+" "+str(pos[2])+" "+str(pos[3])+" "+pos[4]+" "+each+"\n")
	out.close()	
	
	q3 = sp.Popen(['cat','/home/juiwan/analysis_SVA_output_Jan16/windowSize_candidate/%s'%file_out_name],stdout=sp.PIPE)
	q4 = sp.Popen(['sort','-V','-k6,6','-k3,3'],stdin=q3.stdout,stdout=sp.PIPE)
	q5 = q4.communicate()[0].strip()
	
	out_sort = open("/home/juiwan/analysis_SVA_output_Jan16/windowSize_candidate/sorted_%s"%file_out_name,"w")
	out_sort.write(q5+"\n")
	out_sort.close()

	q6 = sp.Popen(['rm','/home/juiwan/analysis_SVA_output_Jan16/windowSize_candidate/%s'%file_out_name])

