from typing import Tuple
from relation import Relation1, Relation2, Relation3, Term, K, IDK, float_isomorphism
from result import Result1, Result2, Result3, NotEnoughKnowns, Success, no_solutions, one_solution1, one_solution3
from util import Multiset, primes, ints, nats

import unittest

def _plus(term_a: Term[int], term_b: Term[int], term_c: Term[int]) -> Result3[int, int, int]:
    match term_a, term_b, term_c:
        case K(a), K(b), K(c):
            return Success([(a, b, c)] if a + b == c else [])
    
        case K(a), K(b), IDK():
            return Success([(a, b, a + b)])
    
        case K(a), IDK(), K(c):
            return Success([(a, c - a, c)])
        
        case K(a), IDK(), IDK():
            return NotEnoughKnowns() # TODO: come back to this
    
        case IDK(), K(b), K(c):
            return Success([(c - b, b, c)])

        case IDK(), K(b), IDK():
            return NotEnoughKnowns() # TODO: come back to this

        case IDK(a_tag), IDK(b_tag), K(c):
            if a_tag == b_tag and c % 2 == 0:
                return Success([(c // 2, c // 2, c)])
            else:
                return NotEnoughKnowns() # TODO: come back to this

        case IDK(), IDK(), IDK():
            return NotEnoughKnowns() # TODO: come back to this, infinite amount

    return Success([]) # Never going to happen (is there a better way?)

plus = Relation3('plus', _plus)

def _multiply(term_a: Term[int], term_b: Term[int], term_c: Term[int]) -> Result3[int, int, int]:
    match term_a, term_b, term_c:
        case K(a), K(b), K(c):
            return Success([(a, b, c)] if a * b == c else [])

        case K(a), K(b), IDK():
            c = a * b
            return Success([(a, b, c)])

        case K(a), IDK(), K(c):
            if c == 0:
                if a == 0:
                    def f():
                        for b in ints():
                            yield (a, b, c)
                    return success(f())

                else:
                    b = 0
                    return one_solution3(a, b, c)

            b = c / a

            return one_solution3(a, b, c) if b.is_integer() else no_solutions()

        case K(a), IDK(), IDK():
            return NotEnoughKnowns()

        case IDK(), K(0), K(0):
            def f():
                for a in ints():
                    yield (a, 0, 0)
            if b == 0:
                if c == 0:
                    def f():
                        for a in ints():
                            yield (a, b, c)

        case IDK(), K(0), K(c):
            return no_solutions()

        case IDK(), K(b), K(c):
            a = c / b
            return one_solution3(a, b, c) if a.is_integer() else no_solutions()

        case IDK(), K(0), IDK():
            def f():
                for a in ints():
                    yield (a, 0, 0)

        case IDK(), K(b), IDK():
            return NotEnoughKnowns()

        case IDK(), IDK(), K(0):
            def f():
                for i in ints():
                    yield (0, i, 0)
                    yield (i, 0, 0)
            return Success(f())

        case IDK(a_tag), IDK(b_tag), K(c):
            if a_tag == b_tag:
                if c < 0:
                    return no_solutions()
                x = c ** 0.5
                if x.is_integer():
                    return one_solution(x, x, c)
                else:
                    return no_solutions()
            else:
                return NotEnoughKnowns() # TODO

        case IDK(), IDK(), IDK():
            return NotEnoughKnowns()

multiply = Relation3('multiply', _multiply)

def _square(term_x: Term[int], term_x_squared: Term[int]) -> Result2[int, int]:
    match term_x, term_x_squared:
        case K(x), K(x_squared):
            return Success(
                [(x, x_squared)] if x ** 2 == x_squared else []
            )

        case K(x), IDK():
            return Success([
                (x, x ** 2)
            ])

        case IDK(), K(x_squared):
            if x_squared < 0:
                return no_solutions()

            x = x_squared ** 0.5
            
            if x.is_integer():
                return Success([
                    ( int(x), x_squared),
                    (-int(x), x_squared)
                ])

            else:
                return no_solutions()

        case IDK(), IDK():
            return NotEnoughKnowns()

    return NotEnoughKnowns() # Never happens

square = Relation2('square', _square)

def prime_factors(product_term: Term[int], prime_factors_term: Term[Multiset[int]]) -> Result2[Multiset[int], int]:
    pass # TODO



def _nat(n_term: Term[int]) -> Result1[int]:
    match n_term:
        case K(n):
            return one_solution1(n) if n >= 0 else no_solutions()

        case IDK():
            return Success(nats())

nat = Relation1("nat", _nat)

def _prime(n_term: Term[int]) -> Result1[int]:
    match n_term:
        case K(n):
            return one_solution1(n) if is_prime(n) else no_solutions()

        case IDK():
            return Success(primes())


prime = Relation1("prime", _prime)



class ArithmeticRelationsTest(unittest.TestCase):
    def test_twelve_squared_equals_what_integers(self):
        result = square(K(12), IDK('_'))
        
        self.assertIsInstance(result, Success)

        if isinstance(result, Success):
            results = list(result.iterable)
            self.assertListEqual(results, [(12, 144)])

    def test_what_integers_squared_equal_144(self):
        result = square(IDK('_'), K(144))
        
        self.assertIsInstance(result, Success)

        if isinstance(result, Success):
            results = list(result.iterable)

            self.assertIn(( 12, 144), results)
            self.assertIn((-12, 144), results)
            self.assertEqual(len(results), 2)

    def test_what_integers_squared_equal_5(self):
        result = square(IDK('_'), K(5))
        
        self.assertIsInstance(result, Success)

        if isinstance(result, Success):
            results = list(result.iterable)
            # There are no integers X such that X^2 = 5
            self.assertListEqual(results, [])


if __name__ == '__main__':
    unittest.main()
