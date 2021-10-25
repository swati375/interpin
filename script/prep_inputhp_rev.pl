#!usr/local/bin/perl5 -w
no warnings 'uninitialized';

use List::Util 'max';
use Cwd qw(cwd);

sub prep_inputhairpin_rev {
$ni=$ARGV[0];

$n2=$ni;
$di=cwd;
chdir $di.'/../../../../prog';
$di=cwd;
print("$di\n");
$dir=$di."/../prep_hairpin";

my $c=0;
if ( -d "$dir/$n2")
{
  print "exists\n";
}
else
{
  system("mkdir $dir/$n2");
}
$dirn=$dir.'/'.$n2.'/reverse';
system("mkdir $dirn");

$dir1 = $di."/../genomes/$n2/det_files/reverse";
opendir(DIR, $dir1) or die("unable to open"); # opening directory
@contents1 = grep !/(^\.\.?$)|(^\.snv$)/, readdir DIR;  
$m=0;    
my @final_print;
$fi='seq';
foreach $file1(@contents1)
{ 
  $num=0;
    $m++;
    open(DATA, "$dir1/$file1") or die;
    $z=0;my @stack=();my @hairpin=();@halix=();
    $file_nam=substr($file1,0,-4);
    
    open(Y, ">>$dirn/$file_nam.txt") or die(" not open");
    while(($read=<DATA>))
    { $z++;
      if ($read=~m/^$fi/)
      {
        print Y "$read";
        goto a;
      }
    } 
	  a:while($read=<DATA>)
		{ 
	    $z++;
      
      if ($read =~m/^Stack/g){push(@stack,$z);}
      if ($read =~m/^Hairpin/g){push(@hairpin,$z);}
    
      if($read=~m/^Structure\s+(\d+)/ig)
      {
        $num=$1-1;
        my @newstack = reverse @stack;
        my @finalstack;
        LOOP1: for my $i (0..$#newstack) 
        { $x=$newstack[$i]-1;
          for my $j ($i+1..$#newstack) {  next LOOP1 if ($newstack[$j]== $x); }
          push @finalstack,$newstack[$i]; 
        }
        $temp_dif=999;
        @hair=reverse@hairpin;@f_hairpin=();@f_stack=();
        LOOP2:for my $l (0..$#hair)
        {
          for my $k (0..$#finalstack)  
          {
            $dif=$hair[$l]-$finalstack[$k]; 
            if(($dif > 0) && ($dif < $temp_dif))
            {
              $temp_dif = $dif;
              push @f_stack,$finalstack[$k];
            }
          }
          push @f_hairpin,"$hair[$l]\n"; 
          $temp_dif=999;
        }
        
        foreach $r (0..$#f_hairpin)
        { push@halix,$f_hairpin[$r]-1;}
        
        @final_print= sort{$b <=> $a}(@f_hairpin,@f_stack,@halix);
        open(DAT, "<$dir1/$file1") or die("not opening"); 
        $z1=0;$q=0;
        goto b;
        b:while($reads=<DAT>)
        { 
            $z1++;
            if ($z1>max(@final_print))
            {
              close(DAT);
              splice @hairpin;splice @hair; splice @f_hairpin; splice @f_stack; splice @finalstack; splice @newstack; splice @halix;splice @stack;splice @final_print;
              goto a; 
            }
            if($reads=~m/Structure\s+$num/ig)
            {
              print Y "\n$reads";
              for $i(0..2)
              {
                $reads=<DAT>;
              }
              if ($reads =~m/Initial dG/)
              {
                print Y "$reads\n";
              }
              $z1=$z1+3;
              goto b;
            }
            if (grep { $_ == $z1} @final_print)
            {
              print Y "$reads";
            }
                                           
        }
      }
    }
#### for last structure
    $num=$num+1;
        my @newstack = reverse @stack;
        my @finalstack;
        LOOP1: for my $i (0..$#newstack) 
        { $x=$newstack[$i]-1;
          for my $j ($i+1..$#newstack) {  next LOOP1 if ($newstack[$j]== $x); }
          push @finalstack,$newstack[$i]; 
        }
        $temp_dif=999;
        @hair=reverse@hairpin;@f_hairpin=();@f_stack=();
        LOOP2:for my $l (0..$#hair)
        {
          for my $k (0..$#finalstack)  
          {
            $dif=$hair[$l]-$finalstack[$k]; 
            if(($dif > 0) && ($dif < $temp_dif))
            {
              $temp_dif = $dif;
              push @f_stack,$finalstack[$k];
            }
          }
          push @f_hairpin,"$hair[$l]\n"; 
          $temp_dif=999;
        }
        
        foreach $r (0..$#f_hairpin)
        { push@halix,$f_hairpin[$r]-1;}
               
        @final_print= sort{$b <=> $a}(@f_hairpin,@f_stack,@halix);
        open(DAT, "<$dir1/$file1") or die("not opening"); 
        $z1=0;$q=0;
        goto b;

        b:while($reads=<DAT>)
        {   
            $z1++;
            if ($z1>max(@final_print))
            {
              close(DAT);
              splice @hairpin;splice @hair; splice @f_hairpin; splice @f_stack; splice @finalstack; splice @newstack; splice @halix;splice @stack;splice @final_print;
              exit; 
            }
            if($reads=~m/Structure\s+$num/ig)
            {
              print Y "\n$reads";
              for $i(0..2)
              {
                $reads=<DAT>;
              }
              if ($reads =~m/Initial dG/)
              {
                print Y "$reads\n";
              }
              $z1=$z1+3;
              goto b;
            }
            if (grep { $_ == $z1} @final_print)
            {
              print Y "$reads";
            }
                                           
        }
}
close DIR;

}##end of function

1;
