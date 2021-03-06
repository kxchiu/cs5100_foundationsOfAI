% Succeeds if all elements in the argument list are bound and all
% different. Fails if any of the elements are unbound, or equal to some
% other element.
alldiff([H | T]) :- member(H, T), !, fail.
alldiff([_ | T]) :- alldiff(T).
alldiff([_]).

% Knowledge base for the digit.
digit(0).
digit(1).
digit(2).
digit(3).
digit(4).
digit(5).
digit(6).
digit(7).
digit(8).
digit(9).

% TWO+TWO=FOUR puzzle.
solve(T,W,O,F,U,R) :-
    digit(F), digit(U), digit(R), digit(T), digit(W), digit(O),
    Vars = [T,W,O,F,U,R],
    alldiff(Vars),
    F \= 0,
    (100*T+10*W+O)+(100*T+10*W+O) =:= 1000*F+100*O+10*U+R.

% SEND+THE=MONEY puzzle.
solve(S,E,N,D,T,H,M,O,Y) :-
    digit(S), digit(E), digit(N), digit(D), digit(T), digit(H),
    digit(M), digit(O), digit(Y),
    Vars = [S,E,N,D,T,H,M,O,Y],
    alldiff(Vars),
    M \= 0,
    (1000*S+100*E+10*N+D)+(100*T+10*H+E) =:= 10000*M+1000*O+100*N+10*E+Y.
