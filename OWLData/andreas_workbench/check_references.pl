#!/usr/bin/perl

use warnings;

%local_ttl = ('sdp' => 'Person.ttl');
%ttl_data = ();

if($#ARGV == -1) {
    print "Please specify file to work with."
}

open ARG, $ARGV[0] or die "File $ARGV[0] not found!";
open MYFILE, ">output-$ARGV[0]";

while(($key, $value) = each(%local_ttl)) {
    print "Loading $value\n";
    open FILE, $value or die;
    chomp(@file = <FILE>);
    @{$ttl_data{$key}} = grep(/^\<http:/, @file);

    foreach $item (@{$ttl_data{$key}}) {
        $item =~ s/^.*\/([^\/]*)\>/$1/;
    }

    close FILE    
}

$count = 0;
$replaces = 0;

foreach $line (<ARG>) {
    $count++;
    $newline = $line;
    
    foreach $key (keys %ttl_data) {
        while ($line =~ /$key:([^\s,;]*)/g) {
            # checking if used object is in namespace $key
            # smartmatch ~~ requires Perl > 5.10.1
            # print "Checking $1\n";
            if (not($1 ~~ @{$ttl_data{$key}})) {
                # looking for fix, taking an initial piece of the used object
                $test = $1;
                $test =~ s/^([A-Za-z]*).*$/$1/;
                # print "Testing with $test\n";
                @matches = grep(/$test/i, @{$ttl_data{$key}});
                # matches == 0  iff.  exactly one match found
                if($#matches == 0) {
                    print "line $count : $key:$test => $key:$matches[0]\n";
                    $newline =~ s/$key:$test[^\s;,.]*/$key:$matches[0]/;
                    $replaces++;
                }
                elsif($#matches == -1) {
                    print "No match found for \"$test\" (line $count)\n";
                }
                else {
                    print "No unambiguous match found for \"$test\" (line $count)\n";
                }
            }
        }
    }
    print MYFILE $newline;
}

close MYFILE;

print "Done. $replaces replaces have been made.\n"
