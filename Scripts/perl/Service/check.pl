##################################################
#
# author: graebe
# createdAt: 2010-12-27

# check an RDF file 

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;

use strict;
use XML::DOM;

my $hash;
my $reversehash;
my $rdfFile="$SD_HOME/OWLData/PolynomialSystems.rdf";
my $parser=new XML::DOM::Parser;
getRDFData();
# action1();
map action($_), @ARGV;

sub action {
# check if data are cited as sd:relatedXMLResource 
  my $fn=shift;
  my $id=$reversehash->{$fn};
  # print "$fn has $id\n" if $id;
  print "$fn is missing\n" unless $id;
}

sub action1 {
# check if a sd:relatedXMLResource is really in OWLData/XMLResources
  map { 
    my $src=$hash->{$_};
    # print "\$src is $src\n";
    print <<EOT unless (-e $src);
$_ -- related resource is missing: $src
EOT
  } (keys %$hash);
}

sub getRDFData {
# fill $hash->{rdf:about}=XMLResource and $reversehash
  my $doc=$parser->parsefile($rdfFile) or die;
  map { 
    my $id=$_->getAttribute("rdf:about");
    my $src=getXMLResource($_,$id);
    $hash->{$id}=$src if $src;
  } $doc->getElementsByTagName("sd:INTPS");
  map { 
    my $src=$hash->{$_};
    $reversehash->{$src}=$_;
  } (keys %$hash);
}

sub getXMLResource {
  my ($node,$id)=@_;
  map { 
    my $src=$_->getAttribute("rdf:resource");
    $src=~s|http://www.symbolicdata.org|$SD_HOME/OWLData|gs;
    return $src;
  } $node->getElementsByTagName("sd:relatedXMLResource");
}

sub mytest {
  my ($id,$src)=@_;
  print <<EOT unless (-e $src);
$id -- related resource is missing: $src
EOT
}

