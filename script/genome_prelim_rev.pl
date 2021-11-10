#!usr/local/bin/perl5 -w
no warnings 'uninitialized';
use Cwd qw(cwd);
$di=cwd;
chdir($di);
require $di.'/run_mfold_rev.pl';
require $di.'/prep_inputhp_rev.pl';

&mfold_rev($ARGV[0]);
$dir=cwd;
# print $dir;
chdir($di);
$dir=cwd;
# print $dir;
&prep_inputhairpin_rev($ARGV[0]);