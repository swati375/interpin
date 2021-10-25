import os, sys
import multiprocessing
from hp_dist_for import hp_dist_new,mfold_dict
from hp_stemloop_filter import call_outlierhp_remove
from locate_all_for import locatehp

def parallel_hp_for(org):
	mfold_dict(org)
	call_outlierhp_remove(org,'forward')
	locatehp(org)
	hp_dist_new(org)

if __name__ == '__main__':
	parallel_hp_for(sys.argv[1])
