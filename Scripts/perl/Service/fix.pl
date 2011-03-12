##################################################
#
# author: graebe
# createdAt: 2006-03-04

# purpose: fix entries in an XML tree

my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use XML::DOM;
use XML;
use strict;

my $parser=new XML::DOM::Parser;

map action($_), @ARGV;

sub action {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;

  map {
    XML::saveOWLFile($doc) if fix1($doc,$_); 
  } $doc->getElementsByTagName("Comment");

}

sub fix1 {
  my ($doc,$node)=@_;
  return unless XML::getValue($node);
  my $u=XML::createNode($doc,"<Comment/>");
  $node->getParentNode->replaceChild($u,$node);
}

sub fix {
  my $node=shift;
  my $r=$node->getAttribute("resource");
  $r=~s/sdxml://;
  $r="sdxml:INTPS/$r.xml";
  $node->removeAttribute("resource");
  $node->setAttribute("url",$r);
  return 1;
}

