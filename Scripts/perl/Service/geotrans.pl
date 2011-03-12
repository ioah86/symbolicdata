##################################################
#
# author: graebe
# createdAt: 2007-10-04 from (external) GeoTrans/newtrans.pl
#
# purpose: transform XMLData/GEO records to Data/XMLResources/GEO records
#
# usage: perl geotrans.pl file (output to stdout)
#
# version: $Id: geotrans.pl,v 1.2 2007/10/04 18:29:47 graebe Exp $


my $SD_HOME = $ENV{'SD_HOME'};
die "Environment variable SD_HOME not set" unless $SD_HOME;
use lib "$ENV{'SD_HOME'}/Scripts/perl";

use sdXML;
#use strict; # no strict since 'eval' is called

my $debug=2;
my $parser=new XML::DOM::Parser;
map action($_), @ARGV;

sub action {
  my $fn=shift;
  my $r=$parser->parsefile($fn) or die;
  return unless sdXML::getTagValue($r,"prooftype") eq "constructive";
  GeoConvert($r);
}

#############################################################
# Begin main

# Idea: 

# Call the Perl 'eval' on the (appropriately translated) GeoCode.  Each
# function call creates several elementary construction steps. Each step
# returns the id of the geometric object just constructed.

# (Elementary) construction steps are stored as cStep objects (hashes),
# containing the required information in pseudo code notation:
#    id           a unique id to identify the object
#    type         the type (Point, Line, Circle)
#    call         call(parameters) creates a representation 
#    parameters   a ListPointer to the list of parameters
#    name         optional, a name assigned via namedCStep

# cStep object id's are piled up in the (ordered) construction list @cList.

# The id Hash %idHash relates id's (anonymous cSteps) and names (named cSteps)
# to their cStep objects.

# The object Hash %objectHash relates string descriptions of existing objects
# to object id's, e.g. "Line[id12,id23]"->id35, "Line[id23,id12]"->id35 (to be
# redone since it does not identify lines with more than 2 known points)

# new idea: store incidence relations as line-point-hash $lp and
# point-line-hash $pl in the form $pl->{point}{line}=1 (two hashes for reason
# of efficient search).

# global vars

my (%idHash, %objectHash, @cList, $counter, @pnames, @pvalues, $lp, $pl);

sub GeoConvert {

  my $r=shift;
  my $id=$r->getDocumentElement->getAttribute("id");
  print "Processing $id\n" if $debug>0;
  # initialize global data 
  %idHash=%objectHash= @cList=(); $counter=1; 
  @pnames=createList(sdXML::getTagValue($r,"parameters"));

  my $s=specializeParameters($r); 

  $s.=GeoCode2PerlCode(sdXML::getTagValue($r,"Points"))."\n";
  $s.=GeoCode2PerlCode(sdXML::getTagValue($r,"coordinates"))."\n";
  $s.=GeoCode2PerlCode(sdXML::getTagValue($r,"conclusion"))."\n";
  eval $s;

  print printConstruction() if $debug>1;
  print GeogebraOutput();
}

# End main
############################################################################

############################################################################
# Subprocedures of main

sub createList {
  local $_=shift;
  return split(/\s+/);
}

sub specializeParameters {
  my $i;
  my $s="";
  for ($i=0;$i<=$#pnames;$i++)  {
    $pvalues[$i]=(rand(10)-5) unless defined $pvalues[$i];
    $s.="\$_".$pnames[$i]."=".$pvalues[$i].";\n";
  }

  print "specializeParameters returned\n$s\n" if $debug>3;
  return $s;
}

sub GeoCode2PerlCode {
  local $_=shift;

  # convert bracket and assignment notations
  s/\[/\(/gs;
  s/\]/\)/gs;
  s/(\$(\w+))\s*:=\s*(.*?);\s*/$1=namedCStep("$2",$3);\n/gs;

  # substitute parameters with Perl variables
  my $a;
  for $a (@pnames) {
    s/\b$a\b/__${a}__/gs;
    s/\$__${a}__/\$$a/gs;
    s/__${a}__/\$_$a/gs;
  }
  
  print "GeoCode2PerlCode returned\n$_\n\n" if $debug>3;
  return $_;
}

sub printConstruction {
  my $r;
  my $s="The following construction plan was generated:\n\n";
  map {
    $r=$idHash{$_};
    $s.="$r->{id} is $r->{type} $r->{call}" . "[" 
      . join(",",@{$r->{parameters}}) . "]";
    $s.=", with name $r->{name}" if defined $r->{name};
    $s.="\n";
  } (@cList);
  return $s;
}

