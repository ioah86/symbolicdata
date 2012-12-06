/* this script does no more work for MuPAD 4.0 due to the new vector format
used in a quite unpredictable way */

resubst:=proc(sol,polys)
begin map(sol,u->simplify(subs(subs(polys,u),u))); end:
// double subs due to Backsubstitution avoided in solve

myBenchmarkFunction:=proc(u) local example,vars,polys,sol,tt;
begin
  example:=subs(theExample,u);
  vars:=subs(theVars,u);
  polys:=subs(thePolys,u);
  print(NoNL,"\n\nSolve: ".example);print();
  if traperror((tt:=time((sol:=solve(polys,vars)))),2)>0 then 
    print(NoNL,"\nInterrupted"); 
    return([example,0,FALSE]);
  else
    print(NoNL,"\nElapsed time: ".tt);
    print(NoNL,"\nResult: ".sol);
    print(NoNL,"\nResubstitution: ".resubst(sol,polys));
  end_if;
  return([example,tt,TRUE]);
end:
