import os,sys
import pandas as pd
import multiprocessing
from multiprocessing import Pool
import pickle
import argparse

def command_line_options():
	parser = argparse.ArgumentParser(description='code for downloading initial genome files for interpin program')
	parser.add_argument('--n','--num_cores', type=int, default=1,
                    help='an integer for specifying number of cores to be used. Use 1 for sequential. default=1')
	args=parser.parse_args()
	num=args.n
	return num

def form_orgdict():
	di=os.getcwd()
	file=open(di+'/../baclist.txt',"r")
	lines=file.readlines()
	bac_dict={}
	data_list=[]
	for li in lines:
		s=li.split('\t')
		ncbid=(s[1].rstrip()).split('.')[0]
		bac_dict[ncbid]=[s[0],s[1].rstrip()]
		data_list.append([s[0],s[1].rstrip()])
	pickle.dump(bac_dict,open(di+'/../orglist_dict.p',"wb"))
	return(data_list)

def download_gff(line):
	di=os.getcwd()
	org=line[0]
	ncbid=line[1]
	#using wget to download gff file
	cmd='mkdir '+di+'/../genomes/'+org
	os.system(cmd)
	cmd = 'wget -O '+di+'/../genomes/'+org+'/'+'{}.gff "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=nuccore&report=gff3&id={}" --no-check-certificate'.format(ncbid,ncbid)
	# print(cmd)
	os.system(cmd)
	download_fasta(org,ncbid)
	

def download_fasta(org,ncbid):
	ncbi=ncbid.split('.')[0]
	di=os.getcwd()
	cmd='esearch -db nucleotide -query "'+ncbid+'" | efetch -format fasta > '+di+'/../genomes/'+org+'/'+ncbi+'.fasta'
	# print(cmd)
	os.system(cmd)
	form_gbk(org,ncbid)


def form_gbk(org,ncbid):
	di=os.getcwd()
	dir1=di+'/../genomes/'+org+'/'
	s=ncbid.split('.')
	cmd='python3 gff_to_genbank.py '+dir1+ncbid+'.gff '+dir1+s[0]+'.fasta'
	# print(cmd)
	os.system(cmd)
	cmd='mv '+dir1+ncbid+'.gb '+dir1+s[0]+'.gbk'
	os.system(cmd)



if __name__=='__main__':
	args=command_line_options()
	# args=sys.argv[1]
	# print(args)
	di=os.getcwd()
	data_list=form_orgdict()
	os.system('mkdir '+di+'/../genomes/')
	pool = Pool( processes = int(args))
	pool.map(download_gff,data_list)
	pool.close()
	pool.join()
	
	
