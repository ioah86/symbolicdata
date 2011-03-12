##################################################
#
# Authox: graebe
# createdAt: 2010-12-22

# purpose: transform XMLData/INTPS descriptions to RDF Data
# see notes at the end of this file

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;

use XML::DOM;
use strict;

my $parser=new XML::DOM::Parser;

my $out;
map $out.=action($_), @ARGV;
print prefix().$out."\n</rdf:RDF>\n";

sub action {
  my $fn=shift;
# get the old XML item
  my $doc=$parser->parsefile($fn) or die;
  return transformedData($doc->getDocumentElement);
}

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
    rdfs:label="SD INTPS Data">

    <rdfs:comment>Polynomial Systems Data in the Symbolic Data Collection.
    Contains Integer and Modular (to be added) Polynomial Systems. The
    XMLData/INTPS/Homog and XMLData/INTPS/Flat examples have yet to be
    treated</rdfs:comment>

    <owl:imports rdf:resource="&sd;Person/" />
  </owl:Ontology>

<!-- Classes -->

  <owl:Class rdf:about="&sd;INTPS" rdfs:label="Integer Polynomial Systems" />
  <owl:Class rdf:about="&sd;ModPS" rdfs:label="Modular Polynomial Systems" />

<!-- Instances and untyped data -->

EOT

}

sub transformedData {
  my $doc=shift;

  # The Header
  my $id=$doc->getAttribute("id");
  my $newid=fixId($id);
  my $createdAt=$doc->getAttribute("createdAt");
  my $createdBy=$doc->getAttribute("createdBy");

  # INTPS specific
  my $vars=fixList(getTagValue($doc,"vars"));
  my $parameters=fixList(getTagValue($doc,"parameters"));
  my $basis=getTagValue($doc,"basis");
  my $basedomain=getTagValue($doc,"basedomain");
  my $ishomogeneous=getTagValue($doc,"isHomog");
  my $dlist=fixList(getTagValue($doc,"dlist"));
  my $llist=fixList(getTagValue($doc,"llist"));
  my $attributes=getTagValue($doc,"attributes");
  my $degree=getTagValue($doc,"degree");
  my $dim=getTagValue($doc,"dim");
  my $isoPrimeDegrees=fixList(getTagValue($doc,"isoPrimeDegrees"));
  my $isoPrimeDims=fixList(getTagValue($doc,"isoPrimeDims"));
  # Common fields
  my $comments=getValues($doc,"Comment");

  my $type="INTPS"; 
  $type="ModPS" if $basedomain; # ModPS entries
  $newid.=".Generators"  if $basedomain; # ModPS entries

  my $out=<<EOT;
 <sd:$type rdf:about="$newid" sd:createdAt="$createdAt" >
   <sd:createdBy rdf:resource="&sd;Person/$createdBy"/>
   <sd:relatedXMLResource rdf:resource="&sdxml;$type/$newid.xml"/>
EOT
  $out.=addValue("sd:hasBaseDomain",$basedomain);
  $out.=addValue("sd:hasVariables",$vars);
  $out.=addValue("sd:hasParameters",$parameters);
  $out.=addValue("sd:isHomogeneous",$ishomogeneous);
  $out.=addValue("sd:hasDegreeList",$dlist);
  $out.=addValue("sd:hasLengthsList",$llist);
  $out.=addValue("sd:hasDegree",$degree);
  $out.=addValue("sd:hasDimension",$dim);
  $out.=addValue("sd:hasIsolatedPrimesDegrees",$isoPrimeDegrees);
  $out.=addValue("sd:hasIsolatedPrimesDimensions",$isoPrimeDims);
  map { 
    $out.=addValue("rdfs:comment",$_);
  } (@$comments);

  return <<EOT;
$out 
 </sd:$type>
EOT

}

sub addValue { 
  my ($a,$b)=@_; 
  return "\n   <$a>$b</$a>" if $b; 
}

sub fixId {
  local $_=shift;
  s|INTPS/||g;
  s|/|.|g;
  s/Chou_/Chou./;
  s/IMO_/IMO./;
  s/PoSSo.Cyclic_9/Cyclic_9/;
  s/Robotic\./Robot-/;
  s/Curves.Graphs/Curves/;
  s/Curves.Generators/Curves/;
  return $_;
}

sub fixList { # convert it to comma separated list
  local $_=shift;
  s/^\s+//g;
  s/\s+$//g;
  s/\s+/,/g;
  return $_;
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
