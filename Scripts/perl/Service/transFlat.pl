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

my $rdffile="$SD_HOME/OWLData/PolynomialSystems.rdf";
my $parser=new XML::DOM::Parser;
my $rdf=$parser->parsefile($rdffile) or die;
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
  my $rdfentry=getRDFEntry($newid);

  unless ($rdfentry) {
    print "$id -> $newid has no RDF Entry\n";
    return;
  }
  my $ref=$rdfentry->getAttribute("rdf:about");

  # INTPS specific
  my $vars=fixList(getTagValue($doc,"vars"));
  my $parameters=fixList(getTagValue($doc,"parameters"));
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
  my $comment=getTagValue($doc,"Comment");

  my $type="INTPS"; 
  $type="ModPS" if $basedomain; # should be processed differently

  my $out=<<EOT;
 <sd:$type rdf:about="$newid.Flat" sd:createdAt="$createdAt" >
   <sd:createdBy rdf:resource="&sd;Person/$createdBy"/>
   <sd:relatedINTPSEntry rdf:resource="$ref"/>
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

  # map { $out.=addValue("rdfs:comment",$_); } (@$comments);

  return <<EOT;
$out 
   <rdfs:comment>Flat variant of $ref</rdfs:comment>
 </sd:$type>
EOT

}

sub addValue { 
  my ($a,$b)=@_; 
  return "\n   <$a>$b</$a>" if $b; 
}

sub getRDFEntry { 
  my $id=shift; 
  map {
    return $_ if $_->getAttribute("rdf:about") eq $id;
  } $rdf->getElementsByTagName("sd:INTPS");
  return;
}

sub fixId {
  local $_=shift;
  s|INTPS/Flat/||g;
  s|/|.|g;
  s/Chou_/Chou./;
  s/IMO_/IMO./;
  s/PoSSo.Cyclic_9/Cyclic_9/;
  s/Robotic\./Robot-/;
  s/Curves.Graphs/Curves/;
  return $_;
}

sub fixList { # convert it to comma separated list
  local $_=shift;
  s/^\s+//g;
  s/\s+$//g;
  s/\s+/,/g;
  return $_;
}

sub addValue { 
  my ($a,$b)=@_; 
  return "\n   <$a>$b</$a>" if $b; 
}

sub getRDFEntry { 
  my $id=shift; 
  map {
    return $_ if $_->getAttribute("rdf:about") eq $id;
  } $rdf->getElementsByTagName("sd:INTPS");
  return;
}

sub fixId {
  local $_=shift;
  s|INTPS/Flat/||g;
  s|/|.|g;
  s/Chou_/Chou./;
  s/IMO_/IMO./;
  s/PoSSo.Cyclic_9/Cyclic_9/;
  s/Robotic\./Robot-/;
  s/Curves.Graphs/Curves/;
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
