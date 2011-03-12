##################################
#
# author: graebe
# createdAt: 2006-03-06

# purpose: output the value of fields

# === start main ===

# all scripts are relative to this environment variable

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;

use lib "$ENV{'SD_HOME'}/Scripts/perl"; # the location of our XML.pm

use strict;
use XML::DOM; 
use XML; 

my $parser=new XML::DOM::Parser;
map action($_), @ARGV;

# === end main ===

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  printField($doc,"abstract");
}

sub printField {
  my ($doc,$tag)=@_;
  my $id=$doc->getDocumentElement->getAttribute("id");
  print "Field $tag of record $id is\n=============\n";
  print XML::getTagValue($doc,$tag);
}

