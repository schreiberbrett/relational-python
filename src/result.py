from dataclasses import dataclass
from typing import Iterable, Tuple, TypeVar, Generic

T = TypeVar('T')

@dataclass(frozen=True)
class NotEnoughKnowns:
    pass

@dataclass(frozen=True)
class UncountablyInfinite:
    pass

@dataclass(frozen=True)
class Success(Generic[T]):
    iterable: Iterable[T] # Empty iterable indicates failure

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

Result1 = NotEnoughKnowns | UncountablyInfinite | Success[Tuple[A]]
Result2 = NotEnoughKnowns | UncountablyInfinite | Success[Tuple[A, B]]
Result3 = NotEnoughKnowns | UncountablyInfinite | Success[Tuple[A, B, C]]

def singleton1(a: A) -> Result1[A]:
    return Success([(a,)])

def singleton2(a: A, b: B) -> Result2[A, B]:
    return Success([(a, b)])

def singleton3(a: A, b: B, c: C) -> Result3[A, B, C]:
    return Success([(a, b, c)])

def no_solutions():
    return Success([])