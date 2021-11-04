from result import NotEnoughKnowns, Result1, Result2, Result3, Success, no_solutions
from relation import IDK, K, Relation2, Term, involution
from typing import Iterable, List, Tuple, TypeVar


T = TypeVar('T')

def isEmptyList(xs_term: Term[List[T]]) -> Result1[List[T]]: # Predicate: lessThan4(3). isHappy(brett).
    match xs_term:
        case K(xs):
            return Success([(xs,)] if len(xs) == 0 else [])

        case IDK():
            return Success([([],)])

    return NotEnoughKnowns() # Never happens


def cons(first: T, rest: List[T]) -> List[T]:
    return [first] + rest 

# []     = ... (y:ys)
# (x:xs) = ...
# [first, ...rest] = xs
def _cons(first_term: Term[T], rest_term: Term[List[T]], xs_term: Term[List[T]]) -> Result3[T, List[T], List[T]]:
    match first_term, rest_term, xs_term:
        case K(first), K(rest), K(xs):
            pass

        case K(first), K(rest), IDK():
            xs = cons(first, rest)
            return Success([(first, rest, xs)])

        case K(first), IDK(),   K(xs):
            rest = [] - first
            return Success([(first, rest, xs)])

        case K(first), IDK(),   IDK():
            pass

        case IDK(),    K(rest), K(xs):
            pass

        case IDK(),    K(rest), IDK():
            pass

        case IDK(),    IDK(),   K(xs):
            if len(xs) == 0:
                # cons(_, _) can never give an empty list
                return no_solutions()

            return Success([(xs[0], xs[1:], xs)])

        case IDK(),    IDK(),   IDK():
            pass

def concat(xs_term: Term[List[T]], ys_term: Term[List[T]], concatenated_term: Term[List[T]]) -> Result3[List[T], List[T], List[T]]:
    match xs_term, ys_term, concatenated_term:
        case K(xs), K(ys), K(concatenated):
            pass

        case K(xs), K(ys), IDK():
            pass

        case K(xs), IDK(), K(concatenated):
            pass

        case K(xs), IDK(), IDK():
            pass

        case IDK(), K(ys), K(concatenated):
            pass

        case IDK(), K(ys), IDK():
            pass

        case IDK(), IDK(), K(concatenated):
            pass

        case IDK(), IDK(), IDK():
            pass

def _reverse(x: List[T]) -> List[T]:
    return list(reversed(x))

reverse = involution("reverse", _reverse)

X = TypeVar('X')
Y = TypeVar('Y')

def zip2(xs_term: Term[List[X]], ys_term: Term[List[Y]], pairs_term: Term[List[Tuple[X, Y]]]) -> Result3[List[X], List[Y], List[Tuple[X, Y]]]:
    match xs_term, ys_term, pairs_term:
        case K(xs), K(ys), K(pairs):
            pass

        case K(xs), K(ys), IDK():
            pass

        case K(xs), IDK(), K(pairs):
            pass

        case K(xs), IDK(), IDK():
            pass

        case IDK(), K(ys), K(pairs):
            pass

        case IDK(), K(ys), IDK():
            pass

        case IDK(), IDK(), K(pairs):
            pass

        case IDK(), IDK(), IDK():
            pass
