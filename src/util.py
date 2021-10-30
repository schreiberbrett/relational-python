from dataclasses import dataclass
from typing import Generic, Hashable, Iterator, List, Tuple, TypeVar, Generator
from itertools import product

A = TypeVar('A')
B = TypeVar('B')

def nats() -> Iterator[int]:
    i = 0
    while True:
        yield i
        i += 1

def ints() -> Iterator[int]:
    yield 0
    i = 1
    while True:
        yield i
        yield -i
        i += 1

def infproduct(iter_as: Iterator[A], iter_bs: Iterator[B]) -> Generator[Tuple[A, B], None, None]:
    past_as: List[A] = []
    past_bs: List[B] = []

    out_of_as = False
    out_of_bs = False

    while not (out_of_as and out_of_bs):
        if not out_of_as:
            try:
                a = next(iter_as)
                past_as.append(a)
                yield from ((a, b) for b in past_bs)
            except StopIteration:
                out_of_as = True

        if not out_of_bs:
            try:
                b = next(iter_bs)
                past_bs.append(b)
                yield from ((a, b) for a in past_as)
            except StopIteration:
                out_of_bs = True


def infproduct_many(*iters: Iterator[A]) -> Generator[Tuple[A, ...], None, None]:
    T = TypeVar('T')

    @dataclass
    class State(Generic[T]):
        past_values: List[T]
        out_of_values: bool
        iterator: Iterator[T]


    def window(xs: List[T]) -> List[Tuple[List[T], T, List[T]]]:
        return [(xs[:i], x, xs[(i + 1):]) for i, x in enumerate(xs)]



    states = [State([], False, x) for x in iters]


    while not all(state.out_of_values for state in states):
        for (prev, state, rest) in window(states):
            if not state.out_of_values:
                try:
                    value = next(state.iterator)
                    state.past_values.append(value)

                    prev_past_values = [v.past_values for v in prev] # type: ignore
                    rest_past_values = [v.past_values for v in rest] # type: ignore


                    yield from ((value, *xprod) for xprod in product(*past_values)) # type: ignore
                except StopIteration:
                    state.out_of_values = True



H = TypeVar('H', bound=Hashable)

class Multiset(Generic[H]):
    pass