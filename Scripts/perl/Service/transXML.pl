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

my $date="2012-12-05";
my $parser=new XML::DOM::Parser;
map action($_), @ARGV;

sub action {
  my $fn=shift;
# get the old XML item
  my $doc=$parser->parsefile($fn) or die;
  my $out=transformedFreeAlgebraData($doc->getDocumentElement);
#  print $out; return;
  open(FH,">$fn.new");
  print FH $out;
  close FH;
  print "Saved to $fn.new\n";
}

sub transformedFreeAlgebraData {
  my $doc=shift;
  my $createdAt=$doc->getAttribute("createdAt");
  $createdAt.="-01-01" if $createdAt=~/^\d+$/;
  my $createdBy="heinle";
  my $vars=fixVarname(getTagValue($doc,"vars"));
  my $parameters=getTagValue($doc,"parameters");
  my $deg=getTagValue($doc,"uptoDeg");

  my $out=<<EOT;
<?xml version="1.0"?>
<FREEALGEBRA createdAt="$createdAt" createdBy="$createdBy">
EOT
  $out.=addValue("vars",$vars);
  $out.=addValue("parameters",$parameters) if $parameters;
  $out.=addValue("uptoDeg",$deg) if $deg;
  map { 
    $out.=fixPoly($_->toString()); 
  } $doc->getElementsByTagName("basis");
  map { 
    $out.=$_->toString(); 
  } $doc->getElementsByTagName("Comment");
  map { 
    $out.=$_->toString(); 
  } $doc->getElementsByTagName("ChangeLog");
  return <<EOT;
$out 
  <ChangeLog>
    <changed at="$date" by="graebe">fixed syntax</changed>
  </ChangeLog>
</FREEALGEBRA>
EOT
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

sub fixPoly { 
  local $_=shift;
  s/\s//g;
  s/poly>/ncpoly>/g;
  return fixVarname($_);
}

sub fixVarname { 
  local $_=shift;
  s/(\w+)\((\d+)\)/$1_$2/g;
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
