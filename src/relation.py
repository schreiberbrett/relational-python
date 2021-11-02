from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, TypeVar, Generic
from result import NotEnoughKnowns, Result1, Result2, Result3, Success, UncountablyInfinite
from functools import cmp_to_key
from pprint import pprint

T = TypeVar('T')

@dataclass(frozen=True)
class K(Generic[T]):
    value: T

    def __repr__(self) -> str:
        return repr(self.value)

@dataclass(frozen=True)
class IDK:
    tag: str

    def __repr__(self) -> str:
        return self.tag

Term = K[T] | IDK

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

@dataclass(frozen=True)
class Relation1(Generic[A]):
    name: str
    f: Callable[[Term[A]], Result1[A]]

@dataclass(frozen=True)
class Relation2(Generic[A, B]):
    name: str
    f: Callable[[Term[A], Term[B]], Result2[A, B]]

@dataclass(frozen=True)
class Relation3(Generic[A, B, C]):
    name: str
    f: Callable[[Term[A], Term[B], Term[C]], Result3[A, B, C]]

def from_list(list: List[A]) -> Relation1[A]:
    pass # TODO

def from_pairs(pairs: List[Tuple[A, B]]) -> Relation2[A, B]:
    pass # TODO

def from_triples(triples: List[Tuple[A, B, C]]) -> Relation3[A, B, C]:
    pass # TODO


R = TypeVar('R')


@dataclass
class Row1:
    columns: Tuple[Relation1[Any], Term[Any]]

    def __init__(self, r: Relation1[A], a: Term[A]):
        self.columns = (r, a)

    def __repr__(self) -> str:
        (r, a) = self.columns
        return f'{r.name}({repr(a)})'

@dataclass
class Row2:
    columns: Tuple[Relation2[Any, Any], Term[Any], Term[Any]]

    def __init__(self, r: Relation2[A, B], a: Term[A], b: Term[B]):
        self.columns = (r, a, b)

    def __repr__(self) -> str:
        (r, a, b) = self.columns
        return f'{r.name}({repr(a)}, {repr(b)})'

@dataclass
class Row3:
    columns: Tuple[Relation3[Any, Any, Any], Term[Any], Term[Any], Term[Any]]

    def __init__(self, r: Relation3[A, B, C], a: Term[A], b: Term[B], c: Term[C]):
        self.columns = (r, a, b, c)

    def __repr__(self) -> str:
        (r, a, b, c) = self.columns
        return f'{r.name}({repr(a)}, {repr(b)}, {repr(c)})'

Row = Row1 | Row2 | Row3

def solve3(rows: List[Row]) -> Result3[Any, Any, Any]:
    return solve3_helper(rows, dict())


def solve3_helper(rows: List[Row], assignments: Dict[str, Any]) -> Result3[Any, Any, Any]:
    def get_term(x: Term[A]) -> Term[A]:
        if isinstance(x, IDK) and x.tag in assignments:
            return K(assignments[x.tag])
        
        return x

    if len(rows) == 0:
        return Success([])

    sorted_rows = sort_by_best_candidates(rows, assignments)

    for prev, current, rest in window(sorted_rows):
        result = NotEnoughKnowns
        match current:
            case Row1((r, a)):
                result = r.f(get_term(a))

            case Row2((r, a, b)):
                result = r.f(get_term(a), get_term(b))

            case Row3((r, a, b, c)):
                result = r.f(get_term(a), get_term(b), get_term(c))

        if isinstance(result, Success):
            break
       
    



def window(xs: List[T]) -> List[Tuple[List[T], T, List[T]]]:
    return [(xs[:i], x, xs[(i + 1):]) for i, x in enumerate(xs)]


def sort_by_best_candidates(rows: List[Row], assignments: Dict[str, Any]) -> List[Row]:
    """
    The rows with the least amount of unknowns should be at the beginning of the list.
    If two rows have the same amount of unknowns, then the one with more knowns should closer to the beginning.
    """
    def cmp(a: Row, b: Row) -> int:
        a_unknowns = number_of_unknowns(a, assignments)
        b_unknowns = number_of_unknowns(b, assignments)

        if a_unknowns == b_unknowns:
            return number_of_knowns(a, assignments) - number_of_knowns(b, assignments)
        else:
            return b_unknowns - a_unknowns

    return sorted(rows, key=cmp_to_key(cmp), reverse=True)


