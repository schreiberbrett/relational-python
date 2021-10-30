from typing import Any, Dict, List
from relation import Row, Row3, Row2, sort_by_best_candidates, K, IDK
from arithmetic_relations import plus, square
import unittest

class ArithmeticRelationsTest(unittest.TestCase):
    def test_sort0(self):
        to_be_sorted: List[Row] = [
            Row3(plus, K(3), K(4), K(7)),
            Row2(square, K(2), IDK('A')),
            Row2(square, K(2), K(4))
        ]

        assignments: Dict[str, Any] = {}

        should_be: List[Row] = [
            Row3(plus, K(3), K(4), K(7)),
            Row2(square, K(2), K(4)),
            Row2(square, K(2), IDK('A'))
        ]

        self.assertListEqual(sort_by_best_candidates(to_be_sorted, assignments), should_be)

if __name__ == '__main__':
    unittest.main()