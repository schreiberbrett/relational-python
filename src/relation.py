from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, TypeVar, Generic
from result import NotEnoughKnowns, Result1, Result2, Result3, Success, UncountablyInfinite, no_solutions
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
    run: Callable[[Term[A]], Result1[A]]

@dataclass(frozen=True)
class Relation2(Generic[A, B]):
    name: str
    run: Callable[[Term[A], Term[B]], Result2[A, B]]

@dataclass(frozen=True)
class Relation3(Generic[A, B, C]):
    name: str
    run: Callable[[Term[A], Term[B], Term[C]], Result3[A, B, C]]

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

def solve(rows: List[Row]) -> NotEnoughKnowns | Iterable[Dict[str, Any]]:
    return solve_helper(rows, dict())

def solve_helper(rows: List[Row], assignments: Dict[str, Any]) -> NotEnoughKnowns | Iterable[Dict[str, Any]]:
    def get_term(x: Term[A]) -> Term[A]:
        if isinstance(x, IDK) and x.tag in assignments:
            return K(assignments[x.tag])
        
        return x

    if len(rows) == 0:
        return [assignments]

    sorted_rows = sort_by_best_candidates(rows, assignments)

    first_result = find_first_result(sorted_rows, assignments)

    if first_result is None:
        return NotEnoughKnowns()

    for x in first_result.success.iterable:
        new_assignments = determine_new_assignments(first_result.row, x)

        merged = dict(assignments, **new_assignments)

        recursive_result = solve_helper(first_result.rest_rows, merged)

        if isinstance(recursive_result, Iterable):
            def f():
                yield from recursive_result

            return f()

            # yield from recursive_result # Yeah, yeah, it's only one branch for now. Take it.
    else:
        return NotEnoughKnowns()





def determine_new_assignments(row: Row, x: Tuple[A] | Tuple[A, B] | Tuple[A, B, C]) -> Dict[str, A | B | C]:
    new_assignments: Dict[str, Any] = dict()

    match row.columns, x:
        case (_, a_term), (a):
            if isinstance(a_term, IDK):
                new_assignments[a_term.tag] = a
        
        case (_, a_term, b_term), (a, b):
            if isinstance(a_term, IDK):
                new_assignments[a_term.tag] = a

            if isinstance(b_term, IDK):
                new_assignments[b_term.tag] = b

        case (_, a_term, b_term, c_term), (a, b, c):
            if isinstance(a_term, IDK):
                new_assignments[a_term.tag] = a

            if isinstance(b_term, IDK):
                new_assignments[b_term.tag] = b

            if isinstance(c_term, IDK):
                new_assignments[c_term.tag] = c

    return new_assignments


@dataclass
class FirstResult():
    row: Row
    success: Success[Any]
    rest_rows: List[Row]

def find_first_result(rows: List[Row], assignments: Dict[str, Any]) -> Optional[FirstResult]:
    '''Iterate through until one gives success. Returns `None` on no successes.'''

    for prev, row, rest in window(rows):
        result = run_row(row, assignments)
        if isinstance(result, Success):
            return FirstResult(
                row=row,
                success=result,
                rest_rows=prev + rest
            )

    return None


def get_tags(row: Row) -> Set[str]:
    tags: Set[str] = set()
    for x in row.columns:
        if isinstance(x, IDK):
            tags.add(x.tag)
    
    return tags



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


def float_isomorphism(name: str, f: Callable[[float], float], g: Callable[[float], float]) -> Relation2[float, float]:
    def r(a_term: Term[float], b_term: Term[float]) -> Result2[float, float]:
        match a_term, b_term:
            case K(a), K(b):
                if f(a) == b: # TODO: float-near-equality
                    return Success([(a, b)])
                else:
                    return no_solutions()

            case K(a), IDK():
                return Success([(a, f(a))])

            case IDK(), K(b):
                return Success([(g(b), b)])

            case IDK(), IDK():
                return NotEnoughKnowns()

        return NotEnoughKnowns()

    return Relation2(name, r)


def query1(r: Relation1[A], optional_a: Optional[A]) -> None:
    a_term = IDK('a') if optional_a is None else K(optional_a)

    result = r.run(a_term)
    
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

    result = r.run(a_term, b_term)
    
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

    result = r.run(a_term, b_term, c_term)
    
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


def run_row(row: Row, assignments: Dict[str, Any] = dict()) -> Result1[Any] | Result2[Any, Any] | Result3[Any, Any, Any]:
    def get_term(x: Term[A]) -> Term[A]:
        if isinstance(x, IDK) and x.tag in assignments:
            return K(assignments[x.tag])
        else:
            return x

    match row:
        case Row1(columns=(r, a)):
            return r.run(get_term(a))

        case Row2(columns=(r, a, b)):
            return r.run(get_term(a), get_term(b))

        case Row3(columns=(r, a, b, c)):
            return r.run(get_term(a), get_term(b), get_term(c))

    return NotEnoughKnowns() # Never happens