sub createFile {
  my ($r,$s)=@_;
#  my $fn="$opt->{out}/$r->{Key}.xml";
  my $fn="$r->{Key}.xml";
  MkFilePath($fn);
  if (-e $fn) {
    print "Making backup of $fn to $fn.bak\n";
    system("cp $fn $fn.bak");
  }
  open(FH,">$fn") or die "Can't open $fn for writing: $!\n";
  print FH $s;
  close(FH);
  print "Output written to file $fn\n";
}

############################################################################
# Management of CSteps

# Available CSteps:

# dynamic elements
#     MP       m=MP[a,b]
#     SP       s=SP[u]

# construction
#     Angle    Angle[A,B,C]	(with vertex B)
#     Circle   Circle[M,A]
#     Point    CircleSlider[c,s]
#     Point    FixedLineSlider[l,u] (i.e., not sliding)
#     Point    IntersectionPoint[l_1,l_2]
#     Line     Line[A_1,A_2]
#     Point    LineSlider[l,s]
#     Point    MidPoint[A,B]  (better use FixedLineSlider ?)
#     Point    MovePoint[A,B,C]	(D such that ABCD is a parallelogram)
#     Point    OCLPoint[P,c,l]
#     Point    OCCPoint[P,c_1,c_2]
#     Line     OrthoLine[P,l]
#     Point    Point[m]
#     Segment  Segment[A_1,A_2]
#     Line     SymLine[l_1,l_2]	(with symmetry axis l_2)
#     Polygon  Triangle[A_1,A_2,A_3]

sub elementaryCStep { 
  my ($type,$call,$parameters,$aliases)=@_; 
  # $type = Type of the object (Point, Line, Circle)
  # cStep = $call(@$parameters)
  # $aliases = reference to a list of aliases on object Hash

  my ($id,$r);
  # test if CStep already exists
  map {
    $id=$objectHash{$_};
    return $id if defined $id;
  } (@$aliases);

  # create the cStep
  my $id="c_".$counter++;
  $r->{id}=$id; 
  $r->{type}=$type; 
  $r->{call}=$call; 
  $r->{parameters}=$parameters; 

  print "$id is $type " . $call . "[" . join(",",@{$parameters}) 
    . "]\n" if $debug>3;

  # commit it to @cList, %idHash and %objectHash
  push @cList, $id;
  $idHash{$id}=$r;
  map $objectHash{$_}=$id, (@$aliases);

  return $id;
}

sub namedCStep {
  my ($name,$id)=@_;
  my $truename=$name;

  # put $truename as name on the CStep object and create a new
  # entry in the id Hash.

  $idHash{$id}->{name}=$truename;
  $idHash{$truename}=$idHash{$id};
  
  print "$id got name $truename \n" if $debug>3;

  return $id;
}

sub typeTest {
  my ($id,$type)=@_;
  my $r=$idHash{$id};

  Error("No such object: $id\n") unless defined $r;

  my $ctype=$r->{type};

  Error("$id has wrong type $ctype, not $type\n") 
    unless $ctype eq $type;
}

sub on {
  my ($point, $line)=@_;
  $pl->{$point}{$line} = $lp->{$line}{$point} = 1;
}

############################################################################
# Interfacing GeoCode to ConstructionCode

#-------------------------------------A------------------------------------

sub altitude { 
  map typeTest($_,"Point"), @_;
  return ortho_line($_[0], pp_line($_[1],$_[2])); 
}

#-------------------------------------B------------------------------------

#-------------------------------------C------------------------------------

sub centroid {
  map typeTest($_,"Point"), @_;
  my ($a, $b);
  { 
    $a=median($_[0],$_[1],$_[2]);
    $b=median($_[1],$_[2],$_[0]);
  }
  return intersection_point($a, $b);
}


sub circle_slider {
  map typeTest($_,"Point"), ($_[0],$_[1]);
  my $alias=["Circle[".join(",",($_[0],$_[1]))."]"]; 
  my $c;
  { 
    $c=elementaryCStep("Circle","Circle",[$_[0],$_[1]],$alias);
  }
  $alias=["CircleSlider[".join(",",($c,$_[2]))."]"];
  return elementaryCStep("Point","CircleSlider",[$c,$_[2]],$alias);
}

