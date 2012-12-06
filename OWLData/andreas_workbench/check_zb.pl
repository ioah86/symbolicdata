#!/usr/bin/perl

use strict;
use warnings;
use Encode;
use LWP::Simple;
use HTML::Tree;

use constant TRUE => 1;
use constant FALSE => 0;

# They array @bib will hold the bib-entries as tuples:
#         ( title, author, year, gbbref )

my @bib = ();

#&loadgbb;

my $file = "BIB.ttl";
open ARG, $file or die "File not found!";
open OUT, ">BIB-ZB.ttl";

my $count = 0;
my $unclear = 0;
my $lastlineblank = FALSE;

while (<ARG>) {
    my $line = $_;
    if ($line =~ /^sdb:/) {
        my @book;
        push @book, $line;

        my $title = '';
        my $author = '';
        my $year = '';

        while(<ARG>) {       
            push @book, $_;

            if ($_ =~ /sd:hasTitle/) {
                $title = ($_ =~ /"([^"]*)"/)[0];
                $title =~ s/&[^&;]*;/.{1,2}/g;
                $title =~ s/;.*//g;
            }
            if ($_ =~ /sd:hasAuthor/) {
                $author = ($_ =~ /sdp:([^,;_]*)[_,;]/)[0];
            }     
            if ($_ =~ /sd:hasYear/) {
                $year = ($_ =~ /"(.*)"/)[0];;
            }

            last if /\.\s*$/;
        }

        print $book[0];
        print $title , "\n";
        print $author, "\n";        
        print $year , "\n";
        
        my @result = &queryzentralblatt($author, $title);

        if ($#result == -1) {
            print "==> nothing found\n\n";
        }
        elsif ($#result == 0) {
            print "==> unique hit\n\n";
            print encode('UTF-8', $result[0][0]), "\n";
            print encode('UTF-8', $result[0][1]), "\n";
            print OUT ($book[0]);                    
            print OUT "    sd:hasZBentry <http://www.zentralblatt-math.org/zmath/en/search/" , encode('UTF-8', $result[0][2]), "> .\n\n";
            $count++;
        }
        else {
            print "==> multiple hits\n\n";
            foreach my $i (0 .. $#result) {
                print "  (", $i+1, ") ", encode('UTF-8', $result[$i][0]), "\n";
                print "      ", encode('UTF-8', $result[$i][1]), "\n";
                print "\n";
            }
            print "\nEnter the number(s) if the book is found, else just hit enter: ";
                chomp(my $manual = <STDIN>);
                print "\n";

                foreach my $n (split(//, $manual)) {
                    if (($n >= 1) && ($n <= $#result+1)) {
                        print OUT ($book[0]);                    
                        print OUT "    sd:hasZBentry <http://www.zentralblatt-math.org/zmath/en/search/" , encode('UTF-8', $result[$n-1][2]), "> .\n\n";
                        
                        $count++;
                    }
                }
        }
        print "\n";
    }
    else {
        print OUT $line unless ($lastlineblank and $line eq "\n");
        if ($line eq "\n") { $lastlineblank = TRUE; }
        else { $lastlineblank = FALSE; }
    }  
}

print OUT "\n";
print "\n$count entries also found in Zentralblatt data base.\n";

close ARG;
close OUT;

exit 0;

# --- subroutines

# Query the gbb by passing 3 arguments where the first argument will be
# matched against the title, the second against the author and the third
# against the year. All parameters can be regex expressions.

sub queryzentralblatt {
    (my $author, my $title) = @_[0..1];

    $author =~ s/(^[A-Za-z]*).*$/$1/;
    # for some reason these do not work as expected :(
    #$title =~ tr/\x{e4}\x{f6}\x{fc}\x{c4}\x{d6}\x{dc}/aouAOU/;
    #$title =~ tr/äöüÄÖÜ/aouAOU/;
    $title =~ s/ä/a/g;
    $title =~ s/ö/o/g;
    $title =~ s/ü/u/g;
    $title =~ s/Ä/A/g;
    $title =~ s/Ö/O/g;
    $title =~ s/Ü/U/g;
    $title =~ s/[^A-Za-z]+/ /g;
    # delete short words as irrelevant
    # not useful for zentralblatt!
    #$title =~ s/\b[A-Za-z]{0,3}\b//g;
    $title =~ s/^\s*//;
    $title =~ s/\s\s*/ /g;
    # get the first 7 words (too many words often produce no hit)
    $title =~ s/^(([^\s]*\s?){0,7}).*$/$1/g;
    $title =~ s/\s/+/g;

    my $content = get("http://www.zentralblatt-math.org/zmath/en/search/?q=ti:%22$title%22+au:$author");

    print "--- SEARCHING ---\n";
    print "Author: $author\n";
    print "Title : $title\n";
    print "With  : http://www.zentralblatt-math.org/zmath/en/search/?q=ti:%22$title%22+au:$author\n\n";

    my @result = ();

    if (not ($content =~ "Your query produces no results.")) {
        my @hits = grep(/href="\?q=an/, (split /\n/, $content));    

        foreach my $res (@hits) {
            my @parse = split(/<br>/, $res);
            # remove tags        
            map $_ =~ s/<[^>]+>//g, @parse;
            # remove leading spaces
            map $_ =~ s/^\s*//g, @parse;
            # capture link to entry
            my $link = ($res =~ /href="([^"]*)"/)[0];

            push @result, [$parse[0], $parse[1], $link];
            #print encode('UTF-8', $parse[0]), "\n";
            #print encode('UTF-8', $parse[1]), "\n";
            #print "$link\n\n";
        }
    }

    return @result;
}

