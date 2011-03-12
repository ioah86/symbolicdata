##################################################
#
# author: graebe
# createdAt: 2006-03-03

# purpose: collect CRefs from XMLData as SQL insert statements for the
# table
# create table CRefs (id varchar(80), xref varchar(80), comment text); 

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use sdXML;
use strict;

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;

my $parser=new XML::DOM::Parser;

map action($_), @ARGV;

sub action {
  my $fn=shift;
# get the old XML item
  my $doc=$parser->parsefile($fn) or die;
  my $id=$doc->getDocumentElement->getAttribute("id");
  map extractReference($id,$_),$doc->getElementsByTagName("ref");
}

sub extractReference {
  my ($id,$node)=@_;
  my $xref=$node->getAttribute("xref");
  $xref=~s.^CRef/..s;
  my $value=sdXML::getValue($node);
  print "delete from CRefs where id='$id' and xref='$xref';\n";
  print "insert into CRefs values('$id','$xref','$value');\n";
}
