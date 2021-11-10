#!/usr/bin/perl -w
use Cwd qw(cwd);
no warnings 'uninitialized';

# program to run multiple files of fasta format in mfold software
sub mfold_for{
    $fi=$ARGV[0];
    $file=$fi;
    #print "running mfold on $file\n";
    # print "forward";
    my $c=0;
            $di=cwd;
            $dir=$di."/../genomes/$file";
            $dir1 = $di."/../genomes/$file/fasta_op/forward";    
                $dir=$dir."/det_files";
                system("mkdir $dir");
                $dir=$dir."/forward";
                system("mkdir $dir");
                opendir(DIR, $dir1) or die 'cant open $file';
                @contents1 = grep !/(^\.\.?$)|(^\.snv$)/, readdir DIR;
                my $a=0;
                chdir($dir) or die "cant change";
                foreach $file1(@contents1)
                {   
                    
                        $a++;
                        $command="mfold SEQ=".$dir1."/$file1";
                        system($command);
                        print($a);
                }

                system("find . -type f -not -iname '*.det' -delete");
                print "\n============================================\nMFOLD FOR $file OVER\n================\n";
# print "done.. \n";
close (DIR);
}##end of function 
1;
