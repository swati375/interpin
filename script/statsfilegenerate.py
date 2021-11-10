import os,sys
import pickle
import random
import numpy as np

def make_table(org):
	di=os.getcwd()
	dir2=di+'/../genomes/'
	dir=di+'/../iden_hairpin/'
	lis_d=os.listdir(dir+org)
	if ('forward' in lis_d) and ('reverse' in lis_d):
		lis=['forward','reverse']
	elif ('forward' in lis_d):
		lis=['forward']
	elif ('reverse' in lis_d):
		lis=['reverse']
	else:
		lis=['no strand']
	if 'no strand' not in lis:
		hp_all=[]
		found=0
		for nm in lis:
			dir1=dir+org+'/'+nm
			hp=[]
			hp_done=[]
			key_done=[]
			key_hp=[]
			found=0
			if ('forward' in nm) and ('first_hpall_iden_forward.p' in os.listdir(dir1)):
				op=pickle.load(open(dir+org+'/forward/interop_add+.p',"rb"))
				idenhp=pickle.load(open(dir+org+'/forward/first_hpall_iden_forward.p',"rb"))
				if len(idenhp.keys())>0:
					found=1
			elif ('reverse' in nm) and ('first_hpall_iden_reverse.p' in os.listdir(dir1)):
				op=pickle.load(open(dir+org+'/reverse/interop_add-.p',"rb"))
				idenhp=pickle.load(open(dir+org+'/reverse/first_hpall_iden_reverse.p',"rb"))
				if len(idenhp.keys())>0:
					found=1

			if found==1:
				for key in idenhp.keys():
					if(idenhp[key][3]=='c'):
						hp.append(idenhp[key][:3])
						key_hp.append(key)
					else:
						key_done.append(key)
						hp_all.append([op[key][0],op[key][1],idenhp[key][0],idenhp[key][1],idenhp[key][2],'single',1,nm])
					
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
						if (v in hp) and (v not in hp_done):
							ind=hp.index(v)
							if key_hp[ind] not in key_done:
								hp_done.append(v)
								temp=[op[key_hp[ind]][0],op[key_hp[ind]][1],idenhp[key_hp[ind]][0],idenhp[key_hp[ind]][1],idenhp[key_hp[ind]][2],'cluster',n,nm]
								hp_all.append(temp)
								key_done.append(key_hp[ind])
		if found==1:
			hp_all=sorted(hp_all)
			np.savetxt(dir+org+"/predictions.csv", hp_all, delimiter =", ", fmt ='% s')
			

# if __name__=='__main__':
# 	make_table('Acetoanaerobium_sticklandii_DSM_519')