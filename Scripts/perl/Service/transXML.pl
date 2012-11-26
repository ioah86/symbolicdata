##################################################
#
# Authox: graebe
# createdAt: 2010-12-22
# lastUpdate:

# purpose: transform XMLData descriptions to XMLResource Data

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;

use XML::DOM;
use strict;

my $date="2010-12-27";
my $parser=new XML::DOM::Parser;
map action($_), @ARGV;

sub action {
  my $fn=shift;
# get the old XML item
  my $doc=$parser->parsefile($fn) or die;
  my $out=transformedGAlgebraData($doc->getDocumentElement);
  print $out;
}

sub transformedINTPSData {
  my $doc=shift;

  # The Header
  my $createdAt=$doc->getAttribute("createdAt");
  my $createdBy=$doc->getAttribute("createdBy");
  my $id=$doc->getAttribute("id");

  # INTPS specific
  my $vars=fixList(getTagValue($doc,"vars"));
  my $parameters=fixList(getTagValue($doc,"parameters"));
  $vars.=",$parameters" if $parameters;

  my $out=<<EOT;
<?xml version="1.0"?>
<INTPS createdAt="$createdAt" createdBy="$createdBy">
<!-- \$Id: transXML.pl,v 1.3 2010/12/31 17:42:06 graebe Exp $ -->
EOT
  $out.=addValue("vars",$vars);
  map { 
    $out.=$_->toString(); 
  } $doc->getElementsByTagName("basis");
  map { 
    $_->toString(); 
  } $doc->getElementsByTagName("Comment");
  map { 
    $out.=$_->toString(); 
  } $doc->getElementsByTagName("ChangeLog");
  return <<EOT;
$out 
  <ChangeLog>
    <changed at="$date" by="graebe">compiled from XMLData $id</changed>
  </ChangeLog>

</INTPS>
EOT
}

sub transformedGAlgebraData {
  my $doc=shift;

  # The Header
  my $createdAt=$doc->getAttribute("createdAt");
  my $createdBy=$doc->getAttribute("createdBy");
  my $id=$doc->getAttribute("id");

  # GAlgebra specific
  my $vars=fixList(getTagValue($doc,"vars"));
  my $parameters=fixList(getTagValue($doc,"parameters"));
  my $commutators=cprocess(getTagValue($doc,"commutators"));

  my $out=<<EOT;
<?xml version="1.0"?>
<GAlgebra createdAt="$createdAt" createdBy="$createdBy">
EOT
  $out.=addValue("vars",$vars);
  $out.=addValue("parameters",$parameters) if $parameters;
  $out.=addValue("commutators",$commutators);
  map { 
    $out.=$_->toString(); 
  } $doc->getElementsByTagName("basis");
  map { 
    $out.=$_->toString(); 
  } $doc->getElementsByTagName("ChangeLog");
  return <<EOT;
$out 
  <ChangeLog>
    <changed at="$date" by="graebe">compiled from XMLData $id</changed>
  </ChangeLog>

</GAlgebra>
EOT
}

sub cprocess {
  local $_=shift;
  s/\[\s*//g;
  s/\s*\]//g;
  my $out;
  map {
    m/(\w)(\d):(\d)=(\S+)/;
    $out.=<<EOT;
<$1 first="$2" second="$3">$4</$1>
EOT
  } (split /\s*,\s*/);
  return $out;
}

sub addValue { 
  my ($a,$b)=@_; 
  return "\n   <$a>$b</$a>" if $b; 
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
