
![Logo](https://github.com/swati375/interpin/blob/main/interpin_logo.png)

    
# Interpin : an algorithm to predict intrinsic terminators

Interpin is an algorithm designed to predict intrinsic transcription terminators in bacterial genomes. 
We have already created a database with the same name, where predictions from 12745 bacterial genomes are placed. It can be found at  [Interpin db](http://pallab.cds.iisc.ac.in/INTERPIN)

This document provides an easy installation guide for our algorithm. It can be used to make predictions for a single genome as well as run parallely on multiple genomes.

# Pre- requisites
1. Python3 (also install the following packages: matplotlib, biopython 1.78, multiprocessing, subprocess ). Anaconda / miniconda can be used for installation.
2. Perl5
3. Download and install edirect.sh
Following command can be used:
```bash
  sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
```
After installation, you may add edirect commands to bashrc file (to access the program from anywhere). Following line should be added:
```bash
  export PATH=${PATH}:$HOME/edirect
```
The same line can be used as a command to add edirect temporarily to current session only.

4. Download and install bacbio package (for initial genome file processing). Following command may be used:
```bash
  pip install bcbio-gff
```

## Installation

Create a folder 'interpin'. Now create another folder 'program' inside it. 
All script codes must be placed inside this folder. 
Follow the steps below to make hairpin predictions using the interpin algorithm:
1. Make a list of bacteria for which you want to make hairpin predictions. Place the file in interpin folder, outside prog folder. 

file name: baclist.txt

file format:

```diff
bacteria1_name ncbiid

bacteria2_name ncbiid
```

Note: Bacteria names and NCBI Id must be tab separated. Each line is record for one genome and must end by a new line character('\n')

Note: In ncbi id please give the complete ncbi id along with the version eg. NC_014614.1: adding .1 is essebntial to get the correct file for program input.

Note: Do not use any space or special case character in bacteria name. replace them by a '_' or '-'. eg: Acetobacter ascendens LMG 1590 to Acetobacter_ascendens_LMG_1590

2. Now, run program inifiles_download.py. This will create a folder : interpin/genomes

```bash
  cd program
  python inifiles_download.py --n num
```
here 'num' is the number of cores available for processing. For serial processing, use 'n=1'.

Note: to see requirements of program and see short description of the program, use the below command. 
```bash
  python inifiles_download.py -h
```
3. Download Molquest for making operon prediction, which will be used for creating boundaries of transcription units. Download from here: [Molquest](http://www.molquest.com/molquest.phtml?topic=downloads)

Note: The free trial for Molquest is currently only available for Windows and Mac users.

Molquest takes fasta files as input. They can be taken from the required bacterial folder inside genomes folder. 
As output, two files are given, take the 'results.txt' file and place this prediction in the same bacterial folder 
from where fasta file was taken. This is the only file required from molquest.

4. Download Mfold package for RNA foldings. Details about the software and installation intruction can be found here: [Mfold download](http://www.unafold.org/mfold/software/download-mfold.php) and [about](http://www.unafold.org/).
5. Now, all the input files are ready and the main interpin code can be run. Use the command below:
```bash
  python interpin.py --n num
```
here 'num' is the number of cores available for processing. For serial processing, use 'n=1'.

Note: to see requirements of program and see short description of the program, use the below command. 
```bash
  python interpin.py -h
```
The final output is given in the form of a csv file, placed in the 'iden_hairpin' folder of each genome.

## sample files
The sample files for each step are provided in the folder 'sample'.
This would help understanding the format of input files if required. 

As an example, I have run Intrepin codes on three bacterial genomes and placed them in the sample folder. The different folders formed, with the raw intermediate files are placed in these folders. 

See below image for explanation of output:
![output]()

## Features

- Can be run parallely on multiple genomes (number depends on cores available)
- Takes 10-15 hours for a giving predictions, with 90% time taken by Mfold to make folded structures.
- Cross platform
- No bias for AT/ GC rich genomes
- Predicts cluster as well as single hairpin. Cluster hairpin are novel type of hairpins given by the algorithm. 
To know more about the study, you can check out our publication [here](https://www.nature.com/articles/s41598-021-95435-3)


  
## 🚀 About Me
I'm a PhD student in the field of Computational biology at the Computational and Data sciences department, Indian Institute of Science.
I have worked with protein, RNA and DNA sequences, structure and annotations, alignment, docking etc.

Currently I work with genomic data and find interesting patterns in them. I then try to find the underlying principles for those patterns.


  
  
