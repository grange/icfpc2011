#!/usr/bin/env python
from eval import *


b = Board(debug=True)

for i in range(10):
    try:
        reset_global_op_counter()
        S(b)(I(b), I(b), S(b)(I(b), I(b)))
    except OpLimitError, e:
        print e

print 'BOARD'
print b

if 0:
    b.prop[1].value=10

    b.apply_right(0, Help)
    b.apply_right(0, Zero)

    b.apply_left(0, K)
    b.apply_left(0, S)
    b.apply_right(0, Succ)
    b.apply_right(0, Zero)

    b.apply_left(0, K)
    b.apply_left(0, S)
    b.apply_right(0, Get)

    b.apply_left(0, K)
    b.apply_left(0, S)
    b.apply_right(0, Succ)
    b.apply_right(0, Zero)

    b.zombie_scan()
    b.display()
