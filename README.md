

![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

    
# an algorithm to predict intrinsic terminators

Interpin is an algorithm designed to predict intrinsic transcription terminators in bacterial genomes. 
We have already created a database with the same name, where predictions from 12745 bacterial genomes are placed. It can be found at  [Interpin db](http://pallab.cds.iisc.ac.in/INTERPIN)

This document provides an easy installation guide for our algorithm. It can be used to make predictions for a single genome as well as run parallely on multiple genomes.

# Pre- requisites
1. Python3 (also install the following packages: matplotlib, biopython 1.78, multiprocessing, subprocess )
2. Perl5
3. Download and install edirect.sh
Following command can be used:
```bash
  sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
```
After installation, you may edirect commands to bashrc file (to access the program from anywhere) or on command line (to use for that session). Following line may be used for both purposes:
```bash
  export PATH=${PATH}:$HOME/edirect
```
4. Download and install bacbio package (for initial genome file processing). Following command may be used:
```bash
  pip install bcbio-gff
```

## Installation

Create a folder 'interpin'. Now create another folder 'program' inside it. 
All script codes must be placed inside this folder. 
Follow the steps below to make hairpin predictions using the interpin algorithm:
1. Make a list of bacteria for which you want to make hairpin predictions. Place the file in interpin folder, outside prog folder. 
file name: baclist_temp.txt

file format:

```diff
bacteria1_name ncbiid

bacteria2_name ncbiid
```

Note: Bacteria names and NCBI Id must be tab separated. Each line is record for one genome and must end by a new line character('\n')

Note: In ncbi id please give the complete ncbi id along with the version eg. NC_014614.1: adding .1 is essebntial to get the correct file for program input.

## 🚀 About Me
I'm a PhD student in the field of Computational biology at the Computational and Data sciences department, Indian Institute of Science.
I have worked with protein, RNA and DNA sequences, structure and annotations, alignment, docking etc.

Currently I work with genomic data and find interesting patterns in them. I then try to find the underlying principles for those patterns.


  
 

  
