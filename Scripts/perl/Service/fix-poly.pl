##################################################
#
# author: graebe
# createdAt: 2010-05-14

# purpose: remove white spaces from poly entries
# usage: perl fix-poly.pl file

use strict;
undef $/;
map action($_), @ARGV;

### end main ###

sub action {
  my $fn=shift;
  open(FH,$fn) or die;
  $_=<FH>;
  s/<poly>(.*?)<\/poly>/trans($1)/egs;
  print $_;
}

sub trans {
  local $_=shift;
  s/\s//gs;
  return "<poly>$_</poly>";
}
