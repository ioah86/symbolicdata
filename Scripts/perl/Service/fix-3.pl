##################################################
#
# author: graebe
# createdAt: 2006-03-04

# purpose: fix id of an OWL record 

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use XML;
use strict;

my $parser=new XML::DOM::Parser;

map action($_), @ARGV;

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  my $oid=$doc->getDocumentElement->getAttribute("id");
  print "Original id is $oid\n";
  my $newid=fix($oid);
  print "New id is $newid\n";
  if ($oid eq $newid) { print "Nothing changed\n"; return; }
  $doc->getDocumentElement->setAttribute("id",$newid);
  XML::saveOWLFile($doc);

}

sub fix {
  local $_=shift;
  s/Chou_/Chou./;
  s/IMO_/IMO./;
  return $_;
}
