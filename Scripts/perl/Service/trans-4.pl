##################################################
#
# author: graebe
# createdAt: 2006-03-05

# purpose: transform GeoCode to the new Data structure

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use XML;
use strict;

my $parser=new XML::DOM::Parser;
my ($hash, $Comment, @ChangeLog);

map action($_), @ARGV;

my $doc=$parser->parse(<<EOT);
<?xml version="1.0"?>
<GeoCode createdAt="2002-05-28" createdBy="graebe"/>
EOT
my $root=$doc->getDocumentElement;
map {
  my $node=$hash->{$_};
  $node->setOwnerDocument($doc);
  $root->appendChild($node);
} (sort keys %$hash);
XML::appendNode($doc,"Comment",$Comment); 
my $u=XML::createNode($doc,"<ChangeLog/>");
map { 
  #print $_->toString();
  $_->setOwnerDocument($doc);
  $u->appendChild($_);
} @ChangeLog;
$root->appendChild($u);

XML::showDocument($doc);

### end main ###

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  my $root=$doc->getDocumentElement;
  my $id=$root->getAttribute("id");
  $id=~s.GeoCode/..;
  $root->setAttribute("id",$id);
  $root->removeAttribute("createdBy");
  $root->removeAttribute("createdAt");
  $root->setTagName("GeoFunctionDescription");
  map $root->removeChild($_), $root->getElementsByTagName("Version");
  map {
    $Comment.="\n".XML::getValue($_);
    $root->removeChild($_); 
  } $root->getElementsByTagName("Comment");
  map {
    push @ChangeLog, @{$_->getChildNodes};
    $root->removeChild($_); 
  } $root->getElementsByTagName("ChangeLog");
  $hash->{$id}=$root;
}
