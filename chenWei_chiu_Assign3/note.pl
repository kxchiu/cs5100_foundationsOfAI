% Succ function to find successor.
% succ(3) will return 4.
succ(3).

% Define functions like writing a sentence.
double_digit(X, Y) :-
    Y is X*2.
power_digit(X, Y, Z) :-
    X is Y**Z,
    write(Y**Z).
is_even(X) :-
    Y is X//2,
    X =:= 2 * Y.

% Input and format
input_sth :-
    write('Input a character: '),
    read(X),
    format('Your input: ~w', [X]),
    put(X), nl.

index([V|_],V,0).
index([_|T],V,s(I)) :- index(T,V,I).
