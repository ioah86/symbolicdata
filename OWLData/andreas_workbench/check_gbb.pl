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

&loadgbb;

my $file = "BIB.ttl";
open ARG, $file or die "File not found!";
open OUT, ">BIB-GBB.ttl";

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
        
        my @result = &querygbb($title, $author, $year);
        my $add_this = undef;
        if ($#result == 0) {
            print " ==> Found!  ";
            print encode('UTF-8', $result[0][0]), "\n";
            print " ==> sd:hasGBBentry <http://www.risc.jku.at/Groebner-Bases-Bibliography/" , encode('UTF-8', $result[0][3]), ">; .\n\n";

            print OUT ($book[0]);
            print OUT "    sd:hasGBBentry <http://www.risc.jku.at/Groebner-Bases-Bibliography/" , encode('UTF-8', $result[0][3]), "> .\n\n";
            $count++;
        }
        # if a book is not find by author, title, and year, but there are
        # entries matching author and year, show the titles and let the user
        # decide
        else {
            my @result = &querygbb(".", $author, $year);
            if (@result) {
                print " ==> might exist in GBB, check manually\n\n";
                foreach my $i (0 .. $#result) {
                    print "      (", $i+1, ") " ,  encode('UTF-8', $result[$i][0]), "\n";
                }
                print "\nEnter the number(s) if the book is found, else just hit enter: ";
                chomp(my $manual = <STDIN>);
                print "\n";

                foreach my $n (split(//, $manual)) {
                    if (($n >= 1) && ($n <= $#result+1)) {
                        print " ==> Adding: ";
                        print encode('UTF-8', $result[$n-1][0]), "\n";
                        print " ==> sd:hasGBBentry <http://www.risc.jku.at/Groebner-Bases-Bibliography/" , encode('UTF-8', $result[$n-1][3]), ">.\n\n";

                        print OUT ($book[0]);                    
                        print OUT "    sd:hasGBBentry <http://www.risc.jku.at/Groebner-Bases-Bibliography/" , encode('UTF-8', $result[$n-1][3]), "> .\n\n";
                        $count++;
                    }
                }
            }
            $unclear++;
        }
        print "\n";
    }
    else {
        print OUT $line unless ($lastlineblank and $line eq "\n");
        if ($line eq "\n") { $lastlineblank = TRUE; }
        else { $lastlineblank = FALSE; }
    }  
}

print "\n$count entries also found in GBB.\n";

close ARG;
close OUT;

exit 0;

# --- subroutines

# Query the gbb by passing 3 arguments where the first argument will be
# matched against the title, the second against the author and the third
# against the year. All parameters can be regex expressions.

sub querygbb {
    my @p = map decode('UTF-8', $_), @_;
    my @result = grep { ($_->[0] =~ /$p[0]/i) && ($_->[1] =~ /$p[1]/) && ($_->[2] =~ /$p[2]/) } @bib;
}

# Load the gröbner bases bibliography from disk (if it is there) or directly
# from the web.

sub loadgbb {
    my $gbb = 'gbb.html';
    my $content = undef;

    if (-e $gbb) {
        print "Reading Gröbner Bases Bibliography from disk\n";
        open GBBFILE, '<', $gbb;
        local $/;
        $content = <GBBFILE>;
    }
    else {
        print "Downloading Gröbner Bases Bibliography\n";
        open GBBFILE, ">$gbb";
        $content = get('http://www.risc.jku.at/Groebner-Bases-Bibliography/do_search.php?query_option1=&search_title=&search_author=-1&search_type=-1&search_keywords=&search_on=0&viewoption=0') or die 'Unable to get page';
        print GBBFILE encode('UTF-8', $content);
        close GBBFILE;
    }
    $content = decode('UTF-8', $content);

    my $tree = HTML::Tree -> new();
    $tree -> parse($content);

    my @tables = $tree -> look_down(_tag => 'table');
    my $table = $tables[4];
    my @tds = $table -> look_down(_tag => 'td');
    my @books = map { $_ -> as_text } @tds;
    my @links = map { $_ -> as_HTML } @tds;

    for(my $i=0; $i < $#books; $i+=10) {
        $books[$i+2] =~ s/[Gg]roe?bner/Gr\x{00F6}bner/g;
        $links[$i+2] =~ /href="(.*)"/;
        push(@bib, [@books[$i+2, $i+3], $books[$i+1], $1]);
    }
}
