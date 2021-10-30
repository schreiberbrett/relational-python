from typing import Tuple
from relation import Relation2, Relation3, Term, K, IDK
from result import NotEnoughKnowns, Result2, Success, Result3, no_solutions
from util import Multiset

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
    pass # TODO

multiply = Relation3('multiply', _multiply)

def _square(term_x: Term[int], term_x_squared: Term[int]) -> Result2[int, int]:
    match term_x, term_x_squared:
        case K(x), K(x_squared):
            return Success([
                (x, x_squared)
            ])

        case K(x), IDK():
            return Success([
                (x, x ** 2)
            ])

        case IDK(), K(x_squared):
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