import pickle
import multiprocessing
from multiprocessing import Pool
#from matplotlib import pyplot as plt
import numpy as np
import os,sys
import re

z=[]

def enr_clstr(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file
	lis1=['forward','reverse']
	for nm in lis1:
		dir1=dir+'/'+nm
		lis=os.listdir(dir)
		fil_btw=pickle.load(open(dir1+'/hpcluster_interop.p',"rb"))
		b=[]
		for var in fil_btw:
			if var[:3] in b:
				print("exit")
				exit()
			else:
				b.append(var[:3])
		fil_btw=sorted(b)
		hp_btw={}
		rep=[]
		total=0
		fil=pickle.load(open(dir1+'/dcluster.p',"rb"))
		for key in fil.keys():
			for val in fil[key]:
				n=len(val)
				v=[]
				st=val[0][0]
				stp=val[n-1][1]
				v.append(st)
				v.append(stp)
				e=0
				for num in val:
					e+=num[6]
				e=e/n
				v.append(e)
				if v not in rep:
					if (v in fil_btw):
						if key in hp_btw.keys():
							if v not in hp_btw[key]:
								hp_btw[key].append(v)
								rep.append(v)
								total+=n
						else:
							hp_btw[key]=[v]
							rep.append(v)
							total+=n
		l=0
		for key in hp_btw.keys():
			l+=len(hp_btw[key])
		pickle.dump(hp_btw,open(dir1+'/cluster_iden_'+nm+'_all.p',"wb"))
			
def enr_dgrt15_all(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file
	lis1=['forward','reverse']
	for nm in lis1:
		dir1=dir+'/'+nm
		fil_btw=pickle.load(open(dir1+'/hp_interopd_grt15.p',"rb"))
		b=[]
		for var in fil_btw:
			if var[:3] in b:
				exit()
			else:
				b.append(var[:3])
		fil_btw=sorted(b)
		hp_btw={}
		rep=[]
		fil=pickle.load(open(dir1+'/dsingle.p',"rb"))
		for key in fil.keys():
			for val in fil[key]:
				v=[]
				st=val[0]
				stp=val[1]
				v.append(st)
				v.append(stp)
				v.append(val[6])
				if v not in rep:
					if (v in fil_btw):
						if key in hp_btw.keys():
							if ((v not in hp_btw[key])):
								hp_btw[key].append(v)
								rep.append(v)
						else:
							hp_btw[key]=[v]
							rep.append(v)
		l=0
		rep=sorted(rep)
		for key in hp_btw.keys():
			l+=len(hp_btw[key])

		# print(nm,"single hp identified with multiple for a operon=",l)#,len(rep))
		pickle.dump(hp_btw,open(dir1+'/d_grt15_iden_'+nm+'_all.p',"wb"))
				
	enr_clstr(file)


if __name__ == '__main__':
	enr_dgrt15_all(sys.argv[1])

