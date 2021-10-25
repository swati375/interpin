import os
import sys
import pickle
from multiprocessing import Pool

#program to add missing genes from gbk files to IR files (genes/operons not detected by molquest).

def missing_cds(org):
	di=os.getcwd()
	dir=di+"/../genomes/"+org+'/fasta_op'
	cds_for=pickle.load(open(dir+'/forward_ststp.p',"rb"))
	dir1=di+"/../iden_hairpin/"+org
	dir2=dir1+'/forward/'
	op=pickle.load(open(dir2+'interop+.p',"rb"))
	intop=[]
	for var in op:
		intop.append([int(var[0]),int(var[1]),int(var[2])])
	intop=sorted(intop)
	if (len(intop)>0) and (len(cds_for)>0):
		for var in cds_for:
			j=0
			while(var[1]>int(intop[j][0])) and (j<len(intop)-1):
				if(var[0]>int(intop[j][1])) and (var[1]<int(intop[j][2])):
					v=intop[j]
					intop.remove(v)
					intop.append([int(v[0]),int(v[1]),var[0]])
					intop.append([var[0],var[1],int(v[2])])
				j+=1
	elif (len(intop)==0) and (len(cds_for)>0):
		for i,var in enumerate(cds_for[0:-1]):
			if int(var[1])<int(cds_for[i+1][0]):
				intop.append([int(var[0]),int(var[1]),int(cds_for[i+1][0])])
		intop.append([int(cds_for[-1][0]),int(cds_for[-1][1]),int(cds_for[-1][1])+270])
		intop=sorted(intop)
	# print("forward transcription units=",len(intop))
	pickle.dump(intop,open(dir2+'interop_add+.p',"wb"))

	cds_rev=pickle.load(open(dir+'/reverse_ststp.p',"rb"))
	dir2=dir1+'/reverse/'
	op=pickle.load(open(dir2+'interop-.p',"rb"))
	intop=[]
	for var in op:
		intop.append([int(var[0]),int(var[1]),int(var[2])])
	intop=sorted(intop)
	if (len(intop)>0) and (len(cds_rev)>0):
		for var in cds_rev:
			j=0
			while(var[1]>int(intop[j][2])) and (j<len(intop)-1):
				if(var[0]>int(intop[j][2])) and (var[1]<int(intop[j][1])):
					v=intop[j]
					intop.remove(v)
					intop.append([var[1],var[0],int(v[2])])
					intop.append([int(v[0]),int(v[1]),var[1]])
				j+=1
	
	elif (len(intop)==0) and (len(cds_rev)>0):
		for i in range(1,len(cds_rev)):
			intop.append([int(cds_rev[i][1]),int(cds_rev[i][0]),int(cds_rev[i-1][1])])
		if(cds_rev[0][0]-270>0):
			intop.append([int(cds_rev[0][1]),int(cds_rev[0][0]),int(cds_rev[0][0]-270)])
		else:
			intop.append([int(cds_rev[0][1]),int(cds_rev[0][0]),0])
			
		intop=sorted(intop)
	# print("reverse transcription units=",len(intop))#,len(op_dict))
	pickle.dump(intop,open(dir2+'interop_add-.p',"wb"))
	
