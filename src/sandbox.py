from relation import *
from arithmetic_relations import *
from list_relations import *
from set_relations import *
from boolean_relations import *
from util import *

prime_a: Term[int] = IDK('prime_a')
prime_b: Term[int] = IDK('prime_b')

goldbach: List[Row] = [
    Row1(prime, IDK('p1')),
    Row1(prime, IDK('p2')),

    # Row1(prime, IDK('p1')),
    # Row1(prime, IDK('p2')),
    Row3(plus,  IDK('p1'), IDK('p2'), K(24)),


    # definition of an even number
    # Row1(nat, IDK('n')                    ),
    # Row3(multiply, K(2), IDK('n'), IDK('2n'))
]

solutions = solve(goldbach)

if isinstance(solutions, Generator):
    print_paced(solutions)

