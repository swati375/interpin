import os,sys
import re
import pickle
from multiprocessing import Pool

## identify and filter the hpclusters that lie in interoperonic region
def hpinterop_clusterwise(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file+'/reverse'
	st1=[]
	stp1=[]
	enr1=[]
	d=pickle.load(open(dir+'/dcluster.p',"rb"))
	sum=0
	for key in d.keys():
		sum+=len(d[key])
		temp=[x for x in d[key] if len(x)==2]
		rem=[]
		for var in temp:
			for v in d[key]:
				if len(v)>2:
					te=[x for x in var if x not in v]
					if(len(te)==0):
						rem.append(var)
						break
		d[key]=[x for x in d[key] if x not in rem]

	for key in d.keys():
		for val in d[key]:
			num=len(val)
			st=val[0][0]
			stp=val[num-1][1]
			enr=0
			for var in val:
				enr+=var[6]
			enr=enr/num
			st1.append(st)
			stp1.append(stp)
			enr1.append(enr)
	hpi=[]
	c_up=0
	op=pickle.load(open(dir+'/interop_add-.p',"rb"))
	for i in range(len(st1)):
		for j in range(len(op)):
			if((st1[i]<=int(op[j][1])) and(stp1[i]>=int(op[j][2]))):
				v=[]
				v.append(st1[i])
				v.append(stp1[i])
				v.append(enr1[i])
				if(int(op[j][1])-st1[i])<300: # in locationcluster program all hp at <300
					if v not in hpi:
						hpi.append(v)
				else:
					c_up+=1
				break
	pickle.dump(hpi,open(dir+'/hpcluster_interop.p',"wb"))
	hpinterop_dgrt15(file)

def hpinterop_dgrt15(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file+'/reverse'
	lis = os.listdir(dir)
	hpi=[]
	c_up=0
	d=pickle.load(open(dir+'/dsingle.p',"rb"))
	sum=0
	for key in d.keys():
		sum+=len(d[key])
	op=pickle.load(open(dir+'/interop_add-.p',"rb"))
	for key in d.keys():
		for val in d[key]:
			for j in range(len(op)):
				if(val[0]<int(op[j][2])):
					break
				elif((val[0]<=int(op[j][1])) and (val[1]>=int(op[j][2]))):
					v=[]
					v.append(val[0])
					v.append(val[1])
					v.append(float(val[6]))
					if v not in hpi:
						if(int(op[j][1])-val[0])<300:  # >300 coming in cases where the stop of gene by ncbi doesnt match operon stop by molquest
							hpi.append(v)
						else:
							c_up+=1
							
	pickle.dump(hpi,open(dir+'/hp_interopd_grt15.p',"wb"))

if __name__ == '__main__':
	hpinterop_clusterwise(sys.argv[1])

