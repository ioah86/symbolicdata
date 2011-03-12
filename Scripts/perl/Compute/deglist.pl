##################################
#
# author: graebe
# createdAt: 2006-03-03

# purpose: compute theDegreeList and theLengthsList using MuPAD. 
# Save the output of this script as in.txt and run it with MuPAD as
# 'mupad <in.txt >out.txt'

# === start main ===

# all scripts are relative to this environment variable
my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl"; # the location of our XML.pm

use strict;
use XML::DOM; 
use XML; 

my $parser=new XML::DOM::Parser;
print("Pref::echo(FALSE):Pref::prompt(FALSE):\n");
map action($_), @ARGV;
print("quit;\n");

# === end main ===

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  my $id=$doc->getDocumentElement->getAttribute("id");
  my $vars=XML::getTagValue($doc,"vars");
  my @l;
  map push(@l,XML::getValue($_)), $doc->getElementsByTagName("poly");
  my $polys=join(",\n",@l);
  print <<EOT;
vars:=[$vars]:
polys:=[$polys]:
dlist:=sort(map(polys,degree)):
llist:=sort(map(polys,nops)):
print(NoNL,"<Result id=\\"$id\\" dlist=\\"".expr2text(dlist)
       ."\\" llist=\\"".expr2text(llist)."\\"/>");
EOT
}

