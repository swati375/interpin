import pickle
import os,sys
#from matplotlib import pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.cluster import KMeans,MiniBatchKMeans,DBSCAN
from sklearn.preprocessing import StandardScaler


def hp_stemloop_filter(hp_all,strand,dir):
	stem=[]
	loop=[]
	hp={}
	id=[]
	c_old=c_extra=0
	for key in hp_all.keys():
		for p,ele in enumerate(hp_all[key]):
			c_old+=1
			if(len(ele[2])==len(ele[4])):
				if key in hp.keys():
					hp[key].append(ele)
				else:
					hp[key]=[ele]
				stem.append(len(ele[2]))
				loop.append(len(ele[3]))
				id.append([p,key])
			else:
				c_extra+=1
	X=[[stem[i],loop[i]] for i in range(len(stem))]

	# using volume based filtering: 5% outliers in volume- mainly from tail of distribution, are removed
	freq,xedge,yedge=np.histogram2d(stem,loop,bins=[15,10])
	x=xedge[1]-xedge[0]
	y=yedge[1]-yedge[0]
	vol=[[0 for i in range(10)] for j in range(15)]
	for i in range(15):
		for j in range(10):
			vol[i][j]=[round(x*y*freq[i][j],2),i,j]
	sum1=0
	vol_grid=[]
	for ele in vol:
		temp=[val[0] for val in ele]
		sum1+=sum(temp)
		for val in ele:
			vol_grid.append(val)
	sum_95=round(sum1*0.95,2)
	sum_98=round(sum1*0.98,2)
	vol_grid.sort(key = lambda x: x[0],reverse=True)
	sum2=0
	vol_in=[]
	vol_out=[] 
	for ele in vol_grid:
		sum2+=ele[0]
		if(sum2>sum_95):
			break
		else:
			vol_in.append(ele)

	hp_new={}
	out=0
	for key in hp.keys():
		for ele in hp[key]:
			pre=0
			for var in vol_in:
				stem1=xedge[var[1]]
				stem2=xedge[var[1]+1]
				loop1=yedge[var[2]]
				loop2=yedge[var[2]+1]
				if((len(ele[2])>=stem1) and (len(ele[2])<stem2) and (len(ele[3])>=loop1) and (len(ele[3])<loop2)):
					pre=1
					if key in hp_new.keys():
						hp_new[key].append(ele)
					else:
						hp_new[key]=[ele]
			if(pre!=1):
				out+=1

	stem=[]
	loop=[]
	for key in hp_new.keys():
		for var in hp_new[key]:
			stem.append(len(var[2]))
			loop.append(len(var[3]))
	pickle.dump(hp_new,open(dir+'outlier_removed_d1.p',"wb"))



def call_outlierhp_remove(file,strand):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file+'/'+strand+'/'
	hp_all=pickle.load(open(dir+'d1.p',"rb"))
	hp_stemloop_filter(hp_all,strand,dir)
	
