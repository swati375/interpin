#!usr/local/bin/perl5 -w
no warnings 'uninitialized';
use Cwd;
require 'run_mfold_rev.pl';
require 'prep_inputhp_rev.pl';

&mfold_rev($ARGV[0]);
&prep_inputhairpin_rev($ARGV[0]);
