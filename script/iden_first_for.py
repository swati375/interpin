import os,sys
import pickle

## program to extract the identified hairpin
def first_iden(hp,file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file
	ip=pickle.load(open(dir+'/forward/interop_add+.p',"rb"))
	hp_new={}
	if(len(ip)>0) and (len(hp)>0):
		for val in range(len(ip)):
			j=0
			while((int(hp[j][1])<=int(ip[val][2]))and j<(len(hp)-1)):
				if((int(hp[j][0])>=int(ip[val][1])) and(int(hp[j][1])<=int(ip[val][2]))):
					if val not in hp_new.keys():
						hp_new[val]=[hp[j]]
					else:
						hp_new[val].append(hp[j])
				j+=1

		hp_for={}
		c=0
		for i in range(len(ip)):
			if i in hp_new.keys():
				hp_for[i]=hp_new[i][0]
			else:
				c+=1
		print("forward")
		print("IR with no hp=",c)
		print("keys in iden=",len(hp_new.keys()))
		pickle.dump(hp_for,open(dir+'/forward/first_hpall_iden_forward.p',"wb"))
	

def single_hp(dir):
	hd=pickle.load(open(dir+'/d_grt15_iden_forward_all.p',"rb"))
	hp_for=[]
	for key in hd.keys():
		for ele in hd[key]:
			ele.append('d')
			if ele not in hp_for:
				hp_for.append(ele)
	return(hp_for)

def cluster_hp(dir):
	h=pickle.load(open(dir+'/cluster_iden_forward_all.p',"rb"))
	hp_for=[]
	for key in h.keys():
		for ele in h[key]:
			ele.append('c')
			if ele not in hp_for:
				hp_for.append(ele)
	return(hp_for)

def func_call_first_iden(file):
	di=os.getcwd()
	dir=di+"/../iden_hairpin/"+file+'/forward'
	hpc=cluster_hp(dir)
	hpd=single_hp(dir)
	hp_tot=hpc+hpd
	hp_tot=sorted(hp_tot)
	first_iden(hp_tot,file)

if __name__ == '__main__':
	func_call_first_iden(sys.argv[1])

