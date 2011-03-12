##################################################
#
# author: graebe
# createdAt: 2006-03-04

# purpose: add entries to Annotation records scanning a file of crefs
# usage: perl fix-1.pl file

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use sdXML;
use strict;

my $owldir ="$SD_HOME/Data/OWLResources";
my $hash; # since there may be several annotations to the same file
my $parser=new XML::DOM::Parser;
open(FH,shift) or die;
while(<FH>) { action($_); }
close FH;
map XML::showDocument($hash->{$_}), (keys %$hash);
#map XML::saveOWLFile($hash->{$_}), (keys %$hash);

### end main ###

sub action {
  local $_=shift;
  s/^\s*//; s/\s*$//;
  my ($id,$ref,$text)=split /\s*\|\s*/;
  my ($rcls,$rid)=splitId($ref);
  my $fn="$owldir/Annotation/$rid.xml";
  my $doc=$hash->{$fn};
  my ($date,$name);
  unless ($doc) {
    $doc=sdXML::getAnnotationHandle($rid,$date,$name);
    $hash->{$fn}=$doc;
  }
  addRelatedInfo($doc,$id); 
}

sub addRelatedInfo {
  my ($doc,$id)=@_;
  my ($cls,$id)=splitId($id);
  my $u=createNode($doc,<<EOT);
<OWL xref="$id" class="$cls"/>
EOT
  map $_->appendChild($u), $doc->getElementsByTagName("relatesTo");
}

sub fixId {
  local $_=shift;
  s.PROBLEMS/.Annotation/.g;
  s.INTPS/.Ideal/.g;
  return $_;
}

sub splitId {
  local $_=shift;
  s.INTPS/.Ideal/.g;
  return split(/\//,$_,2);
}
