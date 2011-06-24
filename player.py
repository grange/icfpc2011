#!/usr/bin/env python

import sys

def Turn(a, b, c):
	print a
	print b
	print c
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

total = 68

for i in xrange(total):
	Turn(2, i, 'inc')
	Turn(1, 'S', i)
	Turn(2, i, 'get')
	if i > 0:
		for j in xrange(i):
			Turn(1, 'K', i)
			Turn(1, 'S', i)
			Turn(2, i, 'succ')
	for j in xrange(11113 - 10000):
		Turn(2, i, 'zero')

ourSlot = 0
oppSlot = 0

# clear slots
Turn(1, 'zero', 0)
Turn(1, 'zero', 1)
Turn(1, 'zero', 2)

Turn(2, 1, 'zero')
Turn(1, 'succ', 1)
for i in xrange(13):
	Turn(1, 'dbl', 1)
for i in xrange(11112 - 8192):
	Turn(1, 'succ', 1)

while ourSlot < total:
	Turn(2, 0, 'attack')

	if ourSlot > 0:
		for i in xrange(ourSlot):
			Turn(1, 'K', 0)
			Turn(1, 'S', 0)
			Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')

	if oppSlot > 0:
		for i in xrange(oppSlot):
			Turn(1, 'K', 0)
			Turn(1, 'S', 0)
			Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')

	Turn(1, 'K', 0)
	Turn(1, 'S', 0)
	Turn(2, 0, 'get')

	Turn(1, 'K', 0)
	Turn(1, 'S', 0)
	Turn(2, 0, 'succ')

	Turn(2, 0, 'zero')

	ourSlot += 1
	oppSlot += 1

while 1:
	Turn(1, 'I', 0)
