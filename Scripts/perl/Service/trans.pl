##################################################
#
# Authox: graebe
# createdAt: 2010-12-22

# purpose: transform XMLData descriptions to RDF Data
# see notes at the end of this file

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;

use XML::DOM;
use strict;

#my $parser=new XML::DOM::Parser;
my $out;
my $hash=getCASData();
map { $out.=getCASData($_); }
(["Axiom"]);
print prefix().$out."\n</rdf:RDF>\n";

sub prefix {
  return <<EOT;
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE rdf:RDF [  
  <!ENTITY sd "http://hgg.ontowiki.net/SymbolicData/">
  <!ENTITY sdxml "http://www.symbolicdata.org/XMLResources/">
  <!ENTITY owl "http://www.w3.org/2002/07/owl#">
  <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#">
  <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">
]>

<rdf:RDF xml:base="&sd;PolynomialSystems/" 
  xmlns:sd="&sd;"
  xmlns:owl="&owl;"
  xmlns:rdf="&rdf;"
  xmlns:rdfs="&rdfs;"
  xmlns:xsd="&xsd;">

<!-- Ontology specific informations -->
  <owl:Ontology rdf:about="&sd;PolynomialSystems/"
    rdfs:label="SD CAS Data">

    <rdfs:comment>CAS Data in the Symbolic Data Collection.</rdfs:comment>

    <owl:imports rdf:resource="&sd;Person/" />
  </owl:Ontology>

<!-- Classes -->

  <owl:Class rdf:about="&sd;CAS" rdfs:label="Computer Algebra System" />

<!-- Instances and untyped data -->

EOT

}

sub getCASData {
  my $u=shift;
  return <<EOT;
  <sd:CAS rdf:about="$u"     
   sd:hasURLLiteral="to be fixed"/>
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
