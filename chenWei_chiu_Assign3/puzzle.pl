% Knowledge base
day(monday).
day(tuesday).
day(wednesday).
day(thursday).
day(friday).

fruit(apple).
fruit(mango).
fruit(banana).
fruit(pear).
fruit(apricot).

nut(almonds).
nut(peanuts).
nut(cashews).
nut(walnuts).
nut(pecans).

solve :-
    day(MonDay), day(TuesDay), day(WednesDay),
    day(ThursDay), day(FriDay),
    all_different([MonDay, TuesDay, WednesDay, ThursDay, FriDay]),

    fruit(MonFru), fruit(TuesFru), fruit(WednesFru),
    fruit(ThursFru), fruit(FriFru),
    all_different([MonFru, TuesFru, WednesFru, ThursFru, FriFru]),

    nut(MonNut), nut(TuesNut), nut(WednesNut),
    nut(ThursNut), nut(FriNut),
    all_different([MonNut, TuesNut, WednesNut, ThursNut, FriNut]),

    % This actually somehow sets the list by day order.
    Triples = [ [MonDay, MonFru, MonNut],
                [TuesDay, TuesFru, TuesNut],
                [WednesDay, WednesFru, WednesNut],
                [ThursDay, ThursFru, ThursNut],
                [FriDay, FriFru, FriNut] ],

    % 1. The apple was eaten later in the week than the mango.
    (
        member([_, apple, _], Triples),
        member([_, mango, _], Triples),
        indexOfInListOfLists(Triples, apple, X, Y),
        indexOfInListOfLists(Triples, mango, Z, W),
        W < Y, X =:= Z
    ),

    % 2. The banana was eaten later in the week than both the almonds and peanuts,
    % but earlier in the week than the pear.
    (
        member([_, banana, _], Triples),
        member([_, _, almonds], Triples),
        member([_, _, peanuts], Triples),
        member([_, pear, _], Triples),
        indexOfInListOfLists(Triples, banana, A, B),
        indexOfInListOfLists(Triples, almonds, C, D),
        indexOfInListOfLists(Triples, peanuts, E, F),
        indexOfInListOfLists(Triples, pear, G, H),
        E =\= A, C =\= G, A =:= G, C =:= E,
        B > D, B > F, B < H
                                       ),

    % 3. The cashews were eaten earlier in the week than both the banana and the
    % apricot, but later in the week than the peanuts.
    (
        member([_, _, cashews], Triples),
        member([_, apricot, _], Triples),
        indexOfInListOfLists(Triples, cashews, I, J),
        indexOfInListOfLists(Triples, apricot, M, N),
        J < B, J < N, J > F, I =\= M
                                              ),

    % 4. The pecans were not eaten the evening after the almonds.
    % Translates to: Pecans were either eaten before or not right after
    % the almonds.
    (
        member([_, _, pecans], Triples),
        indexOfInListOfLists(Triples, pecans, O, P),
        O =:= C, (P < D ; P - D > 1)
                                                         ),

    % 5. Bill ate walnuts one night.
    member([_, _, walnuts], Triples),

    tell(MonDay, MonFru, MonNut),
    tell(TuesDay, TuesFru, TuesNut),
    tell(WednesDay, WednesFru, WednesNut),
    tell(ThursDay, ThursFru, ThursNut),
    tell(FriDay, FriFru, FriNut).


% Succeeds if all elements of the argument list are bound and different.
% Fails if any elements are unbound or equal to some other element.
all_different([H | T]) :- member(H, T), !, fail.
all_different([_ | T]) :- all_different(T).
all_different([_]).

% Finds the index of list containing the element in the lists.
% Returns the index of element in the list and the index of that list in
% the lists.
indexOfInListOfLists(ListOfLists, Element, Index, IndexInList):-
    member(List, ListOfLists),
    indexOf(List, Element, Index),
    indexInList(ListOfLists, List, IndexInList).

% Helper: returns the index of element in the list.
% Somewhat redundant and may need to clean up.
indexOf([Element|_], Element, 0):- !.
indexOf([_|Tail], Element, Index):-
  indexOf(Tail, Element, Index1),
  !,
  Index is Index1+1.

% Helper: returns index of the list containing the element in the lists.
indexInList([Element|_], Element, 0):- !.
indexInList([_|Tail], Element, Index):-
  indexOf(Tail, Element, Index1),
  !,
  Index is Index1+1.

% Prints Day some-day with some-fruit and some-nuts.
tell(X, Y, Z) :-
    write('('), write(X), write(' ,'), write(Y),
    write(' ,'), write(Z), write(')'), nl.
