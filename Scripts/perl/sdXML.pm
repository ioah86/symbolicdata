#########################################################
#
# author: graebe
# date: 2006-03-02
#
# purpose: additional support to manage the special XML documents in
#          this collection

package sdXML;
use XML::DOM;
use strict;

# ============ global settings for this package
my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
my $parser=new XML::DOM::Parser;
my $owldir="$SD_HOME/NewData/OWLResources";


# ============ useful XML shortcuts
sub getTagValue {
  my ($doc,$tag)=@_;
  map { return getValue($_);} $doc->getElementsByTagName($tag);
  return;
}

sub getValue {
  my $node=shift;
  local $_=$node->toString(1);
  s/^\s*<[^>]*?>\s*//s;
  s/\s*<\/[^>]*?>\s*$//s;
  s.&lt;/b&gt;..gs;
  s.&lt;b&gt;..gs;
  s.&lt;br&gt;.\n.gs;
  return $_;
}

# create a node for that document from an xml chunk
sub createNode {
  my ($doc,$xml)=@_;
  my $u=$parser->parse($xml);
  $u=$u->getDocumentElement;
  $u->setOwnerDocument($doc);
  return $u;
}

sub appendNode {
  my ($doc,$tag,$value)=@_;
  my $u=createNode($doc,"<$tag>$value</$tag>");
  $doc->getDocumentElement->appendChild($u);
}

# ============ useful tasks for an OWL record
sub addToChangeLog {
  my ($doc,$by,$at,$text)=@_;
  my $u=createNode($doc,<<EOT);
<changed at="$at" by="$by">$text</changed>
EOT
  map $_->appendChild($u), $doc->getElementsByTagName("ChangeLog");
}

sub getEmptyCopy {
  my $fn=shift;
  my $doc=$parser->parsefile($fn) or die;
  my $root=$doc->getDocumentElement;
  map $root->removeChild($_), $root->getChildNodes;
  $root->appendChild($doc->createComment(" \$"."Id:\$ "));
  return $doc;
}

# $id = id of the Annotation to add the note
# $text = text to be added to the existing note
# $crefs = listref of OWL and XML xml statements
sub getAnnotationHandle {
  my ($id,$date,$nickName)=@_;
  my $doc=$parser->parse(<<EOT); # create new handle
<?xml version="1.0"?>
<Annotation createdAt="$date" createdBy="$nickName" id="$id">
<!-- \$Id: sdXML.pm,v 1.1 2007/10/04 12:51:11 graebe Exp $ -->
<note/>
  <relatesTo/>
  <Comment/>
  <ChangeLog/>
</Annotation>
EOT
# now look for an existing one
  my $fn="$owldir/Annotation/$id.xml";
  if (-e $fn) { $doc=$parser->parsefile($fn) or die; }
  return $doc;
}

sub addNote {
  my ($doc,$text,$crefs,$date,$nickName)=@_;
  map {
    $text=getValue($_)."\n\n".$text;
    $text=~s/^\s+//s;
    $text=~s/\n\n+/\n\n/s;
    my $u=createNode($doc,"<note>$text</note>");
    $_->getParentNode->replaceChild($u,$_);
  } $doc->getElementsByTagName("note");
  map {
    for my $a (@$crefs) {
      $_->appendChild(createNode($doc,$a));
    }
  } $doc->getElementsByTagName("relatesTo");
  
  #addToChangeLog($doc,$nickName,$date,"added information");
}

# ============ save and print a record
sub saveXMLFile {
  my ($doc,$fn)=@_;
  $doc->printToFile("/tmp/uhu.xml",1); 
  system("cp $fn $fn.bak") if -e $fn; 
  system("xmllint --format /tmp/uhu.xml >$fn"); 
  print "XML resource written to $fn\n";
}

sub saveOWLFile {
  my ($doc)=@_;
  my $id=$doc->getDocumentElement->getAttribute("id");
  my $class=$doc->getDocumentElement->getTagName;
  $doc->printToFile("/tmp/uhu.xml",1);
  my $fn="$owldir/$class/$id.xml";
  system("cp $fn $fn.bak") if -e $fn; 
  system("xmllint --format /tmp/uhu.xml >$fn");  
  print "result written to $fn\n";
}

sub showDocument {
  my $doc=shift;
  print $doc->toString(1);
  print "=" x 60 ."\n";
}

1; # must be the last line
