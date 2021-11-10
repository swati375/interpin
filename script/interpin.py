import os, sys
import multiprocessing
from multiprocessing import Pool
import subprocess
from parallel_interop import interoper
from enr_identified_all import enr_dgrt15_all
from rev_interop import rev
import pickle
import argparse
from statsfilegenerate import make_table

def command_line_options():
	parser = argparse.ArgumentParser(description='code for downloading initial genome files for interpin program')
	parser.add_argument('--n','--num_cores', type=int, default=1,
                    help='an integer for specifying number of cores to be used. Use 1 for sequential. default=1')
	args=parser.parse_args()
	num=args.n
	print(num)
	return num

def automate1(indx):
	org=indx[0]
	ncbid=(indx[1]).split('.')[0]
	rev(org,ncbid)
	interoper(org,ncbid)

def automate2(indx):
	org=indx[0]
	ncbid=(indx[1]).split('.')[0]

	lis=['genome_prelim_for.pl' ,'genome_prelim_rev.pl']
	child=[]
	for i in lis:
		p=subprocess.Popen(["perl",i,str(org)], stdout=sys.stdout)
		child.append(p)
	for c in child:
		c.wait()

	lis=['build_for_op.py','build_rev_op.py']
	child=[]
	for i in lis:
		p=subprocess.Popen(["python3",i,str(org)], stdout=sys.stdout)
		child.append(p)
	for c in child:
		c.wait()

	lis=['parallel_hp_for.py',"parallel_hp_rev.py"]
	child=[]
	for i in lis:
		p=subprocess.Popen(["python3",i,str(org)], stdout=sys.stdout)
		child.append(p)
	for c in child:
		c.wait()

	print('made cluster and single hairpin for '+org)
	
	lis=['ir_cluster_for.py','ir_cluster_rev.py']
	child=[]
	for i in lis:
		p=subprocess.Popen(["python3",i,str(org)], stdout=sys.stdout)
		child.append(p)
	for c in child:
		c.wait()

	enr_dgrt15_all(org)

	lis=['iden_first_for.py','iden_first_rev.py']
	child=[]
	for i in lis:
		p=subprocess.Popen(["python3",i,str(org)], stdout=sys.stdout)
		child.append(p)
	for c in child:
		c.wait()

	make_table(org)

if __name__=='__main__':
	args=command_line_options()
	# args=sys.argv[1]
	print(args)
	di=os.getcwd()
	org_list=pickle.load(open(di+'/../orglist_dict.p',"rb"))
	data_list=[]
	for key in org_list.keys():
		data_list.append(org_list[key])
	os.system('mkdir '+di+'/../iden_hairpin/')
	os.system('mkdir '+di+'/../prep_hairpin/')
	os.system('mkdir '+di+'/../complete_hpin/')
	pool = Pool( processes = int(args))
	pool.map(automate1,data_list)
	pool.close()
	pool.join()
	arg=int(args/2)
	if arg<1:
		arg=1
	pool = Pool( processes = int(arg))
	pool.map(automate2,data_list)
	pool.close()
	pool.join()

	
