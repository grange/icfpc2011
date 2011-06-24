#!/usr/bin/env python

from eval import *

print '-'*80, 'First example, deathmatch'
b1 = Board(debug=True) # player one view
b2 = Board(invert=b1, debug=True) # player 2 view, swapped

b1.apply_right(0, Zero)
b2.apply_right(0, Zero)
print '='*6

b1.apply_left(0, Succ)
b2.apply_right(0, Zero)
print '='*6

b1.apply_left(0, Succ)
b2.apply_right(0, Dec)
print '='*6

b1.apply_left(0, Dbl)
b2.apply_right(0, Zero)
print '='*6

b1.apply_left(0, Inc)
b2.apply_left(0, Succ)




print '\n'
print '-'*80, 'Second example, healing'
b = Board(debug=True)

b.apply_right(0, Help)
b.apply_right(0, Zero)
b.apply_left(0, K)
b.apply_left(0, S)
b.apply_right(0, Succ)
b.apply_right(0, Zero)

b.apply_right(1, Zero)
b.apply_left(1, Succ)
b.apply_left(1, Dbl)
b.apply_left(1, Dbl)
b.apply_left(1, Dbl)
b.apply_left(1, Dbl)

b.apply_left(0, K)
b.apply_left(0, S)
b.apply_right(0, Get)
b.apply_left(0, K)
b.apply_left(0, S)
b.apply_right(0, Succ)
b.apply_right(0, Zero)

b.zombie_scan()