sub circle_center {
  typeTest($_[0],"Circle");
  my $circle=$idHash{$_[0]};
  Error("$_[0] not a circle\n") unless $circle->{type} eq "Circle"; 
  my @p=@{$circle->{parameters}};
  return $p[0];
}

sub circle_sqradius { 
  typeTest($_[0],"Circle");
  my $circle=$idHash{$_[0]};
  Error("$_[0] not a circle\n") unless $circle->{type} eq "Circle"; 
  my @p=@{$circle->{parameters}};
  my $alias=["Segment[".join(",",@p)."]",
	    "Segment[".join(",",($p[1],$p[0]))."]"];
  elementaryCStep("Segment","Segment",[@_],$alias);
  return 0;
}

sub circumcenter {
  map typeTest($_,"Point"), @_;
  my ($a, $b);
  { $a=p_bisector($_[0],$_[1]);
    $b=p_bisector($_[1],$_[2]);
  }
  return intersection_point($a, $b);
}

sub csym_point {
  map typeTest($_,"Point"), @_;
  return fixedpoint($_[0],$_[1],-1);
}

#-------------------------------------D------------------------------------

#-------------------------------------E------------------------------------

#-------------------------------------F------------------------------------

#-------------------------------------G------------------------------------

#-------------------------------------H------------------------------------

#--------------------------------------I------------------------------------

sub intersection_point {
  map typeTest($_,"Line"), @_;
  my $alias=["IntersectionPoint[".join(",",[$_[0],$_[1]])."]",
	     "IntersectionPoint[".join(",",[$_[1],$_[0]])."]"];
  return elementaryCStep("Point","IntersectionPoint",[@_],$alias);
}  

#-------------------------------------I------------------------------------
# Prädikate zählen nicht, denn die inneren Argumente werden alle
# vor Aufruf dieser äußeren Funktion ausgewertet.

sub angle_sum { return 0; }

sub is_cc_tangent { map typeTest($_,"Circle"), @_; return 0; }

sub is_cl_tangent 
{ typeTest($_[0],"Circle"); typeTest($_[1],"Line"); return 0; }

sub is_collinear 
{ map typeTest($_,"Point"), @_; return pp_line($_[0],$_[1]); }

sub is_concurrent { map typeTest($_,"Line"), @_; return 0; }

sub is_orthogonal { map typeTest($_,"Line"), @_; return 0; }

sub is_concyclic 
{ map typeTest($_,"Point"), @_; 
  return p3_circle($_[1],$_[2],$_[3]); 
}

sub is_parallel { map typeTest($_,"Line"), @_; return 0; }

sub on_bisector { map typeTest($_,"Point"), @_; return 0; }

sub on_circle 
{ typeTest($_[0],"Point"); typeTest($_[1],"Circle"); return 0; }

sub on_line
{ typeTest($_[0],"Point"); typeTest($_[1],"Line"); return 0; }

sub l2_angle { map typeTest($_,"Line"), @_; return 0; }

#-------------------------------------K------------------------------------

#-------------------------------------L------------------------------------


sub Line { Error("Don't call Line directly!\n"); }

sub line_slider {
  typeTest($_[0],"Line");
  my $alias=["LineSlider[".join(",",@_)."]"];
  return elementaryCStep("Point","LineSlider",[@_],$alias);
}

#-------------------------------------M------------------------------------

sub median { 
  map typeTest($_,"Point"), @_;
  return pp_line($_[0],midpoint($_[1],$_[2])); 
}


sub midpoint { # midpoint now without reference to the line
  map typeTest($_,"Point"), @_;
  my $alias=["MidPoint[".join(",",[$_[0],$_[1]])."]",
	     "MidPoint[".join(",",[$_[1],$_[0]])."]"];
  #my $a=pp_line($_[0],$_[1]); 
  #return elementaryCStep("Point","MidPoint",[@_,$a],$alias);
  return elementaryCStep("Point","MidPoint",[@_],$alias);
}

sub p_bisector { 
  map typeTest($_,"Point"), @_;
  my ($a, $b);
  { $a=midpoint($_[0],$_[1]);
    $b=pp_line($_[0],$_[1]);
  }
  return ortho_line($a, $b); 
}

#-------------------------------------N------------------------------------

#-------------------------------------O------------------------------------

sub orthocenter {
  map typeTest($_,"Point"), @_;
  my ($a, $b);
  { $a=altitude($_[0],$_[1],$_[2]);
    $b=altitude($_[1],$_[2],$_[0]);
  }
  return intersection_point($a, $b);
}

