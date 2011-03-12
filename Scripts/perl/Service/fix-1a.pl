##################################################
#
# author: graebe
# createdAt: 2006-03-04

# purpose: add entries to Annotation records scanning a file of crefs

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use XML;
use strict;

my $owldir ="$SD_HOME/NewData/OWLResources";
my $oldxmldir ="$SD_HOME/XMLData";
my $hash; # since there may be several annotations to the same file
my $parser=new XML::DOM::Parser;
open(FH,shift) or die;
while(<FH>) { scan($_); }
close FH;
map process($_), (keys %$hash);

### end main ###

sub scan {
  local $_=shift;
  s/^\s*//; s/\s*$//;
  my ($id,$ref,$text)=split /\s*\|\s*/;
  push @{$hash->{$id}}, fixId($ref)."XX".$text;
}

sub process {
  my $bib=shift;
  my $olddoc=$parser->parsefile("$oldxmldir/$bib.xml") or die;
  my $at=$olddoc->getDocumentElement->getAttribute("createdAt");
  my $by=$olddoc->getDocumentElement->getAttribute("createdBy");
  my $out=<<EOT;
The paper [$bib] discusses the following examples:

EOT
  my $l;
  map {
    my ($id,$text)=split /XX/;
    $_=$id;
    if ($text) { $out.="$_ as $text\n";} else {$out.="$_\n";} 
    push (@$l,"<OWL xref=\"$_\" class=\"Ideal\"/>") unless /\s+/;
  } @{$hash->{$bib}};
  
  $bib=~s.BIB/..;
  push (@$l,"<OWL xref=\"$bib\" class=\"BIB\"/>");

  my $doc=XML::getAnnotationHandle("BIB.$bib",$at,$by);
  XML::addNote($doc,$out,$l,$at,$by);
  #XML::showDocument($doc);
  XML::saveOWLFile($doc);
}
 
sub fixId {
  local $_=shift;
  s.INTPS/..g;
  s|/|.|g;
  s|Homog\.(.*)$|$1 (homogenized)|g;
  return $_;
}

sub splitId {
  local $_=shift;
  s.INTPS/.Ideal/.g;
  return split(/\//,$_,2);
}
