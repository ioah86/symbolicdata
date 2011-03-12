f##################################################
#
# author: graebe
# createdAt: 2006-03-04

# purpose: Create Annotation records from nonempty Comment part. 

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use sdXML;
use strict;

my $owldir ="$SD_HOME/Data/OWLResources";
my $parser=new XML::DOM::Parser;

map action($_), @ARGV;

## end main ##

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;

  map {
    my $c=sdXML::getTagValue($doc,"Comment");
    createAnnotation($doc,$c) if $c; 
  } $doc->getElementsByTagName("Comment");

}

sub createAnnotation {
  my ($doc,$c)=@_;
  my $id=$doc->getDocumentElement->getAttribute("id");
  my $fn="$owldir/Annotation/$id.xml";
  return "$fn already exists\n" if -e $fn;
  my $date=$doc->getDocumentElement->getAttribute("createdAt");
  my $person=$doc->getDocumentElement->getAttribute("createdBy");
  open(FH,">$fn");
  print FH <<EOT;
<?xml version="1.0"?>
<Annotation createdAt="$date" createdBy="$person" id="$id">
<!-- \$Id: fix-2.pl,v 1.3 2007/10/04 12:51:11 graebe Exp $ -->
<note>$c</note>
  <relatesTo>
    <OWL xref="$id" class="INTPSAnnotation"/>
  </relatesTo>
  <Comment/>
  <ChangeLog/>
</Annotation>
EOT
  close(FH);
  print "Annotation saved to $fn\n";
}

sub fix {
  my $node=shift;
  my $r=$node->getAttribute("resource");
  $r=~s/sdxml://;
  $r="sdxml:INTPS/$r.xml";
  $node->removeAttribute("resource");
  $node->setAttribute("url",$r);
  return 1;
}

sub saveFile {
  my ($doc,$fn)=@_;
  # print $doc->toString(1); return;
  system("cp $fn $fn.bak");
  $doc->printToFile($fn,1);
  print "Saved changes to $fn\n";
}
