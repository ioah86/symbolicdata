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
open OUT, ">BIB-CS.ttl";

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

        print $book[0], "\n";
        print $title , "\n";
        print $author, "\n";        
        print $year , "\n";
        
        my $result = &queryciteseer($author, $title);
        
        if ($result) {
            print OUT ($book[0]);                    
            print OUT "    sd:hasCSentry <" , encode('UTF-8', $result), "> .\n\n";
            $count++;
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
print "\n$count entries also found in Cite Seer data base.\n";

close ARG;
close OUT;

exit 0;

# --- subroutines

# Query the gbb by passing 3 arguments where the first argument will be
# matched against the title, the second against the author and the third
# against the year. All parameters can be regex expressions.

sub queryciteseer {
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
    $title =~ s/\b[A-Za-z]{0,3}\b//g;
    $title =~ s/^\s*//;
    $title =~ s/\s\s*/ /g;
    # get the first 7 words (too many words often produce no hit)
    $title =~ s/^(([^\s]*\s?){0,7}).*$/$1/g;
    $title =~ s/\s/+/g;

    my $content = get("http://citeseer.ist.psu.edu/search?q=title%3A($title)+AND+author%3A$author&sort=cite&t=doc");
    my $tree = HTML::Tree -> new();
    $tree -> parse($content);

    my @result = $tree -> look_down(_tag => 'div', id => "result_list");

    print "--- SEARCHING ---\n";
    print "Author: $author\n";
    print "Title : $title\n";
    print "--- RESULT (as HTML) ---\n";
    print $result[0] -> as_HTML, "\n";

    my $html = $result[0] -> as_HTML;
    my $result = undef;

    if ($html =~ 'class="result"') {
        print "--- EXTRACTED LINK ---\n";
        $result = ($html =~ /href="([^"]*)"/)[0];
        # erase session id
        $result =~ s/;jsessionid.*\?/?/;
        $result = "http://citeseer.ist.psu.edu" . $result;
        print "$result\n";
    }
    print "--- RESULT-END ---\n";
    return $result;
}

