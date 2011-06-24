#!/usr/bin/env python

import sys

def Turn(lr, slot, card):
	print lr
	if lr == 1:
		print card
		print slot
	else:
		print slot
		print card
	OppTurn()

def OppTurn():
	sys.stdout.flush()
	lr = sys.stdin.readline().rstrip()
	if lr == '1':
		card = sys.stdin.readline().rstrip()
		slot = sys.stdin.readline().rstrip()
	elif lr == '2':
		slot = sys.stdin.readline().rstrip()
		card = sys.stdin.readline().rstrip()

if sys.argv[1] == '1':
	OppTurn()

Turn(2, 3, 'zero')

Turn(2, 1, 'K')
Turn(2, 1, 'zero')
Turn(1, 1, 'K')
Turn(1, 1, 'S')
Turn(2, 1, 'dec')
Turn(1, 1, 'K')
Turn(1, 1, 'S')
Turn(2, 1, 'get')
Turn(1, 1, 'K')
Turn(1, 1, 'S')
Turn(2, 1, 'succ')
Turn(1, 1, 'K')
Turn(1, 1, 'S')
Turn(2, 1, 'succ')
Turn(1, 1, 'K')
Turn(1, 1, 'S')
Turn(2, 1, 'succ')

Turn(2, 2, 'S')
Turn(2, 2, 'get')
Turn(2, 2, 'I')
Turn(1, 2, 'K')
Turn(1, 2, 'S')
Turn(1, 2, 'K')
Turn(1, 2, 'S')
Turn(2, 2, 'get')
Turn(1, 2, 'K')
Turn(1, 2, 'S')
Turn(2, 2, 'succ')
Turn(2, 2, 'zero')

while 1:
	for i in xrange(213):
		Turn(2, 0, 'zero')
		Turn(1, 0, 'succ')
		Turn(1, 0, 'succ')
		Turn(1, 0, 'get')

		Turn(2, 0, 'zero')

	Turn(1, 3, 'succ')
