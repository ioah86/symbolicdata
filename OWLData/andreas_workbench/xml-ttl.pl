#!/usr/bin/perl

use warnings;
use strict;

open TTL, "../FreeAlgebra.ttl" or die "File $ARGV[0] not found!";
my @pols = ();

while (my $line = <TTL>) {
    if ($line =~ m!^<.*/([^/]*)>!) {
        push @pols, $1;
    }
}

close TTL;

for my $file (glob "../XMLResources/FREEALGEBRA/*.xml") {
    $file =~ m!.*/([^/]*)\.xml$!;    
    if ($1 ~~  @pols) {
        print "$1 --> found\n";
    }
    else {
        print "$1 --> not found\n";
    }
}


