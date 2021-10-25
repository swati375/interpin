import numpy as np
from matplotlib import pyplot as plt
import os
import re
import pickle 
from multiprocessing import Pool

# function extracts sequences from .gbk file ans stores gene start stop positions
def rev(org,ncbid):
	di=os.getcwd()
	dir2=di+"/../genomes/"+org+'/'
	dir1=dir2+'fasta_op'
	os.system('mkdir '+dir1)
	os.system('mkdir '+dir1+'/forward')
	os.system('mkdir '+dir1+'/reverse')
	
	with open(dir2+ncbid+'.fasta',"r")as fil:
		s=[]
		for line in fil:
			line=line.rstrip()
			s.append(line)
	del s[0]
	seq="".join(s)
	seq=seq.replace('T','U')
	seq=seq.replace('Y','C')
	seq=seq.replace('R','A')
	seq=seq.replace('M','A')
	seq=seq.replace('K','G')
	seq=seq.replace('S','C')
	seq=seq.replace('W','U')
	seq=seq.replace('V','C')
	seq=seq.replace('B','G')
	seq=seq.replace('D','A')
	seq=seq.replace('H','U')

	with open(dir2+ncbid+'.gbk','r')as fil:
		c=0
		st=stp=0
		for_ststp=[]
		rev_ststp=[]
		v=[]
		for line in fil:
			if 'CDS' in line:
				en=re.compile('.*CDS(\s+|\s+complement\(|\s+complement\(<)(\d+)(..|..>)(\d+).*')
				if(en.match(line)):
					c+=1
					if(c==1):
						gi_prev=0
						se_prev=0
					if 'complement' in line:
						stp=int(en.match(line).group(2))+20
						st=int(en.match(line).group(2))-270
						v=[]
						v.append(int(en.match(line).group(2)))
						v.append(int(en.match(line).group(4)))
						l='com'
					else:
						st=int(en.match(line).group(4))-20
						stp=int(en.match(line).group(4))+270
						v=[]
						v.append(int(en.match(line).group(2)))
						v.append(int(en.match(line).group(4)))
						l='c'
					se=seq[st:stp]
					#print(se)
			if 'protein_id' in line:
				#print(line)
				en=re.compile('\s+/protein_id=\"(\w+).\d\"\n')
				if(en.match(line)):
					#print("matched")
					gi=en.match(line).group(1)
					if(c==1):
						gi_prev=0
						se_prev=0
					if(c>1):
						if(se != se_prev) and(gi!=gi_prev):
							if 'com' in l:
								v.append(gi)
								rev_ststp.append(v)
								
							else:
								v.append(gi)
								for_ststp.append(v)
							
							gi_prev=gi
							se_prev=se
		pickle.dump(for_ststp,open(dir1+'/forward_ststp.p',"wb"))
		pickle.dump(rev_ststp,open(dir1+'/reverse_ststp.p',"wb"))
	

# function creates fasta seq files for input to mfold
def fasta_op(org,ncbid):
	di=os.getcwd()
	dir2=di+"/../genomes/"+org+'/'
	dir1=dir2+'fasta_op'
	with open(dir2+ncbid+'.fasta',"r")as fil:
		s=[]
		for line in fil:
			line=line.rstrip()
			s.append(line)
	del s[0]
	seq="".join(s)
	# print(seq[0:100])
	seq=seq.replace('T','U')
	seq=seq.replace('Y','C')
	seq=seq.replace('R','A')
	seq=seq.replace('M','A')
	seq=seq.replace('K','G')
	seq=seq.replace('S','C')
	seq=seq.replace('W','U')
	seq=seq.replace('V','C')
	seq=seq.replace('B','G')
	seq=seq.replace('D','A')
	seq=seq.replace('H','U')
	
	op_for=pickle.load(open(di+'/../iden_hairpin/'+org+'/forward/interop_add+.p',"rb"))
	op_rev=pickle.load(open(di+'/../iden_hairpin/'+org+'/reverse/interop_add-.p',"rb"))
	for i,li in enumerate(op_for):
		st=li[1]-20
		stp=li[1]+270
		se=seq[st:stp]
		new_f=open(dir1+'/forward/seq'+str(i)+'.seq',"w")
		new_f.write('seq'+str(i)+'\n')
		complement = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A','N':'N'}
		se=''.join([complement[base] for base in se])
		new_f.write(se)
	for i,li in enumerate(op_rev):
		st=li[1]-270
		if(st<0):
			st=0
		stp=li[1]+20
		se=seq[st:stp]
		new_f=open(dir1+'/reverse/seq'+str(i)+'.seq',"w")
		new_f.write('seq'+str(i)+'\n')
		se=se[::-1]
		# print(se,st,stp)
		new_f.write(se)

