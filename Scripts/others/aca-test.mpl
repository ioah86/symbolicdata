resubst:=proc(sol,polys)
begin map(sol,u->simplify(subs(polys,u))); end;

myBenchmarkFunction:=proc(u) example,vars,polys,sol;
begin
  example:=subs(u,theExample);
  vars:=subs(u,theVars);
  polys:=subs(u,thePolys);
  print(NoNL,"Solve: ".example);print();
  if traperror(
     sol:=solve(polys,vars)
     , 2) >0 then print("Interrupted"); return
  else
  print(NoNL,sol);
  print(NoNL,resubst(sol,polys));
end:
