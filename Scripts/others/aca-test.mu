resubst:=proc(sol,polys)
begin map(sol,u->simplify(subs(subs(polys,u),u))); end:
// double subs due to Backsubstitution avoided in solve


myBenchmarkFunction:=proc(u) local example,vars,polys,sol,tt;
begin
  example:=subs(theExample,u);
  vars:=subs(theVars,u);
  polys:=subs(thePolys,u);
  print(NoNL,"Solve: ".example);print();
  if traperror(
     (tt:=time((sol:=solve(polys,vars)))),
     2)>0 then print(NoNL,"Interrupted");print(); return();
  else
  print(NoNL,"Elapsed time: ".tt);print();
  print(NoNL,sol);print();
  print(NoNL,resubst(sol,polys));print();
  end_if;
end:
