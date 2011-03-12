##################################################
#
# author: graebe
# createdAt: 2006-03-03

# purpose: transform PERSON records to the new Data structure

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
# get the old XML item
  my $doc=$parser->parsefile($fn) or die;
# fix the id
  my $oldid=$doc->getDocumentElement->getAttribute("id");
  my $id=fixId($oldid);
  my $contribution=createContribution($doc,$fn,$id);
  my $person=createPerson($doc,$fn,$id);

  # map XML::showDocument($_), ($contribution,$person); return;

  map XML::saveOWLFile($_), ($contribution,$person); 
}

sub createContribution { 
  my ($src,$fn,$id)=@_;
  my $doc=XML::getEmptyCopy($fn);
  my $root=$doc->getDocumentElement;
  $root->setAttribute("id",$id);
  $root->setTagName("Contributor");
  $root->removeAttribute("createdBy");
  
  my $hash;
  $hash->{"hasURL"}=XML::getTagValue($src,"url");
  $hash->{"hasEmail"}=XML::getTagValue($src,"email");
  $hash->{"hasContributed"}=XML::getTagValue($src,"contribution");
  $hash->{"theName"}=XML::getTagValue($src,"name");
  $hash->{"theNickName"}=$id;
  $hash->{"thePerson"}=<<EOT;
<OWL xref="$id" class="Person"/>
EOT
  $hash->{"theStatus"}=XML::getTagValue($src,"status");

  map {
    XML::appendNode($doc,$_,$hash->{$_}) if $hash->{$_};
  } (sort keys %$hash);

  return $doc;
}

sub createPerson { 
  my ($src,$fn,$id)=@_;
  my $doc=XML::getEmptyCopy($fn);
  my $root=$doc->getDocumentElement;
  $root->setAttribute("id",$id);
  $root->setTagName("Person");
  $root->removeAttribute("createdBy");

  my $hash;
  $hash->{"hasAffiliation"}=XML::getTagValue($src,"location");
  $hash->{"theName"}=XML::getTagValue($src,"name");

  map {
    XML::appendNode($doc,$_,$hash->{$_}) if $hash->{$_};
  } (sort keys %$hash);

  return $doc;
}

sub fixId {
  local $_=shift;
  s.PERSON/..;
  return $_;
}

