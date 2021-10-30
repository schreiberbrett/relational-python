from relation import IDK, K, Term
from result import Result2, Result3
from typing import Hashable, Set, TypeVar


H = TypeVar('H', bound=Hashable)

def union(a_term: Term[Set[H]], b_term: Term[Set[H]], out_term: Term[Set[H]]) -> Result3[Set[H], Set[H], Set[H]]: # TODO
    match a_term, b_term, out_term:
        case K(a), K(b), K(out):
            pass

        case K(a), K(b), IDK():
            pass

        case K(a), IDK(), K(out):
            pass

        case K(a), IDK(), IDK():
            pass

        case IDK(), K(b), K(out):
            pass

        case IDK(), K(b), IDK():
            pass

        case IDK(), IDK(), K(out):
            pass

        case IDK(), IDK(), IDK():
            pass

def subset(subset_term: Term[Set[H]], superset_term: Term[Set[H]]) -> Result2[Set[H], Set[H]]:
    match subset_term, superset_term:
        case K(subset), K(superset):
            pass

        case K(subset), IDK():
            pass

        case IDK(), K(superset):
            pass

        case IDK(), IDK():
            pass

def strict_subset(subset_term: Term[Set[H]], superset_term: [Term[Set[H]]]) -> Result2[Set[H], Set[H]]:
    match subset_term, superset_term:
        case K(subset), K(superset):
            pass

        case K(subset), IDK():
            pass

        case IDK(), K(superset):
            pass

        case IDK(), IDK():
            pass