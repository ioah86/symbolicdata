##################################################
#
# author: graebe
# createdAt: 2006-03-03

# purpose: transform INTPS/Curves/Generators records to
# XMLResource/GenPS and add information to the corresponding
# Annotation

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use XML;
use strict;

my $parser=new XML::DOM::Parser;
my $xmldir="$SD_HOME/NewData/XMLResources/GenPS";

map action($_), @ARGV;

sub action {
  my $fn=shift;
# get the old XML item
  my $doc=$parser->parsefile($fn) or die;
# fix the id
  my $oldid=$doc->getDocumentElement->getAttribute("id");
  my $id=fixId($oldid);
# create XMLResource file
  my $doc1=createXMLSource($doc,$fn);
# create Annotation
  my $date=$doc->getDocumentElement->getAttribute("createdAt");
  my $name=$doc->getDocumentElement->getAttribute("createdBy");
  my $refs=[split(/\n/,<<EOT)];
<XML url="sdxml:GenPS/$id.xml" XMLType="GeneralPolynomialSystem"/>
<OWL xref="$id" class="INTPSAnnotation"/>
<OWL xref="$id" class="Ideal"/>
EOT

  my $doc2=getAnnotationHandle($id,$date,$name);
  XML::addNote($doc2,<<EOT,$refs,$date,$name);

The generators of the implicit representation computed over GF(31991)
are contained in sdxml:GenPS/$id.xml
EOT

# add ChangeLog entry 
  XML::addToChangeLog($doc1,"graebe","2006-03-05",
		      "compiled from XMLData $oldid") ;
  XML::addToChangeLog($doc2,"graebe","2006-03-05",
		      "compiled from XMLData $oldid") ;
# save the stuff
  # return map XML::showDocument($_), ($doc1, $doc2);

  XML::saveXMLFile($doc1,"$xmldir/$id.xml");
  XML::saveOWLFile($doc2);

}

sub createXMLSource { # compile the XML resource
  my ($src,$fn)=@_;
  my $doc=getEmptyCopy($fn);
  my $root=$doc->getDocumentElement;

  my $hash;
  my $uhu=XML::getTagValue($src,"vars");
  $uhu.=" ".XML::getTagValue($src,"parameters");
  $hash->{"vars"}=fixVarList($uhu);
  $hash->{"basis"}=XML::getTagValue($src,"basis");
  $hash->{"ChangeLog"}=XML::getTagValue($src,"ChangeLog");

# build up the DOM 
  XML::appendNode($doc,"basedomain","GF(31991)");
  XML::appendNode($doc,"vars",$hash->{"vars"});
  XML::appendNode($doc,"basis",$hash->{"basis"});
  XML::appendNode($doc,"Comment",$hash->{"Comment"});
  XML::appendNode($doc,"ChangeLog",$hash->{"ChangeLog"});
  return $doc;
}

sub fixId {
  local $_=shift;
  s|INTPS/Curves/Generators/|Curves.|;
  return $_;
}

sub fixVarList { # convert it to comma separated list
  local $_=shift;
  s/^\s+//g;
  s/\s+$//g;
  s/\s+/,/g;
  return $_;
}
