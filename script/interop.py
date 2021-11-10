import numpy as np
import os
import re
import pickle 
from multiprocessing import Pool


#program to extract interoperonic regions from molquest predictions. operons on both strands are separated.
def interop(org):
	di=os.getcwd()
	dir2=di+"/../genomes/"+org+'/'
	os.system("mkdir "+di+"/../iden_hairpin/"+org)
	dir1=di+"/../iden_hairpin/"+org
	with open(dir2+'result.txt','r')as file3:
		op=[]
		opnum=0
		for line in file3 :
			en=re.compile('.*\s(\d+)\s\w.*(\+|\-).*\s(\d+)\s\-\s+(\d+).*')
			if en.match(line):
				op.append(en.match(line).groups())
	pickle.dump(op, open(dir1+"/op.p", "wb"))
	# print('done op')

def interop2(org):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+org
	op1=pickle.load(open(dir+'/op.p',"rb"))
	op_dict={}	
	op=[]
	opnum=sign=st=stp=0
	al=[]
	for lis in op1:
		al=[]
		if(lis[0] == opnum):
			stp=lis[3]
			if key in op_dict.keys():
				op_dict[key].append([int(lis[2]),int(lis[3])])
			else:
				op_dict[key]=[[int(lis[2]),int(lis[3])]]
		else:
			if(int(opnum)>0):
				al.append(opnum)
				al.append(sign)
				al.append(st)
				al.append(stp)
			op.append(al)
			opnum=lis[0]
			sign=lis[1]
			st=lis[2]
			stp=lis[3]
			key=opnum+sign
			if key in op_dict.keys():
				op_dict[key].append([int(lis[2]),int(lis[3])])
			else:
				op_dict[key]=[[int(lis[2]),int(lis[3])]] 
	al=[]
	al.append(opnum)
	al.append(sign)
	al.append(st)
	al.append(stp)
	op.append(al)
	pickle.dump(op_dict,open(dir+'/op_dict.p',"wb"))
	pickle.dump(op, open(dir+"/op2.p", "wb"))

def sign_separate_interop(org):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+org
	op2=pickle.load(open(dir+'/op2.p',"rb"))
	op2.pop(0)
	cp=0
	c=0
	opp=[]
	op=[]
	opall=[]
	for l in op2:
		if(l[1] == '+'):
			if(cp==0):
				st_p=l[2]
				stinterp=l[3]
				cp=cp+1
			else:
				al=[]
				stpinterp=l[2]
				al.append(st_p)
				al.append(stinterp)
				al.append(stpinterp)
				opp.append(al)
				st_p=l[2]
				stinterp=l[3]
				opall.append(al)
		else:
			if(c==0):
				stpinter=1
				st=l[3]
				stinter=l[2]
				c=c+1
			else:
				al=[]
				al.append(st)
				al.append(stinter)
				al.append(stpinter)
				op.append(al)
				stpinter=st
				st=l[3]
				stinter=l[2]
				opall.append(al)
	
	if 'st' in locals():
		op.append([st,stinter,str(int(stinter)-270)])
	os.system("mkdir "+dir+"/reverse")
	pickle.dump(op, open(dir+"/reverse/interop-.p", "wb"))

	if 'st_p' in locals():
		opp.append([st_p,stinterp,str(int(stinterp)+270)])
	os.system("mkdir "+dir+"/forward")
	pickle.dump(opp, open(dir+"/forward/interop+.p", "wb"))
	



