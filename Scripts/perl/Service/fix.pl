##################################################
#
# author: graebe
# createdAt: 2012-11-04

# purpose: extract entries in an XML tree

use XML::DOM;
use strict;

my $parser=new XML::DOM::Parser;
my $hash;
map action2($_), @ARGV;
#map print("$_: $hash->{$_}\n"), (sort keys %$hash);

sub action1 {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  my $name=$doc->getDocumentElement->getAttribute("createdBy");
  $hash->{$name}++;
}

sub action2 {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  print "\n$fn:\n";
  map {
    print $_->toString();
  } $doc->getElementsByTagName("Comment");
}
