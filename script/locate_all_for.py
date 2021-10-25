import pickle
import os,sys
from multiprocessing import Pool

## priogram to find the location of hairpins on the genome (earlier wrt input sequence). 

def locatehp(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file+'/forward'
	loc_file=pickle.load(open(dir+'/interop_add+.p',"rb"))
	gi_all=list(range(len(loc_file)))
	d1=pickle.load(open(dir+'/outlier_removed_d1.p',"rb"))
	sum1=0
	for key in d1.keys():
		sum1+=len(d1[key])
	dn={}
	for key in d1.keys():
		ke=int(key)
		c=1
		if(ke in gi_all):
			indx=gi_all.index(ke)
			c=0
			for var in d1[key]:
				v=[]
				st=var[0]+int(loc_file[indx][1])
				stp=var[1]+int(loc_file[indx][1])
				v.append(st)
				v.append(stp)
				v.append(var[2])
				v.append(var[3])
				v.append(var[4])
				v.append(var[5])
				v.append(float(var[6]))
				if ke in dn:
					if v in dn[ke]:
						continue
					else:
						dn[ke].append(v)
				else:
					dn[ke]=[v]
		if(c==1):
			next
	sum=0
	for key in dn.keys():
		sum+=len(dn[key])
		dn[key]=sorted(dn[key])
	pickle.dump(dn,open(dir+'/location_allhp.p',"wb"))
	in_ir(file)

def in_ir(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file+'/forward'
	op=pickle.load(open(dir+'/interop_add+.p',"rb"))
	df=pickle.load(open(dir+'/location_allhp.p',"rb"))
	data={}
	for key in df.keys():
		for ele in df[key]:
			j=0
			while((ele[1]>int(op[j][1])) and (j<len(op)-1)):
				if(ele[0]>=int(op[j][1])) and (ele[1]<=int(op[j][2])):
					if key in data.keys():
						data[key].append(ele)
					else:
						data[key]=[ele]
				j+=1
	if(len(op)==1) and (len(df.keys())==1):
		for key in df.keys():
			for ele in df[key]:
				if(ele[0]>=int(op[0][1])) and (ele[1]<=int(op[0][2])):
					if key in data.keys():
						data[key].append(ele)
					else:
						data[key]=[ele]

	sum=0
	for key in data.keys():
		sum+=len(data[key])
	print('hp in IR for=',len(data.keys()))
	pickle.dump(data,open(dir+'/location_irhp.p',"wb"))
	
