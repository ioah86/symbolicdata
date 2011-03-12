##################################################
#
# author: graebe
# createdAt: 2010-12-22

# purpose: transform Person Records to RDF Data

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
  <!ENTITY foaf "http://xmlns.com/foaf/0.1/">
  <!ENTITY sd "http://hgg.ontowiki.net/SymbolicData/">
  <!ENTITY owl "http://www.w3.org/2002/07/owl#">
  <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#">
  <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">
]>

<rdf:RDF xml:base="&sd;Person/"
  xmlns:foaf="&foaf;"
  xmlns:sd="&sd;"
  xmlns:owl="&owl;"
  xmlns:rdf="&rdf;"
  xmlns:rdfs="&rdfs;"
  xmlns:xsd="&xsd;">

<!-- Ontology specific informatx1ions -->
  <owl:Ontology rdf:about="&sd;Person/"
    rdfs:label="SD Person Data">
    <rdfs:comment>A first draft</rdfs:comment>
  </owl:Ontology>

<!-- Classes -->

  <owl:Class rdf:about="&foaf;Person"/>

<!-- Instances and untyped data -->

EOT

}

sub transformedData {
  my $doc=shift;

  # The Header
  my $id=$doc->getAttribute("id");
  my $newid=fixId($id);
  my $createdAt=$doc->getAttribute("createdAt");

  # PERSON specific
  my $name=getTagValue($doc,"name");
  my $address=fixText(getTagValue($doc,"address"));
  my $contribution=fixText(getTagValue($doc,"contribution"));
  my $email=getTagValue($doc,"email");
  my $location=getTagValue($doc,"location");
  my $status=fixText(getTagValue($doc,"status"));
  my $url=getTagValue($doc,"url");

  # Common fields
  my $comments=getValues($doc,"Comment");

  my $out=<<EOT;
 <foaf:Person rdf:about="$newid" rdfs:label="$name">
EOT
  $out.=addValue("sd:hasAddress",$address);
  $out.=addValue("sd:hasContributed",$contribution);
  $out.=addValue("sd:hasEmail",$email);
  $out.=addValue("sd:hasAffiliation",$location);
  $out.=addValue("sd:hasStatus",$status);
  $out.=addValue("sd:lastModified","2004-08-26");
  $out.=addValue("sd:hasURLLiteral",$url);
  map { 
    $out.=addValue("rdfs:comment",$_);
  } (@$comments);

  return <<EOT;
$out 
 </foaf:Person>
EOT

}

sub addValue { 
  my ($a,$b)=@_; 
  return "\n   <$a>$b</$a>" if $b; 
}

sub fixId {
  local $_=shift;
  s|PERSON/||g;
  return $_;
}

sub fixText {
  local $_=shift;
  s|&lt;br&gt;|, |g;
  s|&lt;b&gt;||g;
  s|&lt;/b&gt;||g;
  s|\n|, |gs;
  s|\s+| |gs;
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

