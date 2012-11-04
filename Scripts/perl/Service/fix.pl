##################################################
#
# author: graebe
# createdAt: 2012-11-04

# purpose: extract entries in an XML tree

use XML::DOM;
use strict;

my $parser=new XML::DOM::Parser;
my $hash;
map action($_), @ARGV;
map print("$_\n"), (sort keys %$hash);

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  my $name=$doc->getDocumentElement->getAttribute("createdBy");
  $hash->{$name}=1;
}
