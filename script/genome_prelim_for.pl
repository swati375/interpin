#!usr/local/bin/perl5 -w
no warnings 'uninitialized';
use Cwd qw(cwd);
$di=cwd;
chdir($di);
require $di.'/run_mfold_for.pl';
require $di.'/prep_inputhp_for.pl';

#program to run mfold on sequences and extract out hp from mfold output for each seq
&mfold_for($ARGV[0]);
$dir=cwd;
#print $dir;
chdir($di);
$dir=cwd;
#print $dir;
&prep_inputhairpin_for($ARGV[0]);
