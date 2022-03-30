import pickle
import os
import re
import math
from multiprocessing import Pool
import sys

def build_hp_for(org):
	# print(srr)
	di=os.getcwd()
	file1=org

	org=ngi=0

	dir1=di+"/../prep_hairpin/"+file1+'/forward'
	print (dir1)
	org=org+1
	#-------------$organism contain organism name for genomes folder and gene id-----------------------------------#

	#---------------Writing output file------------------------------------------------------------
	filen=di+"/../complete_hpin/forward_"+file1
	w=open(filen,"w")
	#---------------------------------------------------------------------------------------------------------------
	w.write( "============================================================================================================================================\n")
	w.write("\n\tOrganism: "+file1+"\n")
	w.write("============================================================================================================================================\n")

	total_eng_genome=total_no_genome=sum_genome=sq=0
	pair_eng_2=[]
	pair_eng3=[]
	genome_eng =[]
	hair_eng=[]
	total_energy=[]
	
	contents3=os.listdir(dir1)
	dir_seq=di+"/../genomes/"+file1+"/fasta_op/forward/"
	gi_all=os.listdir(dir_seq)
	gi_all=[x[3:-4] for x in gi_all]
	for file3 in contents3:
	   	with open(dir_seq+file3[0:-4]+'.seq') as fil:
	   		line=fil.readlines()
	   		seq=line[1]
	   	gi=file3[3:-4]
		count_alpha=sum(c.isalpha() for c in file3[0:-4])
	   	# print ("gi=",gi)
	   	if gi not in gi_all:
	   		print("NOOOO!!\n")
	   	else:
		   	w.write("\n\n******************************************************************************************************************************************\n")
		   	w.write("\n\tGI="+gi+"\t\tLength= "+str(len(seq))+"\n")
		   	w.write("\nDownstream Sequence -20 to 270 = "+seq+"\n\n")
		   	with open(dir1+'/'+file3)as fil_bui:
		   		fil=fil_bui.readlines()
		   		count=end_stem=eng_bulb=sum_a=num=total_no=0
		   		start=[]
		   		stop=[]
		   		hh_all=[]
		   		hh=[]
		   		hh1=[]
		   		num_prev=-1
		   		num=0
				loop_c=0
		   		for line in fil[3:]:
		   			if(num_prev<num):
			   			if ('External closing pair' in line) and ('Interior' not in line):
			   				ene=re.match(r'.* is [AUGCTYRMKSWVBDHXYZaugctyrmkswvbdhxyz]\(\s+(\d+)\)\-[UACGTYRMKSWVBDHXYZaugctyrmkswvbdhxyz]\(\s+(\d+)\)',line)
			   				stem_start=int(ene.group(1))-count_alpha
			   				stem_stop=int(ene.group(2))-count_alpha
			   				st=stem_start-20
			   				en=stem_stop-20
			   				start.append(st)
			   				stop.append(en)
							loop_c+=1
			   			if 'Helix' in line:
			   				ene=re.match(r'.*ddG =\s*(\-\d+\.\d+|\d+\.\d+)\s+.*',line)
			   				eng_stem=float(ene.group(1))
			   			if 'Hairpin loop' in line:
							if (loop_c>0):
								ene=re.match(r'.*ddG =\s+(\-\d+\.\d+|\d+\.\d+)\s+Closing pair is [AUGCTYRMKSWVBDHXYZaugctyrmkswvbdhxyz]\(\s+(\d+)\)\-[AUGCTYRMKSWVBDHXYZaugctyrmkswvbdhxyz]\(\s+(\d+)\)',line)
								count+=1
								loop_c=0
								stt=int(ene.group(2))-20-count_alpha
								end=int(ene.group(3))-20-count_alpha
								eng_bulb=float(ene.group(1))
								bulb_stt=int(ene.group(2))-count_alpha
								bulb_stp=int(ene.group(3))-count_alpha
								total_no+=1
								hairpin_loop1=seq[stem_start-1:bulb_stt]
								hairpin_loop2=seq[bulb_stt:bulb_stp-1]
								hairpin_loop3=seq[bulb_stp-1:stem_stop]
								hairpin_loop=hairpin_loop1+"("+hairpin_loop2+")"+hairpin_loop3
								hairpin_loopx=hairpin_loop1+hairpin_loop2+hairpin_loop3
								hairpin_length=len(hairpin_loop)-2
								if 'eng_stem' in locals():
									dummy = eng_stem+eng_bulb
									total_eng=float(dummy)
									total_energy.append(total_eng)
									hair_eng.append(total_eng)
									sum_a+=float(total_eng)
									hh_all=[[start[i],stop[i]] for i in range(len(start))]
									hh_all=sorted(hh_all)
									hh=[row[0] for row in hh_all]
									hh1=[row[1] for row in hh_all]
									if(count == 1):
										st_num=num+1
										w.write("******************************structure="+str(st_num)+"********************************************\n")
										w.write(" _______________________________________________________________________________________________________________________\n")
										w.write( " Start\tStop\tHairpin loop\tLength\tEnergy\n")
										w.write(" ________________________________________________________________________________________________________________________\n")
									w.write(str(st)+"\t"+str(en)+'\t'+hairpin_loop+"\t"+str(hairpin_length)+"\t"+str(total_eng)+"\n")
			   			if 'Structure' in line:
			   				num_prev=num
			   				ene=re.match(r'Structure\s+(\d+)',line)
			   				num=int(ene.group(1))-1
			   				del total_energy[:],hair_eng[:],hh[:],hh1[:],start[:],stop[:]
				   			count=sum_a=total_no=0
		   	num=num+1
		   	w.write("************************************************************************************************\n")
		   	fil_bui.close()


if __name__ == '__main__':
	build_hp_for(sys.argv[1])
