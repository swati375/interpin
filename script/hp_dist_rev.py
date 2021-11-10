import pickle
import os
from itertools import combinations
import copy
from multiprocessing import Pool
from functools import reduce
import re
from operator import itemgetter, attrgetter


def merge(a, b):
    while True:
        try:
            idx = b.index(a[-1]) + 1  # leftmost occurrence of a[-1] in b
        except ValueError:  # a[-1] not in b
            return 0
        if a[-idx:] == b[:idx]:
            return a + b[idx:]
        else:
        	return 0

def recur_merge(pn):
	p=[]
	i=0
	while i<len(pn):
		c=0
		j=i+1
		if(j<len(pn)):
			while(j<len(pn)):
				res=merge(pn[i],pn[j])
				if(res):
					if res not in p:
						p.append(res)
					pn.remove(pn[j])
					j=j-1
					c=1
				j+=1
		if(c==0) and (i<len(pn)):
			p.append(pn[i])
		i+=1
	p=sorted(p)
	return(p)

def call_merge(dn):
	pn=[]
	l_dn=len(dn)
	l_pn=0
	while(l_dn!=l_pn):
		pn=recur_merge(dn)
		l_pn=len(pn)
		l_dn=len(dn)
		dn=copy.deepcopy(pn)
	return dn

def hp_dist_new(file):
	di=os.getcwd()
	loc=di+"/../iden_hairpin/"+file+'/reverse/'
	d=pickle.load(open(loc+"location_irhp.p","rb"))
	c=0
	df={}
	df_single={}
	for key in d.keys():
		ar=[]
		ar_d=[]
		if(c>-1):
			dn=list(combinations(d[key],2))
			d_new=[]
			visited=[]
			for var in dn:
				if((var[0][1]-var[1][0])<16) and ((var[0][1]-var[1][0])>0):
					d_new.append(list(var))
	## for all d_grt hp
			if(len(d_new)>0):
				for var in d_new:
					for val in var:
						if(val not in ar_d):
							ar_d.append(val)
				d_dkey=reduce(lambda l, x: l if x in l else l+[x], d[key], [])
				df_single[key]=[x for x in d_dkey if x not in ar_d]
				df_single[key]=sorted(df_single[key],reverse=True)
				if len(df_single[key])==0:
					del(df_single[key])
			elif((len(d_new)==0) and (len(d[key])>0)):
				df_single[key]=sorted(d[key],reverse=True)
	
			dn=[]
			d_copy=copy.deepcopy(d_new)
			d_new=sorted(d_new)
			if(len(d_new)>0):
				for i in range(len(d_new)):
					i_check=0
					j=i+1
					if(j<len(d_new)):
						p=1
						while p:
							dist=d_new[i][1][1]-d_new[j][0][0]
							if(dist>16) or (j==len(d_new)-1):
								p=0
							if(dist<16) and (dist>0):
								i_check=1
								dn.append(d_new[i]+d_new[j])
								
								if(d_new[i] not in visited):
									visited.append(d_new[i])
									visited.append([d_new[i][1],d_new[j][0]])
							j+=1
							if(j>=len(d_new)):
								p=0
						if(i_check==0):
							if d_new[i] not in dn:
								dn.append(d_new[i])
				dn.append(d_new[i])
				del d_new
				d_indx=[]
				for var in dn:
					vn=[]
					for v in var:
						vn.append(d[key].index(v))
					d_indx.append(vn)
					d_indx=sorted(d_indx)
				if(d_copy==dn):
					ar=dn
				else:
					ar=call_merge(d_indx)
					dn=[]
					for var in ar:
						vn =[]
						for v in var:
							vn.append(d[key][v])
						dn.append(vn)
					ar=dn
		c+=1
		if(len(ar)>0):
			df[key]=ar
	
	pickle.dump(df,open(loc+'dcluster.p',"wb"))
	pickle.dump(df_single,open(loc+'dsingle.p',"wb"))
	

def mfold_dict(file):
	di=os.getcwd()
	d={}
	dir=di+"/../complete_hpin/";
	
#### forming mfold for all hairpins dictionary
	with open(dir+'reverse_'+file,'r') as f:
		for line in f:
			en=re.compile('\s+GI=(\w+).*')
			if en.match(line):
				gi=en.match(line).group(1)
				continue
			
			en=re.compile('(\-?\d+)\s+(\-?\d+)\s+(\w+)\((\w+)\)(\w+)\s+(\d+)\s+(\-?\d+\.\d+)')
			entry=[]
			if en.match(line):
				entry.append(int(en.match(line).group(1)))
				entry.append(int(en.match(line).group(2)))
				entry.append(en.match(line).group(3))
				entry.append(en.match(line).group(4))
				entry.append(en.match(line).group(5))
				entry.append(int(en.match(line).group(6)))
				entry.append(float(en.match(line).group(7)))
				if gi in d:
					if entry in d[gi]:
						continue
					else:
						d[gi].append(entry)
				else:
					d[gi]=[entry]
	
#### sorting hairpins for each gene
	d_new={}
	sum=0
	for key in d.keys():
		sum+=len(d[key])
		d_new[key]=sorted(d[key],key=itemgetter(0))

	pickle.dump(d_new,open(di+"/../iden_hairpin/"+file+"/reverse/d1.p", "wb"))