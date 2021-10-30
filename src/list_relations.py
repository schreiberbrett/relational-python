from result import Result1, Result2, Result3
from relation import IDK, K, Term
from typing import List, Tuple, TypeVar


T = TypeVar('T')

def nil(xs_term: Term[List[T]]) -> Result1[List[T]]:
    match xs_term:
        case K(xs):
            pass

        case IDK():
            pass


def cons(first_term: Term[T], rest_term: Term[List[T]], xs_term: Term[List[T]]) -> Result3[List[T], List[T], List[T]]:
    match first_term, rest_term, xs_term:
        case K(first), K(rest), K(xs):
            pass

        case K(first), K(rest), IDK():
            pass

        case K(first), IDK(),   K(xs):
            pass

        case K(first), IDK(),   IDK():
            pass

        case IDK(),    K(rest), K(xs):
            pass

        case IDK(),    K(rest), IDK():
            pass

        case IDK(),    IDK(),   K(xs):
            pass

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

def reverse(xs_term: Term[List[T]], reversed_term: Term[List[T]]) -> Result2[List[T], List[T]]:
    match xs_term, reversed_term:
        case K(xs), K(reversed):
            pass

        case K(xs), IDK():
            pass

        case IDK(), K(reversed):
            pass

        case IDK(), IDK():
            pass

X = TypeVar('X')
Y = TypeVar('Y')

def zip(xs_term: Term[List[X]], ys_term: Term[List[Y]], pairs_term: Term[List[Tuple[X, Y]]]) -> Result3[List[X], List[Y], List[Tuple[X, Y]]]:
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