sub ortho_line {
  typeTest($_[0],"Point");
  typeTest($_[1],"Line");
  my $alias=["OrthoLine[".join(",",@_)."]"];
  return elementaryCStep("Line","OrthoLine",[@_],$alias);
}

sub other_cl_point {
  typeTest($_[0],"Point");
  typeTest($_[1],"Circle");
  typeTest($_[2],"Line");
  my $alias=["OCLPoint[".join(",",@_)."]"];
  return elementaryCStep("Point","OCLPoint",[@_],$alias);
}

sub other_cc_point {
  typeTest($_[0],"Point");
  typeTest($_[1],"Circle");
  typeTest($_[2],"Circle");
  my $alias=["OCCPoint[".join(",",@_)."]",
	     "OCCPoint[".join(",",($_[0],$_[2],$_[1]))."]",];
  return elementaryCStep("Point","OCCPoint",[@_],$alias);
}

sub other_incenter {
  map typeTest($_,"Point"), @_;
  return intersection_point(ortho_line($_[1],pp_line($_[0],$_[1])),
			    ortho_line($_[2],pp_line($_[0],$_[2])));
}

#-------------------------------------P------------------------------------

sub pc_circle {
  map typeTest($_,"Point"), @_;
  my $alias=["Circle[".join(",",@_)."]"];
  return elementaryCStep("Circle","Circle",[@_],$alias);
}

sub p3_angle {
  map typeTest($_,"Point"), @_; 
  my $alias=["Angle[".join(",",($_[2],$_[1],$_[0]))."]"];
  return elementaryCStep("Angle","Angle",[@_],$alias);
}

sub p3_circle {
  map typeTest($_,"Point"), @_; 
  my $a=circumcenter(@_);
  return pc_circle($a,$_[0]);
}

sub p9_center {
  map typeTest($_,"Point"), @_;
  my ($P1,$P2,$P3,$C);
  { $P1=midpoint($_[0],$_[1]);
    $P2=midpoint($_[2],$_[1]);
    $P3=midpoint($_[2],$_[0]);
    $C=circumcenter($P1,$P2,$P3);
  }
  pc_circle($C,$P1);
  return $C;
}

sub pappus_line {
  map typeTest($_,"Point"), @_;
  my ($A,$B,$C,$D,$E,$F)=@_;
  return pp_line(intersection_point(pp_line($A,$E),pp_line($B,$D)),
		 intersection_point(pp_line($A,$F),pp_line($C,$D)));
}

sub par_point {
# par_point(A,B,C) = a point D=C-B+A, i.e., such that ABCD is a parallelogram
  map typeTest($_,"Point"), @_;
  my $alias=["MovePoint[".join(",",@_)."]",
	    "MovePoint[".join(",",($_[2],$_[1],$_[0]))."]"];
  return elementaryCStep("Point","MovePoint",[@_],$alias);
}

sub par_line {
  typeTest($_[0],"Point");
  typeTest($_[1],"Line");
  my ($A,$l)=@_;
  my $r=$idHash{$l};
  my ($B,$C)=@{$idHash{$l}->{parameters}};
  my $D=par_point($A,$B,$C);
  return pp_line($A,$D);
}

sub pedalpoint {
  typeTest($_[0],"Point");
  typeTest($_[1],"Line");
  my $a=ortho_line($_[0],$_[1]);
  return intersection_point($a,$_[1]);
}

sub Point { return elementaryCStep("Point","Point",[@_],[]); }


sub pp_line {
  map typeTest($_,"Point"), @_;
  my $alias=["Line[".join(",",@_)."]", 
	     "Line[".join(",",($_[0],$_[1]))."]"];
  my $r=elementaryCStep("Line","Line",[@_],$alias);
  return $r;
}

#-------------------------------------Q------------------------------------

#-------------------------------------R------------------------------------

#-------------------------------------S------------------------------------

sub sqrdist {
  map typeTest($_,"Point"), @_;
  my $alias=["Segment[".join(",",@_)."]",
	    "Segment[".join(",",($_[1],$_[0]))."]"];
  elementaryCStep("Segment","Segment",[@_],$alias);
  return 0;
}

sub sqrdist_pl {
  typeTest($_[0],"Point");
  typeTest($_[1],"Line");
  return sqrdist($_[0],pedalpoint($_[0],$_[1]));
}

sub sym_line {
  map typeTest($_,"Line"), @_;
  return elementaryCStep("Line","SymLine",[@_],[]);
}

