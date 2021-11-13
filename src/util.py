from dataclasses import dataclass
from enum import Enum, auto
from pprint import pprint
from typing import Any, Generic, Hashable, Iterable, Iterator, List, Set, Tuple, TypeVar, Generator
from itertools import product
from random import shuffle

from result import Success

A = TypeVar('A')
B = TypeVar('B')

def nats():
    i = 0
    while True:
        yield i
        i += 1

def ints():
    yield 0
    i = 1
    while True:
        yield i
        yield -i
        i += 1


def spin_cycle(iters: List[Iterator[A]]) -> Generator[A, None, None]:
    if len(iters) == 0:
        return

    i = 0
    while True:
        yield next(iters[i])
        i += 1
        if i == len(iters):
            i = 0


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    # TODO: Use AKS

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


def primes() -> Iterator[int]:
    # TODO: use computerphile Sieve of Eratosthenes
    for i in nats():
        if i == 0 or i == 1:
            continue

        if is_prime(i):
            yield i

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


def from_iterable(iterable: Iterable[A]) -> Success[Tuple[A]]:
    def f():
        for i in iterable:
            yield (i,)

    return Success(f())









class GeneratorState(Enum):
    EXHAUSTED     = auto()
    MAY_HAVE_MORE = auto()

@dataclass
class GeneratorAndState(Generic[A]):
    iterator: Generator[A, None, None]
    state: GeneratorState

def flatten(generator_of_generators: Generator[Generator[A, None, None], None, None]) -> Generator[A, None, None]:
    known_generators: List[GeneratorAndState[A]] = []
    for inner_iterator in generator_of_generators:
        known_generators.append(GeneratorAndState(inner_iterator, GeneratorState.MAY_HAVE_MORE))

        # yield once from each of the known iterators
        for x in known_generators:
            try:
                yield next(x.iterator)
            except StopIteration:
                x.state = GeneratorState.EXHAUSTED

        # remove exhausted iterators
        known_generators = [x for x in known_generators if x.state == GeneratorState.MAY_HAVE_MORE]

    while len(known_generators) > 0:
        # yield once from each of the known iterators
        for x in known_generators:
            try:
                yield next(x.iterator)
            except StopIteration:
                x.state = GeneratorState.EXHAUSTED

        # remove exhausted iterators
        known_generators = [x for x in known_generators if x.state == GeneratorState.MAY_HAVE_MORE]        




def mischief():
    for nat in nats():
        def inner():
            for i in range(nat):
                yield i
        
        yield inner()


def print_paced(generator: Generator[Any, None, None]) -> None:
    for x in generator:
        pprint(x)
        b = input('ENTER to continue. q to stop: ')
        if b == 'q':
            break

def mischief2():
    for x in [nats(), nats(), ints()]:
        yield x








H = TypeVar('H', bound=Hashable)

class Multiset(Generic[H]):
    pass


def flatten_uniques(generator_of_generators: Generator[Generator[H, None, None], None, None]) -> Generator[H, None, None]:
    seen_results: Set[H] = set()
    known_generators: List[GeneratorAndState[H]] = []
    for inner_iterator in generator_of_generators:
        known_generators.append(GeneratorAndState(inner_iterator, GeneratorState.MAY_HAVE_MORE))

        # yield once from each of the known iterators
        for x in known_generators:
            try:
                result = next(x.iterator)
                if result not in seen_results:
                    seen_results.add(result)
                    yield result
            except StopIteration:
                x.state = GeneratorState.EXHAUSTED

        # remove exhausted iterators
        known_generators = [x for x in known_generators if x.state == GeneratorState.MAY_HAVE_MORE]

    while len(known_generators) > 0:
        # yield once from each of the known iterators
        for x in known_generators:
            try:
                result = next(x.iterator)
                if result not in seen_results:
                    seen_results.add(result)
                    yield result
            except StopIteration:
                x.state = GeneratorState.EXHAUSTED

        # remove exhausted iterators
        known_generators = [x for x in known_generators if x.state == GeneratorState.MAY_HAVE_MORE]        



def flatten_uniques_random_pick(generator_of_generators: Generator[Generator[H, None, None], None, None]) -> Generator[H, None, None]:
    seen_results: Set[H] = set()
    known_generators: List[GeneratorAndState[H]] = []
    for inner_iterator in generator_of_generators:
        known_generators.append(GeneratorAndState(inner_iterator, GeneratorState.MAY_HAVE_MORE))

        # yield once from each of the known iterators
        for x in known_generators:
            try:
                result = next(x.iterator)
                if result not in seen_results:
                    seen_results.add(result)
                    yield result
            except StopIteration:
                x.state = GeneratorState.EXHAUSTED

        # remove exhausted iterators
        known_generators = [x for x in known_generators if x.state == GeneratorState.MAY_HAVE_MORE]
        shuffle(known_generators)

    while len(known_generators) > 0:
        # yield once from each of the known iterators
        for x in known_generators:
            try:
                result = next(x.iterator)
                if result not in seen_results:
                    seen_results.add(result)
                    yield result
            except StopIteration:
                x.state = GeneratorState.EXHAUSTED

        # remove exhausted iterators
        known_generators = [x for x in known_generators if x.state == GeneratorState.MAY_HAVE_MORE]
        shuffle(known_generators)



