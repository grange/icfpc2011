#!/usr/bin/env python

import sys
from game import GameState

g = GameState(sys.argv[1], debug=False, eval_=True, collect_stats=False)
g.start()
Turn = g.turn


def Attack():
	Turn(2, 0, 'attack')
	Turn(2, 0, 'zero')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'get')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'dbl')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'dbl')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'get')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')

def Help():
	# copy help loop to slot 0
	Turn(2, 0, 'zero')
	Turn(1, 0, 'succ')
	Turn(1, 0, 'dbl')
	Turn(1, 0, 'dbl')
	Turn(1, 0, 'get')

	# do help
	Turn(2, 0, 'zero')

# slot 1: value to help/attack
Turn(2, 1, 'zero')
Turn(1, 1, 'succ')
for i in xrange(13):
	Turn(1, 1, 'dbl')

# slot 2: help func
Turn(2, 2, 'help')
Turn(2, 2, 'zero')
Turn(2, 2, 'zero')
Turn(1, 2, 'K')
Turn(1, 2, 'S')
Turn(2, 2, 'get')
Turn(1, 2, 'K')
Turn(1, 2, 'S')
Turn(2, 2, 'succ')

# slot 3: K-help func
Turn(2, 3, 'K')
Turn(2, 3, 'zero')
Turn(1, 3, 'K')
Turn(1, 3, 'S')
Turn(1, 3, 'K')
Turn(1, 3, 'S')
Turn(2, 3, 'get')
Turn(1, 3, 'K')
Turn(1, 3, 'S')
Turn(2, 3, 'succ')
Turn(1, 3, 'K')
Turn(1, 3, 'S')
Turn(2, 3, 'succ')
Turn(2, 3, 'zero')

# slot 4: help loop
Turn(2, 4, 'S')
Turn(2, 4, 'get')
Turn(2, 4, 'I')
Turn(1, 4, 'K')
Turn(1, 4, 'S')
Turn(1, 4, 'K')
Turn(1, 4, 'S')
Turn(2, 4, 'get')
Turn(1, 4, 'K')
Turn(1, 4, 'S')
Turn(2, 4, 'succ')
Turn(1, 4, 'K')
Turn(1, 4, 'S')
Turn(2, 4, 'succ')
Turn(1, 4, 'K')
Turn(1, 4, 'S')
Turn(2, 4, 'succ')
Turn(2, 4, 'zero')

# slot 5: slot to attack
Turn(2, 5, 'zero')
Turn(1, 5, 'succ')
for i in xrange(7):
	Turn(1, 5, 'dbl')
for i in xrange(127):
	Turn(1, 5, 'succ')

# attack opponent's slot 0
Help()
Attack()
Attack()

# now we can double help/attack value
Turn(1, 1, 'dbl')

while 1:
	# attack from slot 255
	Turn(1, 5, 'put')
	Turn(2, 5, 'zero')

	for i in xrange(255):
		if i % 2 == 0:
			Help()
		Attack()
		#if g.turn_number > 1000: g.evaluator_on_off(False)

		# next slot to attack
		Turn(1, 5, 'succ')


		#if g.b.prop[253].health <= 0:
		#	print >>sys.stderr, "----- slot 253 killed"

		#if g.player == 1: print >>sys.stderr, 'Opp add: ', g.b.opp_mru('add')[0:3]
		#if g.player == 1: print >>sys.stderr, 'Opp call:', g.b.opp_mru('call')[0:3]
		#if g.player == 1: print >>sys.stderr, 'Opp get:', g.b.opp_mru('get')[0:3]
		#if g.player == 1: print >>sys.stderr, 'Opp put:', g.b.opp_mru('put')[0:3]
		#if g.player == 1: print >>sys.stderr, 'Opp tree:', g.b.opp_tree_sizes()[0:6]
		#if g.player == 1: print >>sys.stderr


