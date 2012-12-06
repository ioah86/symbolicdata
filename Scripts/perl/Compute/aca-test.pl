##################################
#
# author: graebe
# createdAt: 2006-03-03
# lastUpdate: 2012-11-26

# purpose: Demonstration how a benchmark could be set up. Works for examples
# given directly by an INTPS XMLResource.

# best to define this environment variable
die unless defined $ENV{'SD_HOME'};

use strict;
use XML::DOM; # A convenient perl DOM Parser package 

#### start main: create benchmark output for a special system.

my $parser=new XML::DOM::Parser;
my $xmldir="$ENV{'SD_HOME'}/OWLData/XMLResources/INTPS";
my $zeroDimensionalExamples=
    ["Sym1_211", "Katsura_4", "Sym1_311", "Cyclic_5", "Sym1_321", 
     "Katsura_5"]; 

print createOutputforMuPAD($zeroDimensionalExamples);

# === end main ===

sub createOutputforMuPAD {
    my $listOfExamples=shift;
    my $theExamples=join(",\n",map(getExample($_), @$listOfExamples));
    my $out=<<EOT;
// Startup
read("aca-test.mu"):

// make a list of all examples to be processed
theExamples:=[$theExamples]:

// Run the examples using a specially defined run function
// within the CAS that encapsulates all data and produces all
// output information.

map(theExamples, myBenchmarkFunction);

quit;
EOT
}

sub createOutputforMaple {
    my $listOfExamples=shift;
    my $theExamples=join(",\n",map(getExample($_), @$listOfExamples));
    my $out=<<EOT;
read("aca-test.mpl");
theExamples:=[$theExamples];
map(theExamples, myBenchmarkFunction);
quit;
EOT
}

sub getExample {
    my $name=shift;
    my $doc=$parser->parsefile("$xmldir/$name.xml") or die;
    my $vars=join(",",getTagValue($doc,"vars"));
    my $polys=join(",\n",getPolys($doc));
    return <<EOT;
[theExample = "$name",
 theVars=[$vars],
 thePolys=[
$polys
       ]]
EOT
}

sub getPolys {
    my ($doc)=@_;
    my @l;
    map { push(@l, getValue($_));} $doc->getElementsByTagName("poly");  
    return @l;
}

sub getTagValue {
    my ($doc,$tag)=@_;
    map { return getValue($_);} $doc->getElementsByTagName($tag);  
}

sub getValue {
    my $node=shift;
    local $_=$node->toString(1);
    s/^\s*<[^>]*?>\s*//s;
    s/\s*<\/[^>]*?>\s*$//s;
    return $_;
}