def is_known(term: Term[A], assignments: Dict[str, Any]) -> bool:
    match term:
        case K():
            return True
        case IDK(tag):
            return (tag in assignments)
    
    return False # Never reached

def number_of_knowns(row: Row, assignments: Dict[str, Any]) -> int:
    match row:
        case Row1((_, a)):
            n = 0
            if is_known(a, assignments): n += 1
            return n
        
        case Row2((_, a, b)):
            n = 0
            if is_known(a, assignments): n += 1
            if is_known(b, assignments): n += 1
            return n
        
        case Row3((_, a, b, c)):
            n = 0
            if is_known(a, assignments): n += 1
            if is_known(b, assignments): n += 1
            if is_known(c, assignments): n += 1
            return n
    
    return 0 # Never reached

def number_of_unknowns(row: Row, assignments: Dict[str, Any]) -> int:
    match row:
        case Row1((_, a)):
            n = 0
            if not is_known(a, assignments): n += 1
            return n
        
        case Row2((_, a, b)):
            n = 0
            if not is_known(a, assignments): n += 1
            if not is_known(b, assignments): n += 1
            return n
        
        case Row3((_, a, b, c)):
            n = 0
            if not is_known(a, assignments): n += 1
            if not is_known(b, assignments): n += 1
            if not is_known(c, assignments): n += 1
            return n
    
    return 0 # Never reached






def isomorphism(name: str, f: Callable[[A], B], inverse_of_f: Callable[[B], A]) -> Relation2[A, B]:
    def r(a_term: Term[A], b_term: Term[B]) -> Result2[A, B]:
        match a_term, b_term:
            case K(a), K(b):
                return Success([(a, b)] if f(a) == b else [])

            case K(a), IDK():
                return Success([(a, f(a))])

            case IDK(), K(b):
                return Success([(inverse_of_f(b), b)])

            case IDK(), IDK():
                return NotEnoughKnowns()

        return NotEnoughKnowns()

    return Relation2(name, r)


def involution(name: str, f: Callable[[A], A]) -> Relation2[A, A]:
    return isomorphism(name, f, f)


def query1(r: Relation1[A], optional_a: Optional[A]) -> None:
    a_term = IDK('a') if optional_a is None else K(optional_a)

    result = r.f(a_term)
    
    match result:
        case NotEnoughKnowns():
            print('Not enough knowns.')
        case UncountablyInfinite():
            print('Uncountably infinite.')
        case Success(iterable):
            for x in iterable:
                pprint(x)
                print()
                b = input('ENTER to continue. q to stop: ')
                if b == 'q':
                    break
            else:
                print('Results exhausted.')

def query2(r: Relation2[A, B], optional_a: Optional[A], optional_b: Optional[B]) -> None:
    a_term = IDK('a') if optional_a is None else K(optional_a)
    b_term = IDK('b') if optional_b is None else K(optional_b)

    result = r.f(a_term, b_term)
    
    match result:
        case NotEnoughKnowns():
            print('Not enough knowns.')
        case UncountablyInfinite():
            print('Uncountably infinite.')
        case Success(iterable):
            for x in iterable:
                pprint(x)
                print()
                b = input('ENTER to continue. q to stop: ')
                if b == 'q':
                    break
            else:
                print('Results exhausted.')

def query3(r: Relation3[A, B, C], optional_a: Optional[A], optional_b: Optional[B], optional_c: Optional[C]) -> None:
    a_term = IDK('a') if optional_a is None else K(optional_a)
    b_term = IDK('b') if optional_b is None else K(optional_b)
    c_term = IDK('c') if optional_c is None else K(optional_c)

    result = r.f(a_term, b_term, c_term)
    
    match result:
        case NotEnoughKnowns():
            print('Not enough knowns.')
        case UncountablyInfinite():
            print('Uncountably infinite.')
        case Success(iterable):
            for x in iterable:
                pprint(x)
                print()
                b = input('ENTER to continue. q to stop: ')
                if b == 'q':
                    break
            else:
                print('Results exhausted.')