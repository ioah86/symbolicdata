##################################################
#
# author: graebe
# createdAt: 2006-03-04
# modified: 2010-12-27

# purpose: fix a string in a file 

use strict;

map action($_), @ARGV;

sub action {
  my $fn=shift;
  system("cp $fn $fn.bak");
  local $/;
  open(FH,$fn);
  local $_=<FH>;
  close FH;
  open(FH,">$fn");
  print FH fix($_);
  close FH;
  print "Fixed $fn\n";
}

sub fix {
  local $_=shift;
  s/compiled from XMLData ModPS/compiled from XMLData INTPS/gs;
  return $_;
}
