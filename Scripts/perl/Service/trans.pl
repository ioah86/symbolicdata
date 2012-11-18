##################################################
#
# Author: graebe
# createdAt: 2010-12-22

# purpose: generate RDF-Data descriptions from XMLData 
# see notes at the end of this file

use XML::DOM;
use File::Basename;
use strict;

my $parser=new XML::DOM::Parser;
my $out;
map $out.=action($_), @ARGV;
print TurtleEnvelope($out);

sub TurtleEnvelope {
  my $out=shift;
  return <<EOT;
\@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
\@prefix owl: <http://www.w3.org/2002/07/owl#> .
\@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
\@prefix sd: <http://symbolicdata.org/Data/Model/> .
\@prefix sdp: <http://symbolicdata.org/Data/People/> .
\@prefix sdpol: <http://symbolicdata.org/Data/PolynomialSystems/> .
\@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

sd:FreeAlgebra a owl:Class ; rdfs:label "Free Algebra" .

<http://symbolicdata.org/Data/FreeAlgebra/>
    a owl:Ontology ;
    rdfs:label "SD Free Algebra Systems Data" ;
    owl:imports <http://symbolicdata.org/Data/People/> .

$out
EOT
}

sub action {
  my $fn=shift;
  my $id = File::Basename::basename($fn,'.xml');
  my $doc=$parser->parsefile($fn) or die;
  $doc=$doc->getDocumentElement;
  my $date=$doc->getAttribute("createdAt");
  my $comment=getTagValue($doc,"Comment");
  my $vars=getTagValue($doc,"vars");
  my $deg=getTagValue($doc,"uptoDeg");
  return <<EOT;
<http://symbolicdata.org/Data/FreeAlgebra/$id> a sd:FreeAlgebra ;
    sd:createdAt "$date" ;
    sd:createdBy sdp:Heinle_A;
    sd:hasVariables "$vars" ;
    sd:uptoDegree "$deg" ;
    sd:relatedXMLResource <http://symbolicdata.org/XMLResources/FREEALGEBRA/$id.xml> ;
    rdfs:comment "$comment" .

EOT
}

sub getValues {
  my ($node,$tag)=@_;
  my $u;
  map {
    my $s=$_->toString();
    $s=~s/<[^>]*>\s*//gs;
    $s=~s/\s*<\/[^>]*>//gs;
    push(@$u,$s) if $s;
  } $node->getElementsByTagName($tag,0);
  return $u; # gibt nun einen ListPointer zurück
}

sub getTagValue {
  my ($node,$tag)=@_;
  my $u=getValues($node,$tag);
  return join(" ",@$u) if $u; 
}

__END__

export DIR="/home/graebe/SD/SD-2/XMLData"

perl transINTPS.pl $DIR/INTPS/*.xml $DIR/INTPS/Curves/Graphs/*.xml \
 $DIR/INTPS/Geometry/*.xml $DIR/INTPS/Paris/*.xml $DIR/INTPS/PoSSo/*.xml \
 $DIR/INTPS/Robotic/*.xml $DIR/INTPS/SignalTheory/*.xml \
 $DIR/INTPS/Singular/*.xml $DIR/INTPS/Verschelde/*.xml \
 $DIR/INTPS/ZeroDim/*.xml > INTPS.rdf

special processing
XMLData/INTPS/Curves/Generators/*.xml 
They have modular basedomain and are transformed to ModPS entries. 

The following examples are generated from the basic ones. 
XMLData/INTPS/Flat
XMLData/INTPS/Homog

Change them so that 
(1) the name has the basic example as prefix
(2) the reference is to the basic XMLResource/<example>
(3) Add a description how the example can be created from the basic one. 

See transFlat.pl

The following Data were added later on.

export DIR="/home/graebe/SD/SD-2/OWLData/XMLResources/INTPS"
perl transINTPS.pl $DIR/Amrhein.xml $DIR/Becker-Niermann.xml \
$DIR/Cassou_1.xml $DIR/FourBodyProblem.xml $DIR/Gerdt-93a.xml \
$DIR/Reimer_5.xml $DIR/Roczen.xml $DIR/satlib.uuf100_1.xml \
$DIR/satlib.uuf50_8.xml $DIR/satlib.uuf75_8.xml $DIR/Steidel_1.xml \
$DIR/Steidel_6.xml
