import os, sys
from interop import interop,interop2,sign_separate_interop
from multiprocessing import Pool
from missing_cds import missing_cds
from rev_interop import fasta_op

# program to process operon_prediction file from molquest to give initial transcription units
def interoper(org,ncbid):
	interop(org)
	interop2(org)
	sign_separate_interop(org)
	missing_cds(org)
	fasta_op(org,ncbid)
	# print("done")
	
	
