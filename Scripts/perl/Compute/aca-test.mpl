resubst:=proc(sol, polys) 
  map(sol, u -> simplify(subs(polys, u))) end proc;

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
