from relation import *
from arithmetic_relations import *
from list_relations import *
from set_relations import *
from boolean_relations import *
from util import *

a = IDK('a')
x = IDK('x')
y = IDK('y')
z = IDK('z')
w = IDK('w')

n = IDK('n')
_2n = IDK('_2n')

prime_a = IDK('prime_a')
prime_b = IDK('prime_b')
goldbach = [
    Row3(multiply, n, K(2), _2n),
    Row1(prime, prime_a),
    Row1(prime, prime_b),
    Row3(plus, prime_a, prime_b, _2n)
]

for solution in solve(goldbach):
    pprint(solution)



