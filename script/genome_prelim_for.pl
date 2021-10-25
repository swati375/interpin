#!usr/local/bin/perl5 -w
no warnings 'uninitialized';
use Cwd;
require 'run_mfold_for.pl';
require 'prep_inputhp_for.pl';

#program to run mfold on sequences and extract out hp from mfold output for each seq
&mfold_for($ARGV[0]);
&prep_inputhairpin_for($ARGV[0]);