sub sym_point {
  typeTest($_[0],"Point");
  typeTest($_[1],"Line");
  return fixedpoint($_[0],pedalpoint($_[0],$_[1]),2);
}

sub triangle_area {
  map typeTest($_,"Point"), @_;
  return elementaryCStep("Polygon","Triangle",[@_],[]);
}

sub varpoint {
# varpoint(A,B,u) = D=u*A+(1-u)*B
  map typeTest($_,"Point"), ($_[0],$_[1]);
  my $l=pp_line($_[0],$_[1]);
  my $alias=["LineSlider[".join(",",($l,$_[2]))."]"];
  return elementaryCStep("Point","LineSlider",[$l,$_[2]],$alias);
}

sub fixedpoint {
# varpoint(A,B,u) = D=u*A+(1-u)*B, but fixed
  map typeTest($_,"Point"), ($_[0],$_[1]);
  my $l=pp_line($_[0],$_[1]);
  my $alias=["FixedLineSlider[".join(",",($l,$_[2]))."]"];
  return elementaryCStep("Point","FixedLineSlider",[$l,$_[2]],$alias);
}

##########################################################
# GeoGebra Output

sub getGeogebraName {
  my $geogebra = 
    {
     "Line" => "Line",
     "OrthoLine" => "OrthogonalLine",
     "IntersectionPoint" => "Schneide",
     "MidPoint" => "Mittelpunkt",
    };

  return $geogebra->{shift()};
}

sub GeogebraOutput {
  my $s=geogebraPrefix();
  $s.=<<EOT;
<construction title="" author="" date="">
EOT
  my ($call, $r, $s1);
  map $s.=cstep($idHash{$_}), (@cList);
  $s.=<<EOT;
</construction>
</geogebra>
EOT
  return $s;
}

sub cstep {
  my $r=shift;
  my $s;
  my $id=$r->{id};
  # $id=$r->{name} if $r->{name};
  if ($r->{call} eq 'Point') {
    my ($x,$y)=@{$r->{parameters}};
    $s=geogebraPoint($id,$x,$y);
  } 
  else {
    $s='<command name="'.getGeogebraName($r->{call}).'">';
    my $i=0;
    my $u=join(" ", map("a".$i++."=\"$_\"", @{$r->{parameters}}));
    $s.=" <input $u/> <output a0=\"$id\"/> </command>\n";
  }
  return $s;
}

sub geogebraPoint {
  my ($l,$x,$y)=@_;
  return <<EOT;
<element type="point" label="$l">
        <show object="true" label="true"/>
        <objColor r="0" g="0" b="255" alpha="0.0"/>
        <labelMode val="0"/>
        <animation step="0.1"/>
        <fixed val="false"/>
        <breakpoint val="false"/>
        <coords x="$x" y="$y" z="1.0"/>
        <coordStyle style="cartesian"/>
        <pointSize val="3"/>
</element>
EOT
}

sub geogebraPrefix {

  return <<EOT
<geogebra format="3.0">
<gui>
  <show algebraView="true" auxiliaryObjects="false" 
     algebraInput="true" cmdList="true"/>
  <splitDivider loc="250" locVertical="400" horizontal="true"/>
  <font  size="12"/>
</gui>
<euclidianView>
  <size  width="635" height="493"/>
  <coordSystem xZero="215.0" yZero="315.0" scale="50.0" yscale="50.0"/>
  <evSettings axes="true" grid="false" pointCapturing="3" 
     pointStyle="0" rightAngleStyle="2"/>
  <bgColor r="255" g="255" b="255"/>
  <axesColor r="64" g="64" b="64"/>
  <gridColor r="192" g="192" b="192"/>
  <lineStyle axes="1" grid="10"/>
  <axis id="0" show="true" label="" unitLabel="" tickStyle="1" 
    showNumbers="true"/>
  <axis id="1" show="true" label="" unitLabel="" tickStyle="1" 
    showNumbers="true"/>
</euclidianView>
<kernel>
  <continuous val="false"/>
  <decimals val="2"/>
  <angleUnit val="degree"/>
  <coordStyle val="0"/>
</kernel>
EOT

}

1;

__END__

<command name="Line"> <input a0="A" a1="B"/> <output a0="a"/> </command>


# Changes:

# display is set for named GO to "final" and to "draft" otherwise.  Hence the
# variable $display is obsolete at this file.  This supposes that pictures
# generated for output will be postprocessed, since proof schemes contain no
# rendering information (colors, draft, etc.)


