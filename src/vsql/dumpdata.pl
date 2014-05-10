##################################
#
# author: graebe
# createdAt: 2013-08-25
# lastModified: 2013-08-25

# purpose: create dumps of Graphs as sorted ntriples via Sparql query.
# usage: perl dumpdata.pl

# Note that this mechanism is restricted by the size

use strict;
use SparqlQuery;

saveGraphAsSortedNtriples("Annotations","Annotations.n3");
saveGraphAsSortedNtriples("Bibliography","Bibliography.n3");
saveGraphAsSortedNtriples("FreeAlgebras","FreeAlgebras.n3");
saveGraphAsSortedNtriples("GAlgebras","GAlgebras.n3");
saveGraphAsSortedNtriples("GeoCode","GeoCode.n3");
saveGraphAsSortedNtriples("GeometryProblems","GeometryProblems.n3");
saveGraphAsSortedNtriples("GeoProofSchemes","GeoProofSchemes.n3");
saveGraphAsSortedNtriples("People","People.n3");
saveGraphAsSortedNtriples("PolynomialSystems","PolynomialSystems.n3");
saveGraphAsSortedNtriples("Systems","Systems.n3");
saveGraphAsSortedNtriples("TestSets","TestSets.n3");

## end main ##

sub getGraph { # get a whole Graph by a construct query
  my $graphname=shift;
  my $query=<<EOT;
construct { ?s ?p ?o } 
from <http://symbolicdata.org/Data/$graphname/> 
where {?s ?p ?o}
EOT
  my $res=SparqlQuery::query($query);
  return $res;
}

sub saveGraphAsSortedNtriples {
  my ($graph,$target)=@_;
  open(FH,">/tmp/sdtmp.1");
  print FH getGraph($graph);
  close FH;
  system("rapper -i turtle -o ntriples /tmp/sdtmp.1 | sort > /tmp/sdtmp.2");
  system("mv /tmp/sdtmp.2 $target");
  print "Graph $graph saved as $target\n";
}

__END__

Requires to define this isql-vt function in advance

create procedure graph_to_ttl_file (in graph_iri varchar, in f_name varchar)
{ declare ses any; 
  ses := string_output(); 
  DB.DBA.RDF_GRAPH_TO_TTL (graph_iri, ses); 
  string_to_file (f_name, ses, 0); 
}

Note that f_name is owned by the Virtuoso process owner, not the user who
calls that function.


sparql construct { ?s ?p ?o .} from <http://symbolicdata.org/Data/People/> where {?s ?p ?o};

graph_to_ttl_file('http://symbolicdata.org/Data/People/', '/tmp/People.ttl');


